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


colors = {
    'background': '#F6F5F3',
    'text': '#4B5B81',
    'nav': '#283044'
}

# Interactive Components
def total_deaths():
    df_tmp = df[df['total_cases'].notna() & df['total_deaths'].notna()]
    
    fig = px.sunburst(df_tmp, path=['continent', 'location'], values='total_cases',
        color='total_deaths', hover_data=['iso_code'],
        color_continuous_scale='amp',
        color_continuous_midpoint=np.average(df_tmp['total_deaths'], weights=df_tmp['total_cases']))

    return fig

def new_deaths():
    fig = px.line(df, x="date", y="new_deaths", color='continent')
    return fig


def total_cases():
    fig = px.choropleth(df, 
              locations = 'iso_code',
              hover_name='location',
              #hover_data=['variant'],
              color="total_cases", 
              animation_frame="date",
              color_continuous_scale="YlOrRd",
              #locationmode='country names',
              #scope="europe",
              title='Cases of Covid-19',
              projection="natural earth",
              height=700)
    return fig

def new_cases():
    fig = px.line(df, x="date", y="new_cases", color='continent')
    return fig


cases_vs_deaths = dcc.Tabs([
        dcc.Tab(label='Cases', children=[
            html.Br(),html.Br(),
            dbc.Row([            
                dbc.Col([
                    html.H3('New Cases per million', style={'textAlign': 'center', 'color': colors["text"]}),
                    dcc.Graph(
                        figure = px.choropleth(df, 
                            locations = 'iso_code',
                            hover_name='location',
                            #hover_data=['variant'],
                            color="new_cases_per_million", 
                            animation_frame="date",
                            color_continuous_scale="YlOrRd",
                            #locationmode='country names',
                            #scope="europe",
                            projection="natural earth",
                            height=700)
                    )
                ])
            ]),
            html.Br(),html.Br(),
            dbc.Row([            
                dbc.Col([
                    html.H3('Total Covid-19 Cases', style={'textAlign': 'center', 'color': colors["text"]}),
                    dbc.Card(
                        dcc.Graph(figure=total_cases()), body=True
                    )
                ], width=6),
                
                dbc.Col([
                    html.H3('New Covid-19 Cases', style={'textAlign': 'center', 'color': colors["text"]}),
                    dbc.Card(
                        dcc.Graph(figure=new_cases()), body=True
                    )
                ], width=6),
            ]),
        ]),
        dcc.Tab(label='Deaths', children=[
            html.Br(),html.Br(),
            dbc.Row([            
                dbc.Col([
                    html.H3('New Deaths per million', style={'textAlign': 'center', 'color': colors["text"]}),
                    dcc.Graph(
                        figure = px.choropleth(df, 
                            locations = 'iso_code',
                            hover_name='location',
                            #hover_data=['variant'],
                            color="new_deaths_per_million", 
                            animation_frame="date",
                            color_continuous_scale="YlOrRd",
                            #locationmode='country names',
                            #scope="europe",
                            projection="natural earth",
                            height=700)
                    ),
                ])
            ]),
            html.Br(),html.Br(),
            dbc.Row([            
                dbc.Col([
                    html.H3('Total Covid-19 Deaths', style={'textAlign': 'center', 'color': colors["text"]}),
                    dbc.Card(
                        dcc.Graph(figure=total_deaths()), body=True
                    )
                ], width=6),
                
                dbc.Col([
                    html.H3('New Covid-19 Deaths', style={'textAlign': 'center', 'color': colors["text"]}),
                    dbc.Card(
                        dcc.Graph(figure=new_deaths()), body=True
                    )
                ], width=6),
            ])
        ])
])


# Layout
content = html.Div(id="page-content")

layout = dbc.Container([
            dbc.Row([
                dbc.Col([
                    html.H1('Confirmed cases and deaths', style={'textAlign': 'center', 'color': colors["nav"]})
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
                    cases_vs_deaths
                ], width=12)
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