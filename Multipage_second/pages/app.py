# Initializing the main Dash app for the Canadian Immigration Dashboard
import dash
from dash import html, dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
from home import home_page, register_callbacks as home_callbacks
from analysis import analysis_page, register_callbacks as analysis_callbacks

# Setting up the Dash app with Bootstrap theme for styling
app = dash.Dash(__name__, external_stylesheets=[
                dbc.themes.BOOTSTRAP], suppress_callback_exceptions=True)

# Defining color scheme for Python usage
COLOR_SCHEME = {
    'primary': '#2b3e50',
    'secondary': '#4e5d6c',
    'accent': '#df691a',
    'background': 'linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%)',
    'text': '#333333',
    'card_bg': '#ffffff'
}

# Registering callbacks from home and analysis pages
home_callbacks(app)
analysis_callbacks(app)

# Creating the main layout with navigation bar and external CSS
app.layout = html.Div([
    html.Link(rel='stylesheet', href='/assets/styles.css'),
    dcc.Location(id='url', refresh=False),
    dbc.NavbarSimple(
        children=[
            dbc.NavItem(dbc.NavLink("Home", href="/")),
            dbc.NavItem(dbc.NavLink("Analysis", href="/analysis"))
        ],
        brand="Canadian Immigration Dashboard",
        brand_href="/",
        color=COLOR_SCHEME['primary'],
        dark=True,
    ),
    html.Div(id='page-content')
])

# Callback to handle page navigation


@app.callback(Output('page-content', 'children'), [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/analysis':
        return analysis_page
    else:
        return home_page


# Running the app
if __name__ == '__main__':
    app.run(debug=True)
