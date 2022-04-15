from turtle import bgcolor
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
from matplotlib import animation
import numpy as np
import pandas as pd
import plotly.graph_objs as go
import pandas as pd
import plotly.express as px
import numpy as np
from raceplotly.plots import barplot
from datetime import date


# Datasets
df = pd.read_csv('datasets/owid-covid-data.csv')
df = df.dropna(how='all')
df = df[df['continent'].notna()]

# To be responsive
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

server = app.server

app.config.suppress_callback_exceptions = True
app.title = 'Covid-19'

colors = {
    'background': '#F6F5F3',
    'nav': '#283044',
    'text': '#fff'
}

COVID_LOGO = "assets/favicon.ico"

# Interactive Components
# Deaths
def total_deaths():
    df_tmp = df[df['total_cases'].notna() & df['total_deaths'].notna()]
    
    fig = px.sunburst(df_tmp, path=['continent', 'location'], values='total_cases',
        color='total_deaths', hover_data=['iso_code'],
        color_continuous_scale='amp',
        color_continuous_midpoint=np.average(df_tmp['total_deaths'], weights=df_tmp['total_cases']))

    return fig

# Tests
def total_tests():
    df_tests = df.dropna(subset=['positive_rate','tests_per_case','total_tests_per_thousand', 'total_cases'])
    df_tests.sort_values(by = ['total_tests'], ascending=False, inplace=True)
    df_tests.reset_index(drop=True, inplace=True)
    df_table = df_tests.groupby(['continent', 'location']).agg({'total_tests_per_thousand': 'mean', 'positive_rate': 'mean', 'total_cases':'mean', 'tests_per_case':'mean', 'population':'mean'}).reset_index()
    df_show = df_tests.groupby(['date', 'continent', 'location']).agg({'total_tests_per_thousand': 'mean', 'positive_rate': 'mean', 'total_cases':'mean', 'tests_per_case':'mean', 'population':'mean'}).reset_index()
    
    rowEvenColor = 'lightgrey'
    rowOddColor = 'white'

    fig = go.Figure(data=[go.Table(
        header=dict(values=list(['<br>Country', '<br>Total tests per 1000', 'Positives rate<br>       (%)', '<br>Total number of cases', '<br>Tests per case', '<br>Population size']),
                    line_color='darkslategray',
                    fill_color='grey',
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

# Vaccination
def vac_graph():
    mask = (df['date'] > '2021-01-01') & (df['date'] <= '2022-04-10')
    df_2122 = df.loc[mask]
    my_raceplot = barplot(df_2122, item_column='location', value_column='total_vaccinations_per_hundred', time_column='date', top_entries=10)
    my_raceplot.plot(item_label = 'Top Country', value_label = 'Vaccinations per 100 people', frame_duration = 600)
    return my_raceplot.fig


# Cases
continent_options = [dict(label=continent, value=continent) for continent in df['continent'].unique()]
country_options = [dict(label=country, value=country) for country in df['location'].unique()]
dropdown_continent_cases = dcc.Dropdown(
        id='continent_drop_cases',
        options=continent_options,
        value=['Asia'],
        multi=True,
        persistence=True,
        persistence_type='session'
    )

dropdown_country_cases = dcc.Dropdown(
    id='country_drop_cases',
    options=country_options,
    value=['Portugal'],
    multi=True
)

continent_options2 = [dict(label=continent, value=continent) for continent in df['continent'].unique()]
continent_options2.append({'label': 'World', 'value': 'World'})
continent_options2.remove({'label': 'Oceania', 'value': 'Oceania'})
dropdown_scope = dcc.Dropdown(
        id='scope_continent',
        options=continent_options2,
        value='world',
        persistence=True,
        persistence_type='session'
    )

checklist_lin_log_cases = dbc.Checklist(
        id='lin_log_cases',
        options=[dict(label='Linear', value=0)],
        value=[0],
        switch=True,
        style={'textAlign': 'center', 'color': '#fff'}
    )

checklist_projection = dbc.Checklist(
        id='projection',
        options=[dict(label='Equirectangular', value=0)],
        value=[0],
        switch=True,
        style={'textAlign': 'center', 'color': '#fff'}
    )


# Deaths
country_options = [dict(label=country, value=country) for country in df['location'].unique()]
dropdown_country_deaths = dcc.Dropdown(
        id='country_drop_deaths',
        options=country_options,
        value=['Portugal', 'France', 'Italy', 'Spain'],
        multi=True
    )

checklist_lin_log_deaths = dbc.Checklist(
        id='lin_log_deaths',
        options=[dict(label='Linear', value=0)],
        value=[0],
        switch=True,
        style={'textAlign': 'center', 'color': '#fff'}
    ) 

deaths_options_names = ['new_deaths_per_million', 'new_deaths_smoothed_per_million']
deaths_options = [dict(label=deaths.replace('_', ' '), value=deaths) for deaths in deaths_options_names]
dropdown_deaths = dcc.Dropdown(
        id='deaths_option',
        options=deaths_options,
        value='new_deaths_per_million',
    )

dropdown_scope2 = dcc.Dropdown(
        id='scope_continent2',
        options=continent_options2,
        value='world'
    )

checklist_projection2 = dbc.Checklist(
        id='projection2',
        options=[dict(label='Equirectangular', value=0)],
        value=[0],
        switch=True,
        style={'textAlign': 'center', 'color': '#fff'}
    )


# Tests
dropdown_continent_tests = dcc.Dropdown(
        id='continent_drop_tests',
        options=continent_options,
        value=['Europe', 'Asia', 'Africa'],
        multi=True
    )

tests_options_names = ['total_tests_per_thousand', 'new_tests_per_thousand',
       'new_tests_smoothed', 'new_tests_smoothed_per_thousand', 'positive_rate', 'tests_per_case', 'tests_units']
tests_options = [dict(label=tests.replace('_', ' '), value=tests) for tests in tests_options_names]
dropdown_tests = dcc.Dropdown(
        id='tests_option',
        options=tests_options,
        value='total_tests_per_thousand'
    )
    

# Vaccinations
country_options = [dict(label=country, value=country) for country in df['location'].unique()]
dropdown_country = dcc.Dropdown(
        id='country_drop',
        options=country_options,
        value=['Portugal', 'France', 'Italy'],
        multi=True,
        placeholder='Select Countries'
    )

vaccination_names = ['total_vaccinations', 'people_vaccinated', 'people_fully_vaccinated', 'people_vaccinated_per_hundred', 'people_fully_vaccinated_per_hundred']
vaccination_options = [dict(label=vac.replace('_', ' '), value=vac) for vac in vaccination_names]
dropdown_vaccination = dcc.Dropdown(
        id='vaccination_option',
        options=vaccination_options,
        value='total_vaccinations',
    )

radio_lin_log_vac = dcc.RadioItems(
        id='lin_log_vac',
        options=[dict(label='Linear', value=0), dict(label='Log', value=1)],
        value=0,
        style={'textAlign': 'center'}
    )


# Graphics
graph_names = ['chart', 'map', 'scatter']
graph_options = [dict(label=vac.replace('_', ' '), value=vac) for vac in vaccination_names]
dropdown_graph = dcc.Dropdown(
        id='graph_option',
        options=vaccination_options,
        value='total_vaccinations',
    )


# Components
choose_tab = dcc.Tabs([
        dcc.Tab(label='Cases', children=[
            html.Br(),html.Br(),

            html.Div([
                html.Div([
                    html.Br(),
                    html.H5('Continent Choice', style={'textAlign': 'center', 'color': colors["text"]}),
                    dropdown_scope,
                    html.Br(),
                    html.H5('Which Projection?', style={'textAlign': 'center', 'color': colors["text"]}),
                    dbc.Row([
                        html.P('Orthographic', style={'paddingRight': '5px', 'color': '#fff'}),
                        checklist_projection
                    ], style={'alignItems': 'center'})#TODO
                ], style={'width': '30%'}, className='slicerblue'),
            
                html.Div([
                    dcc.Graph(id='total_cases_graph')
                ], style={'width': '70%'}, className='graphblue')
            ], style={'display': 'flex'}),

            html.Div([
                html.Div([
                    dcc.Graph(id='new_cases_graph')
                ], style={'width': '70%'}, className='graphblue'),
                html.Div([
                    html.Br(),
                    html.H5('Country Choice', style={'textAlign': 'center', 'color': colors["text"]}),
                    dropdown_country_cases,
                    html.Br(),
                    dbc.Row([
                        html.P('Log', style={'paddingRight': '5px', 'color': '#fff', 'textAlign': 'center'}),
                        checklist_lin_log_cases
                    ], style={'alignItems': 'center'})
                ], style={'width': '30%'}, className='slicerblue')
            ], style={'display': 'flex'}),
        ]),
        dcc.Tab(label='Deaths', children=[
            html.Br(),html.Br(),
            dbc.Row([
                dbc.Col([
                    html.H1('Confirmed Deaths', style={'textAlign': 'center', 'color': colors["nav"]})
                ], width=12)
            ]),
            dbc.Row([
                dbc.Col([
                    html.H5('This section visualises the covid-19 deaths between 2020 and 2022.', style={'textAlign': 'center', 'paddingLeft': '20px', 'paddingRight': '20px',
                    'paddingTop': '20px'})
                ], width=12)
            ], align='center'),
            html.Br(),html.Br(),

            dbc.Row([            
                dbc.Col([
                    html.H3('Total Covid-19 Deaths', style={'textAlign': 'center', 'color': colors["text"]}),
                    html.Br(),html.Br(),
                    dcc.Tabs([
                        dcc.Tab(label='World Map', children=[
                            html.Br(),
                            html.H5('Which Projection?', style={'textAlign': 'center', 'color': colors["text"]}),
                            dbc.Row([
                                html.P('Orthographic', style={'paddingRight': '5px', 'color': '#fff'}),
                                checklist_projection2
                            ], style={'alignItems': 'center'}),
                            html.Br(),
                            html.H5('Continent Choice', style={'textAlign': 'center', 'color': colors["text"]}),
                            dropdown_scope2,
                            html.Br(),
                            html.H3('Total Covid-19 Deaths', style={'textAlign': 'center', 'color': colors["text"]}),
                            dbc.Card(
                                dcc.Graph(id='total_deaths_graph'), body=True
                            )
                        ]),
                        dcc.Tab(label='Pie Chart', children=[
                            dbc.Card(
                                dcc.Graph(figure=total_deaths()), body=True
                            )
                        ])
                    ])
                ], width=6),
                
                dbc.Col([
                    html.H3('New Covid-19 Deaths', style={'textAlign': 'center', 'color': colors["text"]}),
                    html.H5('Country Choice', style={'textAlign': 'center', 'color': colors["text"]}),
                    dropdown_country_deaths,
                    html.Br(),
                    html.H5('Deaths Choice', style={'textAlign': 'center', 'color': colors["text"]}),
                    dropdown_deaths,
                    html.Br(),
                    html.H5('Linear or Log?', style={'textAlign': 'center', 'color': colors["text"]}),
                    dbc.Row([
                                html.P('Log', style={'paddingRight': '5px', 'color': '#fff'}),
                                checklist_lin_log_deaths
                            ], style={'alignItems': 'center'}),
                    dbc.Card(
                        dcc.Graph(id='new_deaths_graph'), body=True
                    )
                ], width=6),
            ])
        ]),
        dcc.Tab(label='Tests', children=[
            html.Br(),html.Br(),
            dbc.Row([
                dbc.Col([
                    html.H1('Tests for Covid-19', style={'textAlign': 'center', 'color': colors["nav"]})
                ], width=12)
            ]),
            dbc.Row([
                dbc.Col([
                    html.H5('This section visualises the covid-19 tests done between 2020 and 2022.', style={'textAlign': 'center', 'paddingLeft': '20px', 'paddingRight': '20px',
                    'paddingTop': '20px'})
                ], width=12)
            ], align='center'),
            html.Br(),html.Br(),

            dbc.Row([            
                dbc.Col([
                    html.H3('Data on Testing for Covid-19 in all', style={'textAlign': 'center', 'color': colors["text"]}),
                    dbc.Card(
                        dcc.Graph(figure=total_tests()), body=True
                    )
                ], width=12)
            ]),
            html.Br(),html.Br(),
            
            dbc.Row([
                dbc.Col([
                    html.H5('Test Choice', style={'textAlign': 'center', 'color': colors["text"]}),
                    dropdown_tests
                ], width=12),
            ]),
            html.Br(),
            dbc.Row([
                dbc.Col([
                    html.H3('Tests', style={'textAlign': 'center', 'color': colors["text"]}),
                    dbc.Card(
                        dcc.Graph(id='tests_graph'), body=True
                    )
                ], width=12),
            ])
        ]),
        dcc.Tab(label='Vaccinations', children=[
            html.Br(),html.Br(),
            dbc.Row([
                dbc.Col([
                    html.H1('Vaccinations', style={'textAlign': 'center', 'color': colors["nav"]})
                ], width=12)
            ]),
            dbc.Row([
                dbc.Col([
                    html.H5('This section shows the covid-19 vaccinations between 2020 and 2022.', style={'textAlign': 'center', 'paddingLeft': '20px', 'paddingRight': '20px',
                    'paddingTop': '20px'})
                ], width=12)
            ], align='center'),
            html.Br(),html.Br(),

            dbc.Row([
                dbc.Col([
                    html.Br(),
                    dbc.Card(
                        dcc.Graph(figure=vac_graph()), body=True
                    )
                ], width=12)
            ], align='center'),
            html.Br(),html.Br(),

            dbc.Row([
                dbc.Col([
                    html.H5('Country Choice', style={'textAlign': 'center', 'color': colors["text"]}),
                    dropdown_country,
                ], width=6),
                dbc.Col([
                    html.H5('Vaccination Choice', style={'textAlign': 'center', 'color': colors["text"]}),
                    dropdown_vaccination
                ], width=6)
            ], align='center'),
            html.Br(),

            dbc.Row([
                dbc.Col([
                    html.Br(),
                    html.H5('Linear or Log?', style={'textAlign': 'center', 'color': colors["text"]}),
                    radio_lin_log_vac,
                    html.Br(),
                    dbc.Card(
                        dcc.Graph(id='scatter_graph'), body=True
                    )
                ], width=12)
            ], align='center')
        ])
], className='classTabs')

# Navbar
nav_home = dbc.NavItem(dbc.NavLink("Informations about Covid-19", href="/", active="exact"))

# Layout
content = html.Div(id="page-content")

app.layout = html.Div([
    dbc.Navbar(
        dbc.Container([
            html.A(
                dbc.Row(
                    [
                        dbc.Col(html.Img(src=COVID_LOGO, height="80px", className="ml-2")),
                    ],
                    align="center"
                ),
                href="/",
            ),
            dbc.NavbarToggler(id="navbar-toggler2"),
            dbc.Collapse(
                dbc.Nav(
                    [nav_home], className="ml-auto", navbar=True
                ),
                id="navbar-collapse2",
                navbar=True
            ),
        ], fluid=True),
        color=colors["nav"],
        dark=True,
        className="mb-3",
    ),
    dbc.Container([
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
        html.Br(),

        dbc.Row([
            dbc.Col([
                choose_tab
            ], width=12)
        ], align='justify', style={'backgroundColor': '#fff'}),
        html.Br(),html.Br(),

        # Footer
        dbc.Row([
            dbc.Col([
                html.A('Dataset', href="https://github.com/owid/covid-19-data/tree/master/public/data#%EF%B8%8F-download-our-complete-covid-19-dataset--csv--xlsx--json",
                style={'fontWeight': 'bold', 'color': 'grey'})
            ], width=12, style={'textAlign': 'center'}),
            html.Br(),
            dbc.Col([
                html.A('Group: Beatriz Gonçalves - m20210695, Gonçalo Lopes - m20210679, Guilherme Simões - m2021, '
                'João Veloso - m20210696', style={'fontWeight': 'bold', 'color': 'grey'})
            ], width=12, style={'textAlign': 'center'}),
        ], style={'paddingTop': '30px', 'paddingBottom': '30px'}),
    ], fluid=True)
], style={'backgroundColor': colors['background']})

# Navbar
@app.callback(Output("page-content", "children"), [Input("url", "pathname")])
def render(pathname):
    if pathname != "/":
        return dbc.Jumbotron(
            [
                html.H1("Error 404: Page not found", className="text-danger"),
                html.Hr(),
                html.P("The page " + pathname + " was not fount...")
            ]
        )


# Cases
@app.callback(
    Output("total_cases_graph", "figure"),
    [Input("projection", "value"), Input("scope_continent", "value")]
)
def total_cases(projection, scope):
    if len(projection):
        fig = px.choropleth(df, 
            locations = 'iso_code',
            hover_name='location',
            color="total_cases", 
            animation_frame="date",
            color_continuous_scale="YlOrRd",
            scope = scope.lower(),
            title='Total Covid-19 Cases',
            projection=['equirectangular', 'orthographic'][0],
            height=700)
    else:
        fig = px.choropleth(df, 
            locations = 'iso_code',
            hover_name='location',
            color="total_cases", 
            animation_frame="date",
            color_continuous_scale="YlOrRd",
            scope = scope.lower(),
            title='Total Covid-19 Cases',
            projection=['equirectangular', 'orthographic'][1],
            height=700)

    return fig
    

@app.callback(
    Output("new_cases_graph", "figure"),
    [Input("country_drop_cases", "value"), Input("lin_log_cases", "value")]
)
def new_cases(countries, scale):
    data_bar = []

    for country in countries:
        df_bar = df.loc[(df['location'] == country)]
        x_bar = df_bar['date']
        y_bar = df_bar['new_cases_per_million']
        data_bar.append(dict(type='scatter', x=x_bar, y=y_bar, name=country))

    layout_linear = dict(yaxis=dict(title='New Cases Per Million', type=['linear', 'log'][scale]))

    return go.Figure(data=data_bar, layout=layout_linear)


# Deaths
@app.callback(
    Output("new_deaths_graph", "figure"),
    [Input("country_drop_deaths", "value"), Input("lin_log_deaths", "value"), Input('deaths_option', "value")]
)
def new_deaths(countries, scale, death):
    data_hist = []

    for country in countries:
        df_hist = df.loc[(df['location'] == country)]
        x_hist = df_hist['date']
        y_hist = df_hist[death]
        data_hist.append(dict(type='histogram', x=x_hist, y=y_hist, name=country))

    if len(scale):
        layout_hist = dict(yaxis=dict(title=death, type=['linear', 'log'][0]))
    else:
        layout_hist = dict(yaxis=dict(title=death, type=['linear', 'log'][1]))

    return go.Figure(data=data_hist, layout=layout_hist)

@app.callback(
    Output("total_deaths_graph", "figure"),
    [Input("projection2", "value"), Input("scope_continent2", "value")]
)
def total_deaths(projection, scope):
    if len(projection):
        fig = px.choropleth(df, 
            locations = 'iso_code',
            hover_name='location',
            color="total_deaths",
            animation_frame="date",
            color_continuous_scale="amp",
            scope = scope.lower(),
            projection=['equirectangular', 'orthographic'][0],
            height=700)
    else:
        fig = px.choropleth(df, 
            locations = 'iso_code',
            hover_name='location',
            color="total_deaths",
            animation_frame="date",
            color_continuous_scale="amp",
            scope = scope.lower(),
            projection=['equirectangular', 'orthographic'][1],
            height=700)
    return fig


# Tests
@app.callback(
    Output("tests_graph", "figure"),
    [Input("tests_option", "value")]
)
def tests_plot(test):
    fig = px.bar(df, x="continent", y=test, animation_frame="date", color="continent", hover_name="location")
    return fig


# Vaccinations
@app.callback(
    Output('scatter_graph', 'figure'),
    [Input("country_drop", "value"), Input("vaccination_option", "value"), Input("lin_log_vac", "value")]
)
def plots(countries, vaccination, scale):
    data_scatter = []

    for country in countries:
        df_scatter = df.loc[(df['location'] == country)]
        x_scatter = df_scatter['date']
        y_scatter = df_scatter[vaccination]
        data_scatter.append(dict(type='scatter', x=x_scatter, y=y_scatter, name=country))

    layout_scatter = dict(yaxis=dict(title=vaccination, type=['linear', 'log'][scale]))
    return go.Figure(data=data_scatter, layout=layout_scatter)


if __name__ == '__main__':
    app.run_server(debug=True)