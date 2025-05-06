import dash
from dash import dcc, html
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
from dash.dependencies import Input, Output

# Load and prepare the data
try:
    df = pd.read_csv('canadian_immegration_data.csv')
    years = [str(year) for year in range(1980, 2014)]
    if not all(year in df.columns for year in years):
        raise ValueError("Not all years are present in the DataFrame columns")
    df['Total'] = df[years].sum(axis=1)
    df['Growth'] = ((df[years[-1]] - df[years[0]]) /
                    df[years[0]] * 100).round(1)
    df['Variance'] = df[years].var(axis=1)
    yearly_totals = df[years].sum()
    peak_year = yearly_totals.idxmax()
except Exception as e:
    print(f"Error loading data: {e}")
    df = pd.DataFrame()
    years = []
    yearly_totals = pd.Series()
    peak_year = "N/A"

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
        html.H1("Canadian Immigration Dashboard",
                className="text-center my-4 fade-in"),
        html.P("Explore immigration trends to Canada from 1980 to 2013",
               className="text-center mb-4 fade-in", style={'color': COLOR_SCHEME['text']}),
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
        dbc.Col(insight_card("Fastest Growing Source",
                             df.loc[df['Growth'].idxmax(
                             )]['Country'] if not df.empty else "N/A",
                             f"{df['Growth'].max():.1f}% growth" if not df.empty else "N/A"), md=3),
        dbc.Col(insight_card("Most Consistent Contributor",
                             df.loc[df['Variance'].idxmin(
                             )]['Country'] if not df.empty else "N/A",
                             "Lowest variance"), md=3),
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
        html.H3("Select Year for Detailed Analysis",
                className="text-center my-4 fade-in"),
        html.Div([
            dcc.Slider(
                id='year-slider',
                min=1980,
                max=2013,
                value=2010,
                marks={str(year): str(year) for year in range(1980, 2014, 5)},
                step=1
            )
        ], className="slider-container fade-in"),
        dcc.Graph(id='top-10-countries-year', className="graph-container")
    ])
], fluid=True)

# Register callbacks


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
        fig.update_layout(template='plotly_white',
                          plot_bgcolor=COLOR_SCHEME['card_bg'],
                          paper_bgcolor=COLOR_SCHEME['card_bg'])
        return fig

    @app.callback(
        Output('top-10-countries-year', 'figure'),
        [Input('year-slider', 'value')]
    )
    def update_top_10_countries(year):
        if df.empty:
            return px.bar(title="Data not available")
        year = str(year)
        top_10 = df[['Country', year]].sort_values(
            by=year, ascending=False).head(10)
        fig = px.bar(top_10, x='Country', y=year, title=f"Top 10 Countries in {year}",
                     labels={'y': 'Number of Immigrants'},
                     color_discrete_sequence=[COLOR_SCHEME['accent']])
        fig.update_layout(template='plotly_white',
                          plot_bgcolor=COLOR_SCHEME['card_bg'],
                          paper_bgcolor=COLOR_SCHEME['card_bg'])
        return fig
