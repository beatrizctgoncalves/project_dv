import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
import numpy as np
import pandas as pd
import plotly.graph_objs as go


# Datasets
df = pd.read_csv('datasets/owid-covid-data.csv')
df = df[df['continent'].notna()]

# To be responsive
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

server = app.server

app.config.suppress_callback_exceptions = True
app.title = 'Covid-19'

# NavBar
# To connect to app pages
import home
import deaths
import variants
import vacination

#nav_home = dbc.NavItem(dbc.NavLink("Home", href="/home", active="exact"))
nav_deaths = dbc.NavItem(dbc.NavLink("Deaths", href="/deaths", active="exact"))
#nav_variants = dbc.NavItem(dbc.NavLink("Variants", href="/variants", active="exact"))
#nav_vacination = dbc.NavItem(dbc.NavLink("Vacination", href="/vacination", active="exact"))


colors = {
    'background': '#F6F5F3',
    'nav': '#283044'
}

COVID_LOGO = "assets/favicon.ico"

logo = dbc.Navbar(
    dbc.Container(
        [
            html.A(
                dbc.Row(
                    [
                        dbc.Col(html.Img(src=COVID_LOGO, height="80px", className="ml-2")),
                    ],
                    align="center"
                ),
                href="/",
            ),
            dbc.NavbarToggler(id="navbar-toggler2"),
            dbc.Collapse(
                dbc.Nav(
                    [nav_deaths], className="ml-auto", navbar=True
                ),
                id="navbar-collapse2",
                navbar=True
            ),
        ], fluid=True
    ),
    color=colors["nav"],
    dark=True,
    className="mb-3",
)

############################################Title##########################################################
content = html.Div(id="page-content")

app.layout = html.Div(
    #html.Link(rel="stylesheet", href="css/pico.min.css"),
    [dcc.Location(id="url"), logo, content], style={'backgroundColor': colors['background']}
)

@app.callback(Output("page-content", "children"), [Input("url", "pathname")])
def render(pathname):
    #if pathname == "/" or pathname == "/home":
    #    return home.layout
    if pathname == "/deaths":
        return deaths.layout
    #elif pathname == "/variants":
    #    return variants.layout
    #elif pathname == "/vacination":
    #    return vacination.layout
    return dbc.Jumbotron(
        [
            html.H1("Error 404: Page not found", className="text-danger"),
            html.Hr(),
            html.P("The page " + pathname + " was not fount...")
        ]
    )


if __name__ == '__main__':
    app.run_server(debug=True)