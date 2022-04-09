import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objects as go
import pandas as pd
import plotly.express as px
import numpy as np

# Connect to main app.py file
from app import app, server


# Datasets
df_vacinas = pd.read_csv('datasets/country_vaccinations.csv')
df_variants = pd.read_csv('datasets/data.csv')
df_global_daily = pd.read_csv('datasets/worldometer_coronavirus_daily_data.csv')
df_global_summary = pd.read_csv('datasets/worldometer_coronavirus_summary_data.csv')


df_vacinas=df_vacinas.drop(columns=['source_name','source_website'])
df_vacinas=df_vacinas.dropna()

df_Portugal = df_vacinas.loc[df_vacinas["country"] == 'Portugal']
df_Portugal.tail()


def scatter_geo():
    figVacines1 = px.scatter_geo(df_vacinas, locations='iso_code', hover_name='country', color=df_vacinas["daily_vaccinations"], 
                size=df_vacinas["daily_vaccinations"],animation_frame="date", projection="natural earth", title = 'Daily Vaccinations')
    return figVacines1


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
                        dcc.Graph(figure=scatter_geo()), body=True, color=colors["nav"]
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