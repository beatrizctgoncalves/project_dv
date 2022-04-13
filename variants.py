import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objects as go
import pandas as pd
import plotly.express as px
import numpy as np

# Connect to main app.py file
from app import app, server, df


def choropleth():
    return 0

def scattergeo():
    return 0




colors = {
    'background': '#F6F5F3',
    'text': '#4B5B81',
    'nav': '#283044'
}

content = html.Div(id="page-content")

layout = dbc.Container([
            dbc.Row([
                dbc.Col([
                    html.H1('Covid-19', style={'textAlign': 'center', 'color': colors["nav"]})
                ], width=12)
            ]),
            dbc.Row([
                dbc.Col([
                    html.H5('',
                    style={'textAlign': 'justify', 'paddingLeft': '20px', 'paddingRight': '20px',
                    'paddingTop': '20px'})
                ], width=12)
            ], align='justify'),
            dbc.Row([
                dbc.Col([
                    html.H5('More about covid...', style={'textAlign': 'justify', 'paddingLeft': '20px', 'paddingRight': '20px'})
                ], width=12)
            ]),
            dbc.Row([
                dbc.Col([
                    html.H3('Covid-19 Cases in the World ', style={'textAlign': 'center', 'color': colors["text"]})
                ], width=12),
            ]),
            dbc.Row([
                dbc.Col([
                    dbc.Card(
                        dcc.Graph(figure=choropleth()), body=True, color=colors["nav"]
                    )
                ], width=12)
            ]),
            dbc.Row([
                dbc.Col([
                    dbc.Card(
                        dcc.Graph(figure=scattergeo()), body=True, color=colors["nav"]
                    )
                ], width=12)
            ]),

            # Footer
            dbc.Row([
                dbc.Col([
                    html.H6('Datasets: link', style={'textAlign': 'center'})
                ], width=12),
                html.Br(),
                dbc.Col([
                    html.H6('Group: Beatriz Gonçalves - m20210695, Gonçalo Lopes - m2021, Guilherme Simões - m2021, '
                    'João Veloso - m20210696', style={'textAlign': 'center'})
                ], width=12)
            ], style={'paddingTop': '30px', 'paddingBottom': '30px'}),
    ], fluid=True)


if __name__ == "__main__":
    app.run_server(debug=True)