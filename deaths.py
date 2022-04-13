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


# Interactive Components
def total_deaths():
    df_tmp = df[df['total_cases'].notna() & df['total_deaths'].notna()]
    
    fig = px.sunburst(df_tmp, path=['continent', 'location'], values='total_cases',
        color='total_deaths', hover_data=['iso_code'],
        color_continuous_scale='amp',
        color_continuous_midpoint=np.average(df_tmp['total_deaths'], weights=df_tmp['total_cases']))

    return fig

cases_vs_deaths = dcc.Tabs([
        dcc.Tab(label='New Cases per million', children=[
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
        ]),
        dcc.Tab(label='New Deaths per million', children=[
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
            )
        ]),
])

def new_deaths():
    fig = px.line(df, x="date", y="new_cases", color='continent')
    return fig

continent_options = [dict(label=continent, value=continent) for continent in df['continent'].unique()]

dropdown_continent = dcc.Dropdown(
        id='continent_drop',
        options=continent_options,
        value=['Europe'],
        multi=True
    )

@app.callback(
    Output('dd-output-container', 'children'),
    Input('demo-dropdown', 'value')
)
def update_new_deaths(value):
    fig = px.line(df.query('continent=="'+value+'"'), x="date", y="new_cases", color='country')
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

            dbc.Row([            
                dbc.Col([
                    html.H3('Total Covid-19 deaths in the world', style={'textAlign': 'center', 'color': colors["text"]}),
                    dbc.Card(
                        dcc.Graph(figure=total_deaths()), body=True
                    )
                ], width=6),
                
                dbc.Col([
                    html.H3('Continent Choice'),
                    dropdown_continent,
                    html.Div(id='dropdown_country_container'),
                    html.Br(), html.Br(),
                    html.H3('New Covid-19 deaths in the world by continent', style={'textAlign': 'center', 'color': colors["text"]}),
                    dbc.Card(
                        dcc.Graph(figure=new_deaths()), body=True
                    )
                ], width=6),
            ]),
            html.Br(),html.Br(),

            dbc.Row([
                
            ]),
            dbc.Row([
                dbc.Col([
                    
                ], width=6)
            ]),

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