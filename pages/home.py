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
    return dbc.Card([
        dbc.CardBody([
            # Icon and Title Row
            html.Div([
                # Dynamic icon based on title
                html.I(
                    className=f"fas {get_card_icon(title)} fa-2x me-3",
                    style={'color': COLOR_SCHEME['accent']}
                ),
                html.H4(title, className="card-title mb-0")
            ], className="d-flex align-items-center mb-3"),
            
            # Value with animation
            html.Div([
                html.H2(
                    value,
                    className="card-value mb-2",
                    style={
                        'fontSize': '2.2rem',
                        'fontWeight': '600',
                        'color': COLOR_SCHEME['primary'],
                        'fontFamily': "'Inter', sans-serif"
                    }
                ),
                # Subtitle with icon
                html.Div([
                    html.I(className="fas fa-info-circle me-2", 
                          style={'color': COLOR_SCHEME['secondary'], 'opacity': '0.7'}),
                    html.Span(
                        subtitle,
                        style={'color': COLOR_SCHEME['secondary'], 'fontSize': '0.9rem'}
                    )
                ], className="d-flex align-items-center")
            ], className="text-center")
        ], className="p-4")
    ], className="insights-card h-100 border-0 shadow-sm")

def get_card_icon(title):
    icon_map = {
        "Total Immigrants": "fa-users",
        "Top Country": "fa-flag",
        "Top Continent": "fa-globe-americas",
        "Avg. Yearly Immigration": "fa-chart-line",
        "Top Country (2000s)": "fa-calendar-alt",
        "Largest Drop in Immigration": "fa-arrow-down",
        "Most Diversified Year": "fa-globe",
        "Peak Immigration Year": "fa-chart-bar"
    }
    return icon_map.get(title, "fa-chart-pie")

# Home page layout
home_page = dbc.Container([
    # Header Section
    dbc.Row([
        dbc.Col([
            html.Div([
                html.H1("Canadian Immigration Dashboard",
                        className="display-4 text-center mb-3",
                        style={'fontWeight': '700', 'color': '#ffffff'}),
                html.P("Explore immigration trends to Canada from 1980 to 2013",
                       className="lead text-center mb-4 beautiful-subtitle",
                       style={'fontSize': '1.3rem', 'color': '#ffffff'})
            ], className="text-center py-4 rounded-3 mb-4",
               style={'background': 'linear-gradient(135deg, #4361ee 0%, #4cc9f0 100%)'})
        ], width=12)
    ]),

    # Error Message (if needed)
    html.Div("Data not loaded. Please check the CSV file.",
             className="error-message alert alert-danger",
             id='error-message',
             style={'display': 'none' if not df.empty else 'block'}),

    # First Row of Cards
    dbc.Row([
        dbc.Col(insight_card(
            "Total Immigrants",
            f"{df['Total'].sum():,}" if not df.empty else "N/A",
            "1980-2013"
        ), md=3, className="mb-4"),
        
        dbc.Col(insight_card(
            "Top Country",
            df.loc[df['Total'].idxmax()]['Country'] if not df.empty else "N/A",
            f"{df['Total'].max():,} immigrants" if not df.empty else "N/A"
        ), md=3, className="mb-4"),
        
        dbc.Col(insight_card(
            "Top Continent",
            df.groupby('Continent')['Total'].sum().idxmax() if not df.empty else "N/A",
            f"{df.groupby('Continent')['Total'].sum().max():,} immigrants" if not df.empty else "N/A"
        ), md=3, className="mb-4"),
        
        dbc.Col(insight_card(
            "Avg. Yearly Immigration",
            f"{int(df[years].sum().mean()):,}" if not df.empty else "N/A",
            "Per Year"
        ), md=3, className="mb-4")
    ], className="g-4"),

    # Second Row of Cards
    dbc.Row([
        dbc.Col(insight_card(
            "Top Country (2000s)",
            df.loc[df[[str(y) for y in range(2000, 2010)]].sum(axis=1).idxmax()]['Country'] if not df.empty else "N/A",
            "2000–2009"
        ), md=3, className="mb-4"),

        dbc.Col(insight_card(
            "Largest Drop in Immigration",
            df.loc[df['Growth'].idxmin()]['Country'] if not df.empty else "N/A",
            f"{df['Growth'].min():.1f}% drop" if not df.empty else "N/A"
        ), md=3, className="mb-4"),

        dbc.Col(insight_card(
            "Most Diversified Year",
            str(df[years].gt(0).sum().idxmax()) if not df.empty else "N/A",
            f"{df[years].gt(0).sum().max()} countries contributed" if not df.empty else "N/A"
        ), md=3, className="mb-4"),

        dbc.Col(insight_card(
            "Peak Immigration Year",
            str(peak_year) if not df.empty else "N/A",
            f"{yearly_totals.max():,} immigrants" if not df.empty else "N/A"
        ), md=3, className="mb-4")
    ], className="g-4"),

    # Graphs Section
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader(
                    html.H3("Total Immigration by Year",
                            className="text-center mb-0",
                            style={'fontSize': '1.5rem', 'fontWeight': '600'}),
                    className="bg-primary text-white"
                ),
                dbc.CardBody([
                    dcc.Graph(id='total-by-year', className="graph-container")
                ])
            ], className="border-0 shadow-sm")
        ], width=12, className="mb-4")
    ]),

    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader(
                    html.H3("Top Countries by Selected Year Range",
                            className="text-center mb-0",
                            style={'fontSize': '1.5rem', 'fontWeight': '600'}),
                    className="bg-primary text-white"
                ),
                dbc.CardBody([
                    html.Div([
                        dcc.RangeSlider(
                            id='year-range-slider',
                            min=1980,
                            max=2013,
                            value=[2000, 2010],
                            marks={str(year): str(year) for year in range(1980, 2014, 5)},
                            step=1,
                            className="my-4"
                        )
                    ], className="px-4"),
                    dcc.Graph(id='top-10-countries-year', className="graph-container")
                ])
            ], className="border-0 shadow-sm")
        ], width=12)
    ])
], fluid=True, className="py-4")

# Callbacks


def register_callbacks(app):
    @app.callback(
        Output('total-by-year', 'figure'),
        [Input('total-by-year', 'id'),
         Input('dark-mode-state', 'data')]
    )
    def update_total_by_year(_, dark_mode_state):
        if df.empty:
            return px.line(title="Data not available")
            
        # Get dark mode state
        is_dark = dark_mode_state.get('dark_mode', False)
        
        # Set theme-aware colors
        bg_color = '#222222' if is_dark else 'white'
        text_color = 'white' if is_dark else '#333333'
        grid_color = 'rgba(255, 255, 255, 0.1)' if is_dark else 'rgba(0, 0, 0, 0.1)'
            
        yearly_totals = df[years].sum()
        fig = px.line(x=years, y=yearly_totals, title="Total Immigration to Canada (1980–2013)",
                      labels={'x': 'Year', 'y': 'Number of Immigrants'})
        fig.update_layout(
            template='plotly_dark' if is_dark else 'plotly_white',
            plot_bgcolor=bg_color,
            paper_bgcolor=bg_color,
            font=dict(color=text_color),
            margin=dict(l=40, r=40, t=60, b=40),
            height=400,
            xaxis=dict(gridcolor=grid_color),
            yaxis=dict(gridcolor=grid_color)
        )
        return fig

    @app.callback(
        Output('top-10-countries-year', 'figure'),
        [Input('year-range-slider', 'value'),
         Input('dark-mode-state', 'data')]
    )
    def update_top_10_countries(year_range, dark_mode_state):
        if df.empty:
            return px.bar(title="Data not available")
            
        # Get dark mode state
        is_dark = dark_mode_state.get('dark_mode', False)
        
        # Set theme-aware colors
        bg_color = '#222222' if is_dark else 'white'
        text_color = 'white' if is_dark else '#333333'
        grid_color = 'rgba(255, 255, 255, 0.1)' if is_dark else 'rgba(0, 0, 0, 0.1)'
            
        start_year, end_year = year_range
        selected_years = [str(year) for year in range(start_year, end_year + 1)]
        if not selected_years:
            return px.bar(title="No years selected")
        df_selected = df[['Country'] + selected_years].copy()
        df_selected['Total'] = df_selected[selected_years].sum(axis=1)
        top_10 = df_selected[['Country', 'Total']].sort_values(by='Total', ascending=False).head(10)
        fig = px.bar(
            top_10,
            x='Country',
            y='Total',
            title=f"Top 10 Countries ({start_year}–{end_year})",
            labels={'Total': 'Number of Immigrants'},
            color_discrete_sequence=[COLOR_SCHEME['accent']]
        )
        fig.update_layout(
            template='plotly_dark' if is_dark else 'plotly_white',
            plot_bgcolor=bg_color,
            paper_bgcolor=bg_color,
            font=dict(color=text_color),
            margin=dict(l=40, r=40, t=60, b=40),
            height=400,
            xaxis_tickangle=45,
            showlegend=False,
            xaxis=dict(gridcolor=grid_color),
            yaxis=dict(gridcolor=grid_color)
        )
        return fig
