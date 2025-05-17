import dash
from dash import dcc, html
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objects as go
from dash.dependencies import Input, Output
from .data_manager import load_and_prepare_data
import pandas as pd

# Load data
df, years = load_and_prepare_data()

# Color scheme with dark mode variants
COLOR_SCHEME = {
    'light': {
        'primary': '#4361ee',
        'secondary': '#3f37c9',
        'accent': '#4895ef',
        'success': '#4cc9f0',
        'warning': '#f72585',
        'info': '#480ca8',
        'background': 'linear-gradient(135deg, #4cc9f0 0%, #4361ee 100%)',
        'text': '#333333',
        'card_bg': '#ffffff'
    },
    'dark': {
        'primary': '#4895ef',
        'secondary': '#3f37c9',
        'accent': '#4cc9f0',
        'success': '#4cc9f0',
        'warning': '#f72585',
        'info': '#480ca8',
        'background': 'linear-gradient(135deg, #222222 0%, #333333 100%)',
        'text': '#ffffff',
        'card_bg': '#222222'
    }
}

def register_callbacks(app):
    @app.callback(
        [Output('immigration-map', 'figure'),
         Output('stats-panel', 'children'),
         Output('top-countries', 'children')],
        [Input('year-slider', 'value'),
         Input('metric-dropdown', 'value'),
         Input('region-filter', 'value'),
         Input('dark-mode-state', 'data')]
    )
    def update_map(year_range, metric, region, dark_mode_state):
        if df.empty:
            empty_fig = go.Figure()
            empty_fig.update_layout(
                annotations=[dict(
                    text="No data available",
                    xref="paper",
                    yref="paper",
                    x=0.5,
                    y=0.5,
                    showarrow=False
                )]
            )
            return empty_fig, "No data available", "No data available"

        # Get dark mode state
        is_dark = dark_mode_state.get('dark_mode', False) if dark_mode_state else False
        colors = COLOR_SCHEME['dark'] if is_dark else COLOR_SCHEME['light']
        
        # Set colors based on theme
        bg_color = '#222222' if is_dark else '#ffffff'
        text_color = '#ffffff' if is_dark else '#333333'
        land_color = '#2e2e2e' if is_dark else 'rgb(229, 236, 246)'
        ocean_color = '#1a1a1a' if is_dark else 'rgba(211, 233, 250, 0.8)'
        country_color = '#404040' if is_dark else 'rgba(67, 97, 238, 0.3)'
        grid_color = 'rgba(255, 255, 255, 0.1)' if is_dark else 'rgba(67, 97, 238, 0.1)'

        # Filter data based on region
        filtered_df = df.copy()
        if region != 'all':
            filtered_df = filtered_df[filtered_df['Continent'] == region]
        
        # Prepare data based on metric
        if metric == 'Total':
            data = filtered_df.copy()
            year_columns = [str(year) for year in range(year_range[0], year_range[1] + 1)]
            data['Value'] = data[year_columns].sum(axis=1)
            title = f'Immigration Distribution ({year_range[0]}-{year_range[1]})'
        elif metric == 'Growth':
            data = filtered_df.copy()
            start_year = str(year_range[0])
            end_year = str(year_range[1])
            data['Value'] = ((data[end_year] - data[start_year]) / data[start_year] * 100)
            title = f'Growth Rate ({year_range[0]}-{year_range[1]})'
        else:  # YoY
            data = filtered_df.copy()
            year_columns = [str(year) for year in range(year_range[0], year_range[1] + 1)]
            data['Value'] = 0
            for i in range(1, len(year_columns)):
                data['Value'] += ((data[year_columns[i]] - data[year_columns[i-1]]) / 
                               data[year_columns[i-1]] * 100)
            data['Value'] = data['Value'] / (len(year_columns) - 1)
            title = f'Average Year-over-Year Change ({year_range[0]}-{year_range[1]})'

        # Create choropleth map
        fig = go.Figure(data=go.Choropleth(
            locations=data['Country'],
            locationmode='country names',
            z=data['Value'],
            text=data['Country'],
            colorscale=['#3f37c9', '#4361ee', '#4895ef', '#4cc9f0'] if is_dark else 'Viridis',
            marker_line_color=country_color,
            marker_line_width=0.5,
            colorbar=dict(
                title=dict(
                    text=metric,
                    font=dict(color=text_color)
                ),
                tickfont=dict(color=text_color)
            )
        ))

        # Update layout
        fig.update_layout(
            title=dict(
                text=title,
                font=dict(color=text_color, size=16),
                x=0.5,
                y=0.95
            ),
            height=600,
            margin=dict(l=0, r=0, t=50, b=0),
            paper_bgcolor=bg_color,
            plot_bgcolor=bg_color,
            font=dict(
                family="Inter, sans-serif",
                size=12,
                color=text_color
            ),
            geo=dict(
                showframe=True,
                framecolor=grid_color,
                showcoastlines=True,
                coastlinecolor=grid_color,
                projection_type='natural earth',
                showland=True,
                landcolor=land_color,
                showocean=True,
                oceancolor=ocean_color,
                showcountries=True,
                countrycolor=country_color,
                bgcolor=bg_color,
                resolution=110,
                lataxis=dict(
                    showgrid=True,
                    gridcolor=grid_color,
                    gridwidth=0.5,
                    range=[-60, 90]
                ),
                lonaxis=dict(
                    showgrid=True,
                    gridcolor=grid_color,
                    gridwidth=0.5,
                    range=[-180, 180]
                ),
                center=dict(lon=0, lat=30),
                projection_scale=1.3
            ),
            dragmode='pan',
            updatemenus=[
                dict(
                    type='buttons',
                    showactive=True,
                    buttons=[
                        dict(
                            args=[{'geo.projection.type': 'natural earth'}],
                            label='Natural Earth',
                            method='relayout'
                        ),
                        dict(
                            args=[{'geo.projection.type': 'equirectangular'}],
                            label='Equirectangular',
                            method='relayout'
                        ),
                        dict(
                            args=[{'geo.projection.type': 'orthographic'}],
                            label='Orthographic',
                            method='relayout'
                        ),
                        dict(
                            args=[{'geo.projection.type': 'mollweide'}],
                            label='Mollweide',
                            method='relayout'
                        )
                    ],
                    direction='down',
                    x=0.1,
                    y=1.15,
                    bgcolor=colors['primary'],
                    font=dict(color='white')
                )
            ]
        )

        # Calculate statistics
        stats = [
            dbc.Row([
                dbc.Col([
                    html.Div([
                        html.I(className="fas fa-globe me-2"),
                        html.Span(f"Countries: {len(data)}")
                    ], className=f"stat-item {'bg-dark text-light' if is_dark else ''}")
                ], width=6),
                dbc.Col([
                    html.Div([
                        html.I(className="fas fa-calculator me-2"),
                        html.Span(f"Average: {data['Value'].mean():.1f}")
                    ], className=f"stat-item {'bg-dark text-light' if is_dark else ''}")
                ], width=6)
            ]),
            dbc.Row([
                dbc.Col([
                    html.Div([
                        html.I(className="fas fa-arrow-up me-2"),
                        html.Span(f"Maximum: {data['Value'].max():.1f}")
                    ], className=f"stat-item {'bg-dark text-light' if is_dark else ''}")
                ], width=6),
                dbc.Col([
                    html.Div([
                        html.I(className="fas fa-arrow-down me-2"),
                        html.Span(f"Minimum: {data['Value'].min():.1f}")
                    ], className=f"stat-item {'bg-dark text-light' if is_dark else ''}")
                ], width=6)
            ])
        ]

        # Get top 5 countries
        top_5 = data.nlargest(5, 'Value')
        top_countries = html.Div([
            html.Div([
                html.Span(f"{i+1}. {row['Country']}", className=f"country-name {'text-light' if is_dark else ''}"),
                html.Span(f"{row['Value']:.1f}", className=f"country-value {'text-light' if is_dark else ''}")
            ], className=f"top-country-item {'bg-dark' if is_dark else ''}")
            for i, (_, row) in enumerate(top_5.iterrows())
        ], className="top-countries-list")

        return fig, stats, top_countries

# Maps page layout
maps_page = dbc.Container([
    # Header Section with Airport Sign Style
    dbc.Row([
        dbc.Col([
            html.Div([
                # Airport-style sign
                html.Div([
                    html.Div([
                        html.I(className="fas fa-arrow-down me-3", style={
                            'fontSize': '50px',
                            'verticalAlign': 'middle',
                            'color': '#ff0000'
                        }),
                        html.Img(
                            src="https://upload.wikimedia.org/wikipedia/commons/d/d9/Flag_of_Canada_%28Pantone%29.svg",
                            style={
                                'height': '55px',
                                'marginRight': '25px',
                                'verticalAlign': 'middle'
                            }
                        ),
                        html.Span("Canada Arrivals", style={
                            'verticalAlign': 'middle',
                            'letterSpacing': '2px'
                        }),
                        html.Div(
                            "Arrivées Canada",
                            style={
                                'fontSize': '1.1em',
                                'opacity': '0.9',
                                'marginTop': '2px',
                                'letterSpacing': '1px'
                            }
                        )
                    ], style={
                        'backgroundColor': 'black',
                        'color': 'white',
                        'padding': '30px 70px',
                        'borderRadius': '15px',
                        'fontSize': '42px',
                        'fontWeight': 'bold',
                        'display': 'inline-block',
                        'marginBottom': '10px',
                        'boxShadow': '0 8px 30px rgba(0, 0, 0, 0.5)',
                        'fontFamily': 'Arial, sans-serif',
                        'letterSpacing': '1px',
                        'width': '90%',
                        'maxWidth': '1200px',
                        'border': '3px solid rgba(255, 255, 255, 0.15)',
                        'position': 'relative',
                        'top': '-10px'
                    }),
                ], className="text-center d-flex justify-content-center align-items-center",
                   style={'marginTop': '-20px', 'minHeight': '150px'}),
                html.H1("Global Immigration Explorer",
                        className="display-4 text-center text-white mb-1",
                        style={'fontSize': '3rem', 'marginTop': '5px'}),
                html.P("Discover Immigration Patterns Through Interactive Data Visualization",
                       className="lead text-center text-white mb-2",
                       style={'fontSize': '1.3rem'})
            ], className="header-content py-2")
        ], className="header-section mb-2")
    ], className="gradient-background", style={'marginTop': '-24px'}),

    # Control Panel Section
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H4("🎛️ Control Panel", className="card-title text-primary mb-4"),
                    # Year Range Selection with Modern Styling
                    html.Label("📅 Select Year Range", className="control-label"),
                    dcc.RangeSlider(
                        id='year-slider',
                        min=1980,
                        max=2013,
                        value=[1980, 2013],
                        marks={str(year): {'label': str(year)} 
                               for year in range(1980, 2014, 5)},
                        step=1,
                        className="modern-slider mb-4"
                    ),
                    
                    dbc.Row([
                        dbc.Col([
                            # Metric Selection
                            html.Label("📊 Select Metric", className="control-label"),
                            dcc.Dropdown(
                                id='metric-dropdown',
                                options=[
                                    {'label': '📈 Total Immigrants', 'value': 'Total'},
                                    {'label': '📊 Growth Rate (%)', 'value': 'Growth'},
                                    {'label': '📉 Year-over-Year Change', 'value': 'YoY'}
                                ],
                                value='Total',
                                clearable=False,
                                className="modern-dropdown"
                            )
                        ], width=6),
                        
                        dbc.Col([
                            # Region Filter
                            html.Label("🌍 Filter by Region", className="control-label"),
                            dcc.Dropdown(
                                id='region-filter',
                                options=[
                                    {'label': '🌐 All Regions', 'value': 'all'},
                                    {'label': '🌏 Asia', 'value': 'Asia'},
                                    {'label': '🌍 Europe', 'value': 'Europe'},
                                    {'label': '🌍 Africa', 'value': 'Africa'},
                                    {'label': '🌎 Americas', 'value': 'Latin America and the Caribbean'},
                                    {'label': '🌎 Northern America', 'value': 'Northern America'},
                                    {'label': '🌏 Oceania', 'value': 'Oceania'}
                                ],
                                value='all',
                                clearable=False,
                                className="modern-dropdown"
                            )
                        ], width=6)
                    ])
                ])
            ], className="control-panel-card")
        ], width=12)
    ], className="mb-4"),

    # Visualization Section
    dbc.Row([
        # Map Column
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H4("🗺️ Geographic Distribution", className="card-title text-primary mb-3"),
                    dcc.Graph(
                        id='immigration-map',
                        className="map-container",
                        config={'displayModeBar': True, 'scrollZoom': True}
                    )
                ])
            ], className="map-card")
        ], width=8),
        
        # Statistics Column
        dbc.Col([
            # Statistics Card
            dbc.Card([
                dbc.CardHeader(html.H5("📊 Statistics & Insights", className="mb-0 text-white")),
                dbc.CardBody([
                    html.Div(id='stats-panel', className="stats-container"),
                    html.Hr(className="my-3"),
                    html.H6("🏆 Top Contributing Countries", className="mb-3"),
                    html.Div(id='top-countries', className="top-countries-container")
                ])
            ], className="stats-card")
        ], width=4)
    ])
], fluid=True, className="dashboard-container")
