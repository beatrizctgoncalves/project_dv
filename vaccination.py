import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objects as go
import pandas as pd
import plotly.express as px
import numpy as np
from raceplotly.plots import barplot

# Connect to main app.py file
from app import app, server, df

mask = (df['date'] > '2021-01-01') & (df['date'] <= '2022-04-10')
df_2122 = df.loc[mask]

def vaccionation_per_100():
    my_raceplot = barplot(df_2122,  item_column='location', value_column='total_vaccinations_per_hundred', time_column='date', top_entries=10)
    my_raceplot.plot(item_label = 'Top Country', value_label = 'Vaccinations per 100 people', frame_duration = 600)
    return my_raceplot.fig


colors = {
    'background': '#F6F5F3',
    'text': '#4B5B81',
    'nav': '#283044'
}

content = html.Div(id="page-content")

layout = dbc.Container([
            dbc.Row([
                dbc.Col([
                    html.H1('Covid-19 Vaccinations', style={'textAlign': 'center', 'color': colors["nav"]})
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
                    html.H3('Vaccinations per 100 people', style={'textAlign': 'center', 'color': colors["text"]}),
                    dbc.Card(
                        dcc.Graph(figure=vaccionation_per_100()), body=True
                    )
                ], width=12)
            ], align='justify'),
            html.Br(),html.Br(),

            dbc.Row([
                dbc.Col([
                    html.H3('QUALQUER COISA', style={'textAlign': 'center', 'color': colors["text"]}),
                    dbc.Card(
                        #dcc.Graph(figure=total_vacination()), body=True
                    )
                ], width=12)
            ], align='justify'),
            html.Br(),html.Br(),

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