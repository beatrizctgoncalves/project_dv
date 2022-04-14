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
from app import df
import app

country_options = [dict(label=country, value=country) for country in df['location'].unique()]
dropdown_country = dcc.Dropdown(
        id='country_drop',
        options=country_options,
        value=['Portugal'],
        multi=True
    )

vaccination_names = ['Total Vaccinations', 'People Vaccinated', 'People Fully Vaccinated', 'People Vaccinated Per Hundred', 'People Fully Vaccinated_per_hundred']
vaccination_options = [dict(label=vac.replace('_', ' '), value=vac) for vac in vaccination_names]
dropdown_vaccination = dcc.Dropdown(
        id='vaccination_option',
        options=vaccination_options,
        value='Total_Vaccinations',
    )

radio_lin_log = dcc.RadioItems(
        id='lin_log',
        options=[dict(label='Linear', value=0), dict(label='Log', value=1)],
        value=0,
        style={'textAlign': 'center'}
    )


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
                    html.H5('Country Choice', style={'textAlign': 'center', 'color': colors["text"]}),
                    dropdown_country,
                ], width=6),
                dbc.Col([
                    html.H5('Vaccination Choice', style={'textAlign': 'center', 'color': colors["text"]}),
                    dropdown_vaccination,
                    html.Br(),
                    html.H5('Linear or Log?', style={'textAlign': 'center', 'color': colors["text"]}),
                    radio_lin_log
                ], width=6)
            ], align='center'),
            html.Br(),

            dbc.Row([
                dbc.Col([
                    dbc.Card(
                        dcc.Graph(id='bar_graph'), body=True
                    )
                ], width=12)
            ], align='center'),
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


@app.app.callback(
    Output("bar_graph", "figure"),
    [Input("country_drop", "value"), Input("vaccination_option", "value"), Input("lin_log", "value")]
)
def plots(countries, vaccination, scale):
    data_bar = []

    for country in countries:
        df_bar = df.loc[(df['location'] == country)]
        x_bar = df_bar['date']
        y_bar = df_bar[vaccination]
        data_bar.append(dict(type='bar', x=x_bar, y=y_bar, name=country))

    layout_bar = dict(title=dict(text='Total Vaccination from 2020 until 2022'),
                  yaxis=dict(title='Vaccination', type=['linear', 'log'][scale]),
                  paper_bgcolor='#f9f9f9'
                  )

    return go.Figure(data=data_bar, layout=layout_bar)


if __name__ == "__main__":
    app.run_server(debug=True)