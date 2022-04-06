import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
import numpy as np
import pandas as pd
import plotly.graph_objs as go


# https://htmlcheatsheet.com/css/

######################################################Data##############################################################
# Dataset Vacinas
#df_vacinas = pd.read_csv('country_vaccinations.csv')



######################################################Interactive Components############################################

#country_options = [dict(label=country, value=country) for country in df['country_name'].unique()]

#dropdown_country = dcc.Dropdown(
#        id='country_drop',
#        options=country_options,
#        value=['Portugal'],
#        multi=True
#    )


##################################################APP###################################################################
# To be responsive
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

server = app.server

app.config.suppress_callback_exceptions = True
app.title = 'Covid-19'

######################################################NavBar##############################################################
# To connect to app pages
import home

COVID_LOGO = "https://www.pat.nhs.uk/Coronavirus/images/Covid%2019%20Icon.png"

nav_item_home = dbc.NavItem(dbc.NavLink("Home", href="/home", active="exact"))

CONTENT_STYLE = {
    "margin-left": "18rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem",
}

logo = dbc.Navbar(
    dbc.Container(
        [
            html.A(
                dbc.Row(
                    [
                        dbc.Col(html.Img(src=COVID_LOGO, height="30px", className="ml-2")),
                    ],
                    align="center",
                    no_gutters=True,
                ),
                href="/home",
            ),
            dbc.NavbarToggler(id="navbar-toggler2"),
            dbc.Collapse(
                dbc.Nav(
                    [nav_item_home], className="ml-auto", navbar=True
                ),
                id="navbar-collapse2",
                navbar=True,
            ),
        ], fluid=True
    ),
    color="#CACF85",
    dark=True,
    className="mb-3",
)

############################################Title##########################################################
content = html.Div(id="page-content")

app.layout = html.Div(
    [dcc.Location(id="url"), logo, content]
)

@app.callback(Output("page-content", "children"), [Input("url", "pathname")])
def render(pathname):
    if pathname == "/" or pathname == "/home":
        return home.layout
    return dbc.Jumbotron(
        [
            html.H1("Error 404: Page not found", className="text-danger"),
            html.Hr(),
            html.P(f"The page {pathname} was not fount...")
        ]
    )


if __name__ == '__main__':
    app.run_server(debug=True)