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
df_variantes = pd.read_csv('datasets/data.csv')
df_global_daily = pd.read_csv('datasets/worldometer_coronavirus_daily_data.csv')
df_global_summary = pd.read_csv('datasets/worldometer_coronavirus_summary_data.csv')


df_variantes= df_variantes.drop(columns=['source','number_sequenced','percent_cases_sequenced', 'valid_denominator',
       'number_sequenced_known_variant'])
df_variantes = df_variantes.astype({"variant": str}, errors='raise') 

Variant_Codes=['B.1.617.2','B.1.1.7','B.1.351','B.1.1.529','P.1','B.1.1.7+E484K','UNK','B.1.525','B.1.617.1','B.1.621','B.1.616',
               'C.37','B.1.620','B.1.617.3','B.1.427/B.1.429','P.3','AT.1','C.1.2','B.1.640','B.1.526','SGTF']
Variant_Name=['Delta','Alpha','Beta','Omicron','Gama','Alpha W/Mutations','Unknown','Eta','Kappa','Mu','Nameless_1','Lambda','Nameless_2',
              'Nameless_3','Epsilon','Nameless_4','Theta','Nameless_5','IHV','Iota','Nameless_6']    

df_variantes['variant']=df_variantes['variant'].replace(Variant_Codes, Variant_Name)           

def choropleth():
    fig = px.choropleth(df_variantes, 
              locations = 'country',
              hover_name='country',
              hover_data=['variant'],
              color=np.log10(df_variantes["number_detections_variant"]), 
              animation_frame="year_week",
              color_continuous_scale="YlOrRd",
              locationmode='country names',
              scope="europe",
              title='Covid-19',
              height=600
             )
    return fig

def scattergeo():
    fig2 = px.scatter_geo(df_variantes, locations='country', hover_name='country', color="variant", 
                    size='new_cases',
                animation_frame="year_week", projection="natural earth", scope='europe')
    fig2.update_layout(
            title = 'COVID<br>Variants',
            geo_scope='europe',
        )
    return fig2




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