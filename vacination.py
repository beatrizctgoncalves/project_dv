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

def vacionation_per_100():
    my_raceplot = barplot(df_2122,  item_column='location', value_column='total_vaccinations_per_hundred', time_column='date', top_entries=10)
    my_raceplot.plot(item_label = 'Top Country', value_label = 'Vaccinations per 100 people', frame_duration = 600)


df_vac = df[df['population'].notna() & df['people_vaccinated'].notna() & df['people_fully_vaccinated'].notna()]
df_vac = df_vac.groupby('location').agg({'people_vaccinated': 'max', 'people_fully_vaccinated': 'max', 'population':'max'}).reset_index()
df_vac[['population', 'people_vaccinated', 'people_fully_vaccinated']] = df_vac[['population', 'people_vaccinated', 'people_fully_vaccinated']].astype(int)

continents = list(df['continent'].unique())
continents.append('World')
continents.append('Upper middle income')
continents.append('Lower middle income')
continents.append('Wallis and Futuna')
continents.append('High income')
continents.append('European Union')

df_vac = df_vac[~df_vac['location'].isin(continents)]
df_vac = df_vac.sort_values(by=['people_fully_vaccinated', 'people_vaccinated'], ascending=False).reset_index(drop=True)

df['date'] = pd.to_datetime(df['date'])
df = df[df['date'].notna()]

def total_vacination():
    fig = go.Figure()
    fig.add_trace(go.Bar(
        y=df_vac['location'],
        x=df_vac['people_fully_vaccinated'],
        name='Fully vaccinated',
        orientation='h',
        marker=dict(
            color='rgba(246, 78, 139, 0.6)',
            line=dict(color='rgba(246, 78, 139, 1.0)', width=1.5)
        )
    ))
    fig.add_trace(go.Bar(
        y=df_vac['location'],
        x=df_vac['people_fully_vaccinated'],
        name='Has at least 1 dose',
        orientation='h',
        marker=dict(
            color='rgba(58, 71, 80, 0.6)',
            line=dict(color='rgba(58, 71, 80, 1.0)', width=1.5)
        )
    ))
    fig.update_layout(barmode='stack')
    return fig


colors = {
    'background': '#F6F5F3',
    'text': '#4B5B81',
    'nav': '#283044'
}

content = html.Div(id="page-content")

layout = dbc.Container([
            dbc.Row([
                dbc.Col([
                    html.H1('Covid-19 Vacinations', style={'textAlign': 'center', 'color': colors["nav"]})
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
                    html.H3('New Covid-19 Deaths', style={'textAlign': 'center', 'color': colors["text"]}),
                    dbc.Card(
                        dcc.Graph(figure=vacionation_per_100()), body=True
                    )
                ], width=6)
            ], align='justify'),
            dbc.Row([
                dbc.Col([
                    html.H3('New Covid-19 Deaths', style={'textAlign': 'center', 'color': colors["text"]}),
                    dbc.Card(
                        dcc.Graph(figure=total_vacination()), body=True
                    )
                ], width=6)
            ], align='justify'),
            html.Br(),html.Br(),

            # Footer
            dbc.Row([
                dbc.Col([
                    html.A('Dataset', href=" https://github.com/owid/covid-19-data/tree/master/public/data#%EF%B8%8F-download-our-complete-covid-19-dataset--csv--xlsx--json",
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