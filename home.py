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


# Datasets

def choropleth():
    '''fig = go.Figure(data=go.Choropleth(
        locations=df_global_summary['country'], # Spatial coordinates
        z = df_global_summary['total_confirmed'].astype(float), # Data to be color-coded
        locationmode = 'country names', # set of locations match entries in `locations`
        colorscale = 'Reds',
        colorbar_title = "Total Cases",
    ))
    fig.update_layout(
        geo_scope='world', # limite map scope to USA
    )
    return fig'''


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
                    html.H5('The COVID-19 virus, name given by the World Health Organisation to the '
                    'disease caused by the new coronavirus SARS-COV-2, can cause severe respiratory '
                    'infections, such as pneumonia. This virus was first identified in humans in late '
                    '2019 in the Chinese city of Wuhan, Hubei province, and cases have been confirmed '
                    'in other countries.', style={'textAlign': 'justify', 'paddingLeft': '20px', 'paddingRight': '20px',
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
                    html.H3('Covid-19 Cases in the World ', style={'paddingTop': '20px', 'textAlign': 'center', 'color': colors["text"]})
                ], width=12),
            ]),
            dbc.Row([
                dbc.Col([
                    dbc.Card(
                        dcc.Graph(figure=choropleth()), body=True, color=colors["nav"]
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
                    html.H6('Group: Beatriz Gonçalves - m20210695, Gonçalo Lopes - m20210679, Guilherme Simões - m2021, '
                    'João Veloso - m20210696', style={'textAlign': 'center'})
                ], width=12)
            ], style={'paddingTop': '30px', 'paddingBottom': '30px'}),
    ], fluid=True)


if __name__ == "__main__":
    app.run_server(debug=True)