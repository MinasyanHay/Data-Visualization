import dash
from dash import dcc, html
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objects as go
from dash.dependencies import Input, Output
from .data_manager import load_and_prepare_data  # Relative import

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

# Analysis page layout
analysis_page = dbc.Container([
    # Header Section with Modern Design
    dbc.Row([
        dbc.Col([
            html.Div([
                # Modern Analysis Header
                html.Div([
                    html.Div([
                        html.I(className="fas fa-chart-line me-3", style={
                            'fontSize': '50px',
                            'verticalAlign': 'middle',
                            'color': '#4cc9f0'
                        }),
                        html.Span("Immigration Analysis", style={
                            'verticalAlign': 'middle',
                            'letterSpacing': '2px'
                        }),
                        html.Div(
                            "Analyse de l'immigration",
                            style={
                                'fontSize': '1.1em',
                                'opacity': '0.9',
                                'marginTop': '2px',
                                'letterSpacing': '1px'
                            }
                        )
                    ],
                        style={
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
                        }
                    ),
                ], className="text-center d-flex justify-content-center align-items-center",
                   style={'marginTop': '-20px', 'minHeight': '150px'}),
                html.H1("Deep Dive into Immigration Trends",
                        className="display-4 text-center text-white mb-1",
                        style={'fontSize': '3rem', 'marginTop': '5px'}),
                html.P("Explore Regional Patterns and Development Status Analysis",
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
                    html.H4("🔍 Analysis Controls", className="card-title text-primary mb-4"),
                    dbc.Row([
                        dbc.Col([
                            html.Label("🌍 Select Continent", className="control-label"),
                            dcc.Dropdown(
                                id='continent-dropdown',
                                options=[{'label': cont, 'value': cont}
                                         for cont in df['Continent'].unique()] if not df.empty else [],
                                value='Asia' if not df.empty and 'Asia' in df['Continent'].values else None,
                                clearable=False,
                                className="modern-dropdown mb-4"
                            )
                        ], md=6),
                        dbc.Col([
                            html.Label("🗺️ Select Region", className="control-label"),
                            dcc.Dropdown(
                                id='region-dropdown',
                                options=[{'label': reg, 'value': reg}
                                         for reg in df['Region'].unique()] if not df.empty else [],
                                value='Southern Asia' if not df.empty and 'Southern Asia' in df['Region'].values else None,
                                clearable=False,
                                className="modern-dropdown mb-4"
                            )
                        ], md=6)
                    ])
                ])
            ], className="control-panel-card")
        ])
    ], className="mb-4"),

    # Trend Analysis Section
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader(
                    html.H5("📈 Continental Immigration Trends", className="mb-0 text-white")
                ),
                dbc.CardBody([
                    dcc.Graph(id='continent-trend', className="graph-container")
                ])
            ], className="analysis-card mb-4")
        ], md=6),
        dbc.Col([
            dbc.Card([
                dbc.CardHeader(
                    html.H5("🌐 Regional Immigration Patterns", className="mb-0 text-white")
                ),
                dbc.CardBody([
                    dcc.Graph(id='region-trend', className="graph-container")
                ])
            ], className="analysis-card mb-4")
        ], md=6)
    ]),

    # Comparative Analysis Section
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader(
                    html.H5("🏆 Top 10 Contributing Regions", className="mb-0 text-white")
                ),
                dbc.CardBody([
                    dcc.Graph(id='top-10-regions', className="graph-container")
                ])
            ], className="analysis-card mb-4")
        ], md=6),
        dbc.Col([
            dbc.Card([
                dbc.CardHeader(
                    html.H5("🌍 Development Status Distribution", className="mb-0 text-white")
                ),
                dbc.CardBody([
                    dcc.Graph(id='dev-vs-developing', className="graph-container")
                ])
            ], className="analysis-card mb-4")
        ], md=6)
    ]),

    # Yearly Development Trends
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader(
                    html.H5("📊 Development Status Trends Over Time", className="mb-0 text-white")
                ),
                dbc.CardBody([
                    dcc.Graph(id='yearly-dev-vs-developing', className="graph-container")
                ])
            ], className="analysis-card")
        ])
    ])
], fluid=True, className="dashboard-container")


def register_callbacks(app):
    @app.callback(
        Output('continent-trend', 'figure'),
        [Input('continent-dropdown', 'value'),
         Input('dark-mode-state', 'data')]
    )
    def update_continent_trend(continent, dark_mode_state):
        if df.empty or not continent:
            return px.line(title="Data not available")
            
        # Get dark mode state
        is_dark = dark_mode_state.get('dark_mode', False)
        colors = COLOR_SCHEME['dark'] if is_dark else COLOR_SCHEME['light']
        
        # Set theme-aware colors
        bg_color = '#222222' if is_dark else 'white'
        text_color = 'white' if is_dark else '#333333'
        grid_color = 'rgba(255, 255, 255, 0.1)' if is_dark else 'rgba(0, 0, 0, 0.1)'
            
        continent_df = df[df['Continent'] == continent]
        yearly_totals = continent_df[years].sum()
        
        fig = px.line(x=years, y=yearly_totals,
                     title=f"Immigration Trend for {continent}",
                     labels={'x': 'Year', 'y': 'Number of Immigrants'},
                     color_discrete_sequence=[colors['accent']])
        
        fig.update_traces(
            line=dict(width=3),
            mode='lines+markers',
            marker=dict(size=8, symbol='circle')
        )
        
        fig.update_layout(
            template='plotly_dark' if is_dark else 'plotly_white',
            plot_bgcolor=bg_color,
            paper_bgcolor=bg_color,
            font=dict(color=text_color, size=12),
            title=dict(font=dict(size=16)),
            margin=dict(l=40, r=40, t=60, b=40),
            height=400,
            xaxis=dict(
                gridcolor=grid_color,
                title_font=dict(size=14),
                tickfont=dict(size=12)
            ),
            yaxis=dict(
                gridcolor=grid_color,
                title_font=dict(size=14),
                tickfont=dict(size=12)
            ),
            showlegend=False,
            hovermode='x unified'
        )
        return fig

    @app.callback(
        Output('region-trend', 'figure'),
        [Input('region-dropdown', 'value'),
         Input('dark-mode-state', 'data')]
    )
    def update_region_trend(region, dark_mode_state):
        if df.empty or not region:
            return px.line(title="Data not available")
            
        # Get dark mode state
        is_dark = dark_mode_state.get('dark_mode', False)
        colors = COLOR_SCHEME['dark'] if is_dark else COLOR_SCHEME['light']
        
        # Set theme-aware colors
        bg_color = '#222222' if is_dark else 'white'
        text_color = 'white' if is_dark else '#333333'
        grid_color = 'rgba(255, 255, 255, 0.1)' if is_dark else 'rgba(0, 0, 0, 0.1)'
            
        region_df = df[df['Region'] == region]
        yearly_totals = region_df[years].sum()
        
        fig = px.line(x=years, y=yearly_totals,
                     title=f"Immigration Trend for {region}",
                     labels={'x': 'Year', 'y': 'Number of Immigrants'},
                     color_discrete_sequence=[colors['primary']])
        
        fig.update_traces(
            line=dict(width=3),
            mode='lines+markers',
            marker=dict(size=8, symbol='circle')
        )
        
        fig.update_layout(
            template='plotly_dark' if is_dark else 'plotly_white',
            plot_bgcolor=bg_color,
            paper_bgcolor=bg_color,
            font=dict(color=text_color, size=12),
            title=dict(font=dict(size=16)),
            margin=dict(l=40, r=40, t=60, b=40),
            height=400,
            xaxis=dict(
                gridcolor=grid_color,
                title_font=dict(size=14),
                tickfont=dict(size=12)
            ),
            yaxis=dict(
                gridcolor=grid_color,
                title_font=dict(size=14),
                tickfont=dict(size=12)
            ),
            showlegend=False,
            hovermode='x unified'
        )
        return fig

    @app.callback(
        Output('top-10-regions', 'figure'),
        [Input('top-10-regions', 'id'),
         Input('dark-mode-state', 'data')]
    )
    def update_top_10_regions(_, dark_mode_state):
        if df.empty:
            return px.bar(title="Data not available")
            
        # Get dark mode state
        is_dark = dark_mode_state.get('dark_mode', False)
        colors = COLOR_SCHEME['dark'] if is_dark else COLOR_SCHEME['light']
        
        # Set theme-aware colors
        bg_color = '#222222' if is_dark else 'white'
        text_color = 'white' if is_dark else '#333333'
        grid_color = 'rgba(255, 255, 255, 0.1)' if is_dark else 'rgba(0, 0, 0, 0.1)'
            
        top_regions = df.groupby('Region')['Total'].sum().sort_values(ascending=True).tail(10)
        
        fig = go.Figure()
        fig.add_trace(
            go.Bar(
                x=top_regions.values,
                y=top_regions.index,
                orientation='h',
                marker_color=colors['accent'],
                text=top_regions.values,
                textposition='auto',
            )
        )
        
        fig.update_layout(
            title="Top 10 Regions by Total Immigration (1980-2013)",
            template='plotly_dark' if is_dark else 'plotly_white',
            plot_bgcolor=bg_color,
            paper_bgcolor=bg_color,
            font=dict(color=text_color, size=12),
            title_font=dict(size=16),
            margin=dict(l=40, r=40, t=60, b=40),
            height=400,
            xaxis=dict(
                gridcolor=grid_color,
                title="Total Immigrants",
                title_font=dict(size=14),
                tickfont=dict(size=12)
            ),
            yaxis=dict(
                gridcolor=grid_color,
                title="Region",
                title_font=dict(size=14),
                tickfont=dict(size=12)
            ),
            showlegend=False,
            bargap=0.2
        )
        return fig

    @app.callback(
        Output('dev-vs-developing', 'figure'),
        [Input('dev-vs-developing', 'id'),
         Input('dark-mode-state', 'data')]
    )
    def update_dev_vs_developing(_, dark_mode_state):
        if df.empty:
            return px.pie(title="Data not available")
            
        # Get dark mode state
        is_dark = dark_mode_state.get('dark_mode', False)
        colors = COLOR_SCHEME['dark'] if is_dark else COLOR_SCHEME['light']
        
        # Set theme-aware colors
        bg_color = '#222222' if is_dark else 'white'
        text_color = 'white' if is_dark else '#333333'
            
        dev_status = df.groupby('DevName')['Total'].sum()
        
        fig = go.Figure(data=[go.Pie(
            labels=dev_status.index,
            values=dev_status.values,
            hole=.4,
            marker=dict(colors=[colors['primary'], colors['accent']]),
            textinfo='label+percent',
            textfont=dict(size=14, color=text_color),
            hovertemplate="<b>%{label}</b><br>" +
                         "Immigrants: %{value:,.0f}<br>" +
                         "Percentage: %{percent:.1%}<extra></extra>"
        )])
        
        fig.update_layout(
            title="Immigration Distribution: Developed vs Developing Regions",
            template='plotly_dark' if is_dark else 'plotly_white',
            plot_bgcolor=bg_color,
            paper_bgcolor=bg_color,
            font=dict(color=text_color, size=12),
            title_font=dict(size=16),
            margin=dict(l=40, r=40, t=60, b=40),
            height=400,
            showlegend=True,
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1
            )
        )
        return fig

    @app.callback(
        Output('yearly-dev-vs-developing', 'figure'),
        [Input('yearly-dev-vs-developing', 'id'),
         Input('dark-mode-state', 'data')]
    )
    def update_yearly_dev_vs_developing(_, dark_mode_state):
        if df.empty:
            return go.Figure().update_layout(title="Data not available")
            
        # Get dark mode state
        is_dark = dark_mode_state.get('dark_mode', False)
        colors = COLOR_SCHEME['dark'] if is_dark else COLOR_SCHEME['light']
        
        # Set theme-aware colors
        bg_color = '#222222' if is_dark else 'white'
        text_color = 'white' if is_dark else '#333333'
        grid_color = 'rgba(255, 255, 255, 0.1)' if is_dark else 'rgba(0, 0, 0, 0.1)'
            
        dev_df = df[df['DevName'] == 'Developed regions'][years].sum()
        developing_df = df[df['DevName'] == 'Developing regions'][years].sum()
        
        fig = go.Figure()
        
        # Add traces with improved styling
        fig.add_trace(go.Scatter(
            x=years,
            y=dev_df,
            name='Developed',
            line=dict(color=colors['primary'], width=3),
            mode='lines+markers',
            marker=dict(size=8, symbol='circle'),
            hovertemplate="Year: %{x}<br>Immigrants: %{y:,.0f}<extra></extra>"
        ))
        
        fig.add_trace(go.Scatter(
            x=years,
            y=developing_df,
            name='Developing',
            line=dict(color=colors['accent'], width=3),
            mode='lines+markers',
            marker=dict(size=8, symbol='circle'),
            hovertemplate="Year: %{x}<br>Immigrants: %{y:,.0f}<extra></extra>"
        ))
        
        fig.update_layout(
            title="Yearly Immigration Trends: Developed vs Developing Regions",
            xaxis_title="Year",
            yaxis_title="Number of Immigrants",
            template='plotly_dark' if is_dark else 'plotly_white',
            plot_bgcolor=bg_color,
            paper_bgcolor=bg_color,
            font=dict(color=text_color, size=12),
            title_font=dict(size=16),
            margin=dict(l=40, r=40, t=60, b=40),
            height=400,
            xaxis=dict(
                gridcolor=grid_color,
                title_font=dict(size=14),
                tickfont=dict(size=12),
                showgrid=True
            ),
            yaxis=dict(
                gridcolor=grid_color,
                title_font=dict(size=14),
                tickfont=dict(size=12),
                showgrid=True
            ),
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1
            ),
            hovermode='x unified'
        )
        return fig
