import dash
from dash import dcc, html
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objects as go
from dash.dependencies import Input, Output
from .data_manager import load_and_prepare_data  # Relative import

# Load data
df, years = load_and_prepare_data()

# Color scheme
COLOR_SCHEME = {
    'primary': '#2b3e50',
    'secondary': '#4e5d6c',
    'accent': '#df691a',
    'background': 'linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%)',
    'text': '#333333',
    'card_bg': '#ffffff'
}

# Analysis page layout
analysis_page = dbc.Container([
    dbc.Row([
        html.H1("Detailed Immigration Analysis",
                className="text-center my-4 fade-in"),
        html.P("Dive deeper into immigration patterns by continent, region, and development status",
               className="text-center mb-4 fade-in", style={'color': COLOR_SCHEME['text']})
    ], justify="center"),
    dbc.Row([
        dbc.Col([
            html.H4("Select Continent", className="fade-in"),
            html.Div([
                dcc.Dropdown(
                    id='continent-dropdown',
                    options=[{'label': cont, 'value': cont}
                             for cont in df['Continent'].unique()] if not df.empty else [],
                    value='Asia' if not df.empty and 'Asia' in df['Continent'].values else None,
                    multi=False
                )
            ], className="dropdown-container fade-in"),
            dcc.Graph(id='continent-trend', className="graph-container")
        ], md=6, className="fade-in"),
        dbc.Col([
            html.H4("Select Region", className="fade-in"),
            html.Div([
                dcc.Dropdown(
                    id='region-dropdown',
                    options=[{'label': reg, 'value': reg}
                             for reg in df['Region'].unique()] if not df.empty else [],
                    value='Southern Asia' if not df.empty and 'Southern Asia' in df[
                        'Region'].values else None,
                    multi=False
                )
            ], className="dropdown-container fade-in"),
            dcc.Graph(id='region-trend', className="graph-container")
        ], md=6, className="fade-in")
    ], className="my-4"),
    dbc.Row([
        dbc.Col([
            html.H3("Top 10 Regions (1980-2013)",
                    className="text-center my-4 fade-in"),
            dcc.Graph(id='top-10-regions', className="graph-container")
        ], md=6, className="fade-in"),
        dbc.Col([
            html.H3("Developed vs Developing Regions",
                    className="text-center my-4 fade-in"),
            dcc.Graph(id='dev-vs-developing', className="graph-container")
        ], md=6, className="fade-in")
    ], className="my-4"),
    dbc.Row([
        html.H3("Yearly Trends: Developed vs Developing",
                className="text-center my-4 fade-in"),
        dcc.Graph(id='yearly-dev-vs-developing', className="graph-container")
    ], className="fade-in")
], fluid=True)


def register_callbacks(app):
    @app.callback(
        Output('continent-trend', 'figure'),
        [Input('continent-dropdown', 'value')]
    )
    def update_continent_trend(continent):
        if df.empty or not continent:
            return px.line(title="Data not available")
        continent_df = df[df['Continent'] == continent]
        yearly_totals = continent_df[years].sum()
        fig = px.line(x=years, y=yearly_totals, title=f"Immigration Trend for {continent}",
                      labels={'x': 'Year', 'y': 'Number of Immigrants'},
                      color_discrete_sequence=[COLOR_SCHEME['accent']])
        fig.update_layout(template='plotly_white',
                          plot_bgcolor=COLOR_SCHEME['card_bg'],
                          paper_bgcolor=COLOR_SCHEME['card_bg'],
                          # Reduced margins
                          margin=dict(l=40, r=40, t=60, b=40),
                          height=400)  # Consistent height
        return fig

    @app.callback(
        Output('region-trend', 'figure'),
        [Input('region-dropdown', 'value')]
    )
    def update_region_trend(region):
        if df.empty or not region:
            return px.line(title="Data not available")
        region_df = df[df['Region'] == region]
        yearly_totals = region_df[years].sum()
        fig = px.line(x=years, y=yearly_totals, title=f"Immigration Trend for {region}",
                      labels={'x': 'Year', 'y': 'Number of Immigrants'},
                      color_discrete_sequence=[COLOR_SCHEME['accent']])
        fig.update_layout(template='plotly_white',
                          plot_bgcolor=COLOR_SCHEME['card_bg'],
                          paper_bgcolor=COLOR_SCHEME['card_bg'],
                          # Reduced margins
                          margin=dict(l=40, r=40, t=60, b=40),
                          height=400)  # Consistent height
        return fig

    @app.callback(
        Output('top-10-regions', 'figure'),
        [Input('top-10-regions', 'id')]
    )
    def update_top_10_regions(_):
        if df.empty:
            return px.bar(title="Data not available")
        top_regions = df.groupby('Region')['Total'].sum(
        ).sort_values(ascending=False).head(10)
        fig = px.bar(x=top_regions.index, y=top_regions.values, title="Top 10 Regions (1980-2013)",
                     labels={'x': 'Region', 'y': 'Total Immigrants'},
                     color_discrete_sequence=[COLOR_SCHEME['accent']])
        fig.update_layout(template='plotly_white',
                          plot_bgcolor=COLOR_SCHEME['card_bg'],
                          paper_bgcolor=COLOR_SCHEME['card_bg'],
                          # Reduced margins
                          margin=dict(l=40, r=40, t=60, b=40),
                          height=400,  # Consistent height
                          xaxis_tickangle=45)  # Rotate labels
        return fig

    @app.callback(
        Output('dev-vs-developing', 'figure'),
        [Input('dev-vs-developing', 'id')]
    )
    def update_dev_vs_developing(_):
        if df.empty:
            return px.pie(title="Data not available")
        dev_status = df.groupby('DevName')['Total'].sum()
        fig = px.pie(values=dev_status.values, names=dev_status.index,
                     title="Developed vs Developing Regions",
                     color_discrete_sequence=[COLOR_SCHEME['primary'], COLOR_SCHEME['accent']])
        fig.update_layout(template='plotly_white',
                          plot_bgcolor=COLOR_SCHEME['card_bg'],
                          paper_bgcolor=COLOR_SCHEME['card_bg'],
                          # Reduced margins
                          margin=dict(l=40, r=40, t=60, b=40),
                          height=400)  # Consistent height
        return fig

    @app.callback(
        Output('yearly-dev-vs-developing', 'figure'),
        [Input('yearly-dev-vs-developing', 'id')]
    )
    def update_yearly_dev_vs_developing(_):
        if df.empty:
            return go.Figure().update_layout(title="Data not available")
        dev_df = df[df['DevName'] == 'Developed regions'][years].sum()
        developing_df = df[df['DevName'] == 'Developing regions'][years].sum()
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=years, y=dev_df, name='Developed',
                                 line=dict(color=COLOR_SCHEME['primary'])))
        fig.add_trace(go.Scatter(x=years, y=developing_df, name='Developing',
                                 line=dict(color=COLOR_SCHEME['accent'])))
        fig.update_layout(title="Yearly Immigration: Developed vs Developing",
                          xaxis_title="Year", yaxis_title="Number of Immigrants",
                          template='plotly_white',
                          plot_bgcolor=COLOR_SCHEME['card_bg'],
                          paper_bgcolor=COLOR_SCHEME['card_bg'],
                          # Reduced margins
                          margin=dict(l=40, r=40, t=60, b=40),
                          height=400)  # Consistent height
        return fig
