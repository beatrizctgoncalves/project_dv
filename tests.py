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
import gmaps.geojson_geometries

# Connect to main app.py file
from app import app, server, df


colors = {
    'background': '#F6F5F3',
    'text': '#4B5B81',
    'nav': '#283044'
}

df_tests = df.dropna(subset=['positive_rate','tests_per_case','total_tests_per_thousand', 'total_cases'])
df_tests.sort_values(by = ['total_tests'], ascending=False, inplace=True)
df_tests.reset_index(drop=True, inplace=True)
df_table = df_tests.groupby(['continent', 'location']).agg({'total_tests_per_thousand': 'mean', 'positive_rate': 'mean', 'total_cases':'mean', 'tests_per_case':'mean', 'population':'mean'}).reset_index()
df_show = df_tests.groupby(['date', 'continent', 'location']).agg({'total_tests_per_thousand': 'mean', 'positive_rate': 'mean', 'total_cases':'mean', 'tests_per_case':'mean', 'population':'mean'}).reset_index()

# Interactive Components
def total_tests():
    rowEvenColor = 'lightgrey'
    rowOddColor = 'white'

    fig = go.Figure(data=[go.Table(
        header=dict(values=list(['<br>Country', '<br>Total tests per 1000', 'Positives rate<br>       (%)', '<br>Total number of cases', '<br>Tests per case', '<br>Population size']),
                    line_color='darkslategray',
                    fill_color='royalblue',
                    align=['left','center','center','center','center','center'],
                    font=dict(color='white', size=14),
                    height=20,
                    ),
        cells=dict(values=[df_table.location, round(df_table.total_tests_per_thousand), (round(df_table.positive_rate * 100)), round(df_table.total_cases), round(df_table.tests_per_case), round(df_table.population)],
                line_color='darkslategray',
                fill_color = [[rowOddColor,rowEvenColor,rowOddColor, rowEvenColor,rowOddColor, rowEvenColor]*100],
                font=dict(color='black', size=11),
                align=['left','center'])
        )])        
    fig.update_layout(
        showlegend=False,
    )
    return fig

def tests_per_thousand():
    df_bar = df_tests.groupby(['date', 'continent']).agg({'total_tests_per_thousand': 'mean', 'positive_rate': 'mean', 'total_cases':'mean', 'tests_per_case':'mean', 'population':'mean'}).reset_index()
    fig = px.bar(df_bar, x='date', y='total_tests_per_thousand',
             hover_data=['total_tests_per_thousand', 'positive_rate'], color='continent',
             height=500)
    return fig

def gmaps_graph():
    '''gmaps.configure(api_key='AIzaSyAIAYSB9Ipt02TQVMQQctAOwwqGZm0BYrg')
    countries_geojson = gmaps.geojson_geometries.load_geometry('countries')
    fig = gmaps.figure()
    gini_layer = gmaps.geojson_layer(countries_geojson)
    fig.add_layer(gini_layer)
    '''
    return 0



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
                    html.H3('Data on Testing for Covid-19 in all', style={'textAlign': 'center', 'color': colors["text"]}),
                    dbc.Card(
                        dcc.Graph(figure=total_tests()), body=True
                    )
                ], width=12),
            ]),
            html.Br(),html.Br(),
            dbc.Row([
                dbc.Col([
                    html.H3('Tests for Covid-19 per thousand', style={'textAlign': 'center', 'color': colors["text"]}),
                    dbc.Card(
                        dcc.Graph(figure=tests_per_thousand()), body=True
                    )
                ], width=12)
            ]),
            html.Br(),html.Br(),
            dbc.Row([
                dbc.Col([
                    html.H3('Tests for Covid-19 per thousand', style={'textAlign': 'center', 'color': colors["text"]}),
                    dbc.Card(
                        dcc.Graph(figure=gmaps_graph()), body=True
                    )
                ], width=12)
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