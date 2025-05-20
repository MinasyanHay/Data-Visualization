import dash
from dash import html, dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
from pages.home import home_page, register_callbacks as home_callbacks
from pages.analysis import analysis_page, register_callbacks as analysis_callbacks
from pages.maps import maps_page, register_callbacks as maps_callbacks

# Initialize Dash app with Bootstrap theme
LIGHT_THEME = dbc.themes.BOOTSTRAP
DARK_THEME = dbc.themes.DARKLY

app = dash.Dash(__name__, 
                external_stylesheets=[
                    LIGHT_THEME,
                    'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.4/css/all.min.css'
                ],
                suppress_callback_exceptions=True)

# Color schemes for light and dark modes
LIGHT_COLORS = {
    'primary': '#2b3e50',
    'secondary': '#4e5d6c',
    'accent': '#df691a',
    'background': '#ffffff',
    'text': '#333333',
    'card_bg': '#ffffff'
}

DARK_COLORS = {
    'primary': '#375a7f',
    'secondary': '#444444',
    'accent': '#00bc8c',
    'background': '#222222',
    'text': '#ffffff',
    'card_bg': '#303030'
}

# Register callbacks
home_callbacks(app)
analysis_callbacks(app)
maps_callbacks(app)

# Main layout
app.layout = html.Div([
    # Theme stylesheet
    html.Link(id='theme-stylesheet', href=LIGHT_THEME),
    
    # Store components for theme state
    dcc.Store(id='theme-store', data={'dark_mode': False}),
    dcc.Store(id='dark-mode-state', data={'dark_mode': False}),
    
    # Navigation
    dbc.NavbarSimple(
        children=[
            dbc.NavItem(dbc.NavLink("Home", href="/", className="nav-link")),
            dbc.NavItem(dbc.NavLink("Analysis", href="/analysis", className="nav-link")),
            dbc.NavItem(dbc.NavLink("Maps", href="/maps", className="nav-link")),
            html.Button(
                html.I(className="fas fa-moon"),
                id="dark-mode-toggle",
                className="btn btn-outline-light",
                n_clicks=0,
                style={
                    "marginLeft": "20px",
                    "transition": "all 0.3s ease",
                    "borderWidth": "2px"
                }
            )
        ],
        brand="Canadian Immigration Dashboard",
        brand_href="/",
        color="primary",
        dark=True,
        className="mb-4 shadow",
        sticky="top"
    ),
    
    # URL Location
    dcc.Location(id='url', refresh=False),
    
    # Main content container
    html.Div(
        id='page-content',
        className='container-fluid'
    ),
    
    # Footer
    html.Footer(
        dbc.Container([
            html.Hr(),
            dbc.Row([
                dbc.Col([
                    html.H5("Quick Links", className="text-primary"),
                    html.Ul([
                        html.Li(dcc.Link("Home", href="/")),
                        html.Li(dcc.Link("Analysis", href="/analysis")),
                        html.Li(dcc.Link("Maps", href="/maps"))
                    ], style={"listStyle": "none", "padding": 0})
                ], md=6),
                dbc.Col([
                    html.H5("Connect", className="text-primary"),
                    html.Div([
                        html.A(
                            html.I(className="fab fa-github fa-2x me-3"),
                            href="https://github.com/MinasyanHay/Data-Visualization",
                            target="_blank"
                        ),
                        html.A(
                            html.I(className="fab fa-linkedin fa-2x"),
                            href="https://www.linkedin.com/in/hayk-minasyan-8b228620a/",
                            target="_blank"
                        )
                    ])
                ], md=6)
            ], className="py-4")
        ], fluid=True),
        className="bg-light mt-5",
        id="footer"
    )
])

# Page routing callback
@app.callback(Output('page-content', 'children'), [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/analysis':
        return analysis_page
    elif pathname == '/maps':
        return maps_page
    return home_page

# Dark mode toggle callbacks
@app.callback(
    [Output("theme-stylesheet", "href"),
     Output("dark-mode-toggle", "children"),
     Output("dark-mode-toggle", "className"),
     Output("footer", "className"),
     Output("theme-store", "data")],
    [Input("dark-mode-toggle", "n_clicks")],
    [State("theme-store", "data")]
)
def toggle_theme(n_clicks, theme_data):
    if n_clicks is None:
        return LIGHT_THEME, html.I(className="fas fa-moon"), "btn btn-outline-light", "bg-light mt-5", {'dark_mode': False}
    
    dark_mode = not theme_data.get('dark_mode', False)
    theme_data = {'dark_mode': dark_mode}
    
    if dark_mode:
        button_class = "btn btn-outline-warning"  # More visible in dark mode
        footer_class = "bg-dark mt-5 text-light"
        icon = html.I(className="fas fa-sun")
        theme = DARK_THEME
    else:
        button_class = "btn btn-outline-light"
        footer_class = "bg-light mt-5"
        icon = html.I(className="fas fa-moon")
        theme = LIGHT_THEME
        
    return theme, icon, button_class, footer_class, theme_data

# Add a callback to share dark mode state with other components
@app.callback(
    Output("dark-mode-state", "data"),
    [Input("theme-store", "data")]
)
def update_dark_mode_state(theme_data):
    return theme_data

if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 10000))
    server = app.run(debug=False, host = '0.0.0.0', port = port )
