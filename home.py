import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html
from dash.dependencies import Input, Output

# Connect to main app.py file
from app import app, server


CONTENT_STYLE = {
    "margin-left": "18rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem",
}


content = html.Div(id="page-content")

app.layout = html.Div(
    html.H1('Covid-19')
)



if __name__ == "__main__":
    app.run_server(debug=True)