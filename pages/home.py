import dash
from dash import dcc, html
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
from dash.dependencies import Input, Output
from .data_manager import load_and_prepare_data  # Relative import

# Load data
df, years = load_and_prepare_data()

# Rename United Kingdom
if not df.empty:
    df['Country'] = df['Country'].replace(
        'United Kingdom of Great Britain and Northern Ireland', 'UK & N Ireland')

yearly_totals = df[years].sum() if not df.empty else pd.Series()
peak_year = yearly_totals.idxmax() if not df.empty else "N/A"

# Color scheme
COLOR_SCHEME = {
    'primary': '#2b3e50',
    'secondary': '#4e5d6c',
    'accent': '#df691a',
    'background': 'linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%)',
    'text': '#333333',
    'card_bg': '#ffffff'
}

# Helper function for card layout


def insight_card(title, value, subtitle):
    return html.Div([
        html.H4(title, className="card-title"),
        html.H2(value, className="card-text"),
        html.P(subtitle, className="card-subtitle text-muted")
    ], className="insights-card fade-in")


# Home page layout
home_page = dbc.Container([
    dbc.Row([
        html.P("Explore immigration trends to Canada from 1980 to 2013",
               className="text-center mb-4 fade-in beautiful-subtitle",
               style={'color': COLOR_SCHEME['text']}),
        html.Div("Data not loaded. Please check the CSV file.", className="error-message",
                 id='error-message', style={'display': 'none' if not df.empty else 'block'})
    ], justify="center"),

    dbc.Row([
        dbc.Col(insight_card("Total Immigrants",
                             f"{df['Total'].sum():,}" if not df.empty else "N/A",
                             "1980-2013"), md=3),
        dbc.Col(insight_card("Top Country",
                             df.loc[df['Total'].idxmax(
                             )]['Country'] if not df.empty else "N/A",
                             f"{df['Total'].max():,} immigrants" if not df.empty else "N/A"), md=3),
        dbc.Col(insight_card("Top Continent",
                             df.groupby('Continent')['Total'].sum(
                             ).idxmax() if not df.empty else "N/A",
                             f"{df.groupby('Continent')['Total'].sum().max():,} immigrants" if not df.empty else "N/A"), md=3),
        dbc.Col(insight_card("Avg. Yearly Immigration",
                             f"{int(df[years].sum().mean()):,}" if not df.empty else "N/A",
                             "Per Year"), md=3),
    ], className="my-4", justify="center"),

    dbc.Row([
        dbc.Col(insight_card("Top Country (2000s)",
                             df.loc[df[[str(y) for y in range(2000, 2010)]].sum(
                                 axis=1).idxmax()]['Country'] if not df.empty else "N/A",
                             "2000–2009"), md=3),

        dbc.Col(insight_card(
            "Largest Drop in Immigration",
            df.loc[df['Growth'].idxmin()]['Country'] if not df.empty else "N/A",
            f"{df['Growth'].min():.1f}% drop" if not df.empty else "N/A"
        ), md=3),

        dbc.Col(insight_card(
            "Most Diversified Year",
            str(df[years].gt(0).sum().idxmax()) if not df.empty else "N/A",
            f"{df[years].gt(0).sum().max()} countries contributed" if not df.empty else "N/A"
        ), md=3),

        dbc.Col(insight_card("Peak Immigration Year",
                             str(peak_year) if not df.empty else "N/A",
                             f"{yearly_totals.max():,} immigrants" if not df.empty else "N/A"), md=3)
    ], className="my-4", justify="center"),

    dbc.Row([
        html.H3("Total Immigration by Year",
                className="text-center my-4 fade-in"),
        dcc.Graph(id='total-by-year', className="graph-container")
    ], className="fade-in"),

    dbc.Row([
        html.H3("Top Countries by Selected Year Range",
                className="text-center my-4 fade-in"),
        html.Div([
            dcc.RangeSlider(
                id='year-range-slider',
                min=1980,
                max=2013,
                value=[2000, 2010],  # Default range
                marks={str(year): str(year) for year in range(1980, 2014, 5)},
                step=1
            )
        ], className="slider-container fade-in"),
        dcc.Graph(id='top-10-countries-year', className="graph-container")
    ])
], fluid=True)

# Callbacks


def register_callbacks(app):
    @app.callback(
        Output('total-by-year', 'figure'),
        [Input('total-by-year', 'id')]
    )
    def update_total_by_year(_):
        if df.empty:
            return px.line(title="Data not available")
        yearly_totals = df[years].sum()
        fig = px.line(x=years, y=yearly_totals, title="Total Immigration to Canada (1980–2013)",
                      labels={'x': 'Year', 'y': 'Number of Immigrants'})
        fig.update_layout(
            template='plotly_white',
            plot_bgcolor=COLOR_SCHEME['card_bg'],
            paper_bgcolor=COLOR_SCHEME['card_bg'],
            margin=dict(l=40, r=40, t=60, b=40),
            height=400
        )
        return fig

    @app.callback(
        Output('top-10-countries-year', 'figure'),
        [Input('year-range-slider', 'value')]
    )
    def update_top_10_countries(year_range):
        if df.empty:
            return px.bar(title="Data not available")
        start_year, end_year = year_range
        selected_years = [str(year)
                          for year in range(start_year, end_year + 1)]
        if not selected_years:
            return px.bar(title="No years selected")
        df_selected = df[['Country'] + selected_years].copy()
        df_selected['Total'] = df_selected[selected_years].sum(axis=1)
        top_10 = df_selected[['Country', 'Total']].sort_values(
            by='Total', ascending=False).head(10)
        fig = px.bar(
            top_10,
            x='Country',
            y='Total',
            title=f"Top 10 Countries ({start_year}–{end_year})",
            labels={'Total': 'Number of Immigrants'},
            color_discrete_sequence=[COLOR_SCHEME['accent']]
        )
        fig.update_layout(
            template='plotly_white',
            plot_bgcolor=COLOR_SCHEME['card_bg'],
            paper_bgcolor=COLOR_SCHEME['card_bg'],
            margin=dict(l=40, r=40, t=60, b=40),
            height=400,
            xaxis_tickangle=45,
            showlegend=False
        )
        return fig
