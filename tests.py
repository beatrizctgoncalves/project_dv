import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objects as go
import pandas as pd
import plotly.express as px
import numpy as np
import json
import gmaps
import gmaps.datasets
import folium
import branca

# Connect to main app.py file
from app import app, server, df


colors = {
    'background': '#F6F5F3',
    'text': '#4B5B81',
    'nav': '#283044'
}

# Interactive Components
def total_tests():
    url = (
        "https://raw.githubusercontent.com/python-visualization/folium/master/examples/data"
    )
    state_geo = f"{url}/world-countries.json"

    m = folium.Map(location=[0, 0], zoom_start=2)

    folium.Choropleth(
        geo_data=state_geo,
        data=df['total_tests'],
        columns=["location", "total_tests"],
        key_on="feature.id",
        fill_color="BuPu",
        fill_opacity=0.7,
        line_opacity=0.5,
        legend_name="Total Covid 19 tests",
        reset=True,
    ).add_to(m)

    return m

def tests_per_day():
    fig = px.choropleth(df, 
              locations = 'iso_code',
              hover_name='location',
              #hover_data=['variant'],
              color="new_tests_smoothed_per_thousand", 
              animation_frame="date",
              color_continuous_scale=[(0, 'rgba(255,254,230,255)'), (0.5, 'rgba(0,69,40,255)'), (1.0, 'rgb(0,0,0)')],
              #locationmode='country names',
              #scope="europe",
              title='How many tests are performed each day?.',
              projection="natural earth",
              height=700)
    return fig


# Layout
content = html.Div(id="page-content")

layout = dbc.Container([
            dbc.Row([
                dbc.Col([
                    html.H1('Testing for Covid-19', style={'textAlign': 'center', 'color': colors["nav"]})
                ], width=12)
            ]),
            dbc.Row([
                dbc.Col([
                    html.H5('Qualquer coisa.', style={'textAlign': 'justify', 'paddingLeft': '20px', 'paddingRight': '20px',
                    'paddingTop': '20px'})
                ], width=12)
            ], align='justify'),
            html.Br(),html.Br(),

            dbc.Row([            
                dbc.Col([
                    html.H3('Total Covid-19 Tests', style={'textAlign': 'center', 'color': colors["text"]}),
                    dbc.Card(
                        dcc.Graph(figure=total_tests()), body=True
                    )
                ], width=6)
            ]),
            dbc.Row([            
                dbc.Col([
                    html.H3('Total Covid-19 Tests', style={'textAlign': 'center', 'color': colors["text"]}),
                    dbc.Card(
                        dcc.Graph(figure=tests_per_day()), body=True
                    )
                ], width=6)
            ]),

            # Footer
            dbc.Row([
                dbc.Col([
                    html.A('Dataset', href="https://github.com/owid/covid-19-data/tree/master/public/data#%EF%B8%8F-download-our-complete-covid-19-dataset--csv--xlsx--json",
                    style={'fontWeight': 'bold', 'color': 'grey'})
                ], width=12, style={'textAlign': 'center'}),
                html.Br(),
                dbc.Col([
                    html.A('Group: Beatriz Gonçalves - m20210695, Gonçalo Lopes - m2021, Guilherme Simões - m2021, '
                    'João Veloso - m20210696', style={'fontWeight': 'bold', 'color': 'grey'})
                ], width=12, style={'textAlign': 'center'}),
            ], style={'paddingTop': '30px', 'paddingBottom': '30px'}),
    ], fluid=True)


if __name__ == "__main__":
    app.run_server(debug=True)