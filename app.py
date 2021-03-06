import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
import numpy as np
import pandas as pd
import plotly.graph_objs as go
import pandas as pd
import plotly.express as px
import numpy as np
from raceplotly.plots import barplot
from dash import dash_table


# Datasets
df = pd.read_csv('dataset/owid-covid-data.csv')
df = df.dropna(how='all')
df = df[df['continent'].notna()]
mask = (df['date'] > '2020-02-23') & (df['date'] <= '2022-04-12')
df = df.loc[mask]

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

# Deaths
def total_deaths():
    df_tmp = df[df['total_cases'].notna() & df['total_deaths'].notna()]
    
    fig = px.sunburst(df_tmp, path=['continent', 'location'], values='total_cases',
        color='total_deaths', hover_data=['iso_code'],
        color_continuous_scale='amp',
        color_continuous_midpoint=np.average(df_tmp['total_deaths'], weights=df_tmp['total_cases']))

    return fig

# Vaccination
def vac_graph():
    mask = (df['date'] > '2021-01-01') & (df['date'] <= '2022-04-10')
    df_2122 = df.loc[mask]
    my_raceplot = barplot(df_2122, item_column='location', value_column='total_vaccinations_per_hundred', time_column='date', top_entries=10)
    my_raceplot.plot(item_label = 'Top Country', value_label = 'Vaccinations per 100 people', frame_duration = 600)
    return my_raceplot.fig

######## Interactive Components
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
    value=['Portugal', 'France', 'United States'],
    multi=True,
    placeholder='Select a country'
)

continent_options2 = [dict(label=continent, value=continent) for continent in df['continent'].unique()]
continent_options2.append({'label': 'World', 'value': 'World'})
continent_options2.remove({'label': 'Oceania', 'value': 'Oceania'})
dropdown_scope = dcc.Dropdown(
        id='scope_continent',
        options=continent_options2,
        value='world',
        placeholder='World'
    )

radio_lin_log_cases = dbc.RadioItems(
        id='lin_log_cases',
        options=[dict(label='Linear', value=0), dict(label='Log', value=1)],
        value=0,
        switch=True,
        style={'textAlign': 'center', 'color': '#fff'}
    )

radio_projection = dbc.RadioItems(
        id='projection',
        options=[dict(label='Equirectangular', value=0), dict(label='Orthographic', value=1)],
        value=0,
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

radio_lin_log_deaths = dbc.RadioItems(
        id='lin_log_deaths',
        options=[dict(label='Linear', value=0), dict(label='Log', value=1)],
        value=0,
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
        value='world',
        placeholder='World'
    )

radio_projection2 = dbc.RadioItems(
        id='projection2',
        options=[dict(label='Equirectangular', value=0), dict(label='Orthographic', value=1)],
        value=0,
        switch=True,
        style={'textAlign': 'center', 'color': '#fff'}
    )


# Tests
df_tests = df.dropna(subset=['positive_rate','tests_per_case','total_tests_per_thousand', 'total_cases'])
df_tests.sort_values(by = ['total_tests'], ascending=False, inplace=True)
df_tests.reset_index(drop=True, inplace=True)
df_table = df_tests.groupby(['continent', 'location']).agg({'total_tests_per_thousand': 'mean', 'positive_rate': 'mean', 'total_cases':'mean', 'tests_per_case':'mean', 'population':'mean'}).reset_index()
df_table['total_tests_per_thousand'] = round(df_table.total_tests_per_thousand)
df_table['positive_rate'] = round(df_table.positive_rate * 100)
df_table['total_cases'] = round(df_table.total_cases)
df_table['tests_per_case'] = round(df_table.tests_per_case)
df_table['population'] = round(df_table.population)

df_table.rename(columns={'continent': 'Continent', 'location': 'Country', 'total_tests_per_thousand': 'Total tests per 1000', 
    'positive_rate': 'Positives rate (%)', 'total_cases': 'Total number of cases', 'tests_per_case': 'Tests per case',
    'population': 'Population size'}, inplace=True)

table = dash_table.DataTable(
    id='table_id',
    columns=[
        {'name': i, 'id': i, 'deletable': True} for i in df_table.columns
        # omit the id column
        if i != 'id'
    ],
    data=df_table.to_dict('records'),
    editable=True,
    filter_action="native",
    sort_action="native",
    sort_mode='multi',
    selected_rows=[],
    page_action='native',
    page_current= 0,
    page_size= 10,
    style_data={
        'whiteSpace': 'normal',
        'height': 'auto'
    }
)

dropdown_continent_tests = dcc.Dropdown(
        id='scope_tests',
        options=continent_options2,
        value='world',
        placeholder='World'
    )

tests_options_names = ['total_tests_per_thousand', 'new_tests_per_thousand',
       'new_tests_smoothed', 'new_tests_smoothed_per_thousand', 'positive_rate', 'tests_per_case', 'tests_units']
tests_options = [dict(label=tests.replace('_', ' '), value=tests) for tests in tests_options_names]
dropdown_tests = dcc.Dropdown(
        id='tests_option',
        options=tests_options,
        value='total_tests_per_thousand'
    )

dropdown_tests2 = dcc.Dropdown(
        id='tests_option2',
        options=tests_options,
        value='total_tests_per_thousand'
    )

dropdown_scope3 = dcc.Dropdown(
        id='scope_continent3',
        options=continent_options2,
        value='world',
        placeholder='World'
    )

radio_projection3 = dbc.RadioItems(
        id='projection3',
        options=[dict(label='Equirectangular', value=0), dict(label='Orthographic', value=1)],
        value=0,
        switch=True,
        style={'textAlign': 'center', 'color': '#fff'}
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

radio_lin_log_vac = dbc.RadioItems(
        id='lin_log_vac',
        options=[dict(label='Linear', value=0), dict(label='Log', value=1)],
        value=0,
        switch=True,
        style={'textAlign': 'center', 'color': '#fff'}
    )


####### Components
choose_tab = dcc.Tabs([
        dcc.Tab(label='Cases', children=[
            html.Br(),html.Br(),

            html.Div([
                html.Div([
                    html.Br(),html.Br(),
                    html.H5('Continent Choice', style={'textAlign': 'center', 'color': colors["text"]}),
                    dropdown_scope,
                    html.Br(),html.Br(),
                    html.H5('Which Projection?', style={'textAlign': 'center', 'color': colors["text"]}),
                    radio_projection
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
                    html.Br(),html.Br(),
                    html.H5('Country Choice', style={'textAlign': 'center', 'color': colors["text"]}),
                    dropdown_country_cases,
                    html.Br(),html.Br(),
                    radio_lin_log_cases
                ], style={'width': '30%'}, className='slicerblue')
            ], style={'display': 'flex'})
        ]),

        # Deaths
        dcc.Tab(label='Deaths', children=[
            html.Br(),html.Br(),

            dcc.Tabs([
                dcc.Tab(label='World Map', children=[
                    html.Br(),html.Br(),
                    html.Div([
                        html.Div([
                            dcc.Graph(id='total_deaths_graph')
                        ], style={'width': '70%'}, className='graphblue'),
                        html.Div([
                            html.Br(),html.Br(),
                            html.H5('Continent Choice', style={'textAlign': 'center', 'color': colors["text"]}),
                            dropdown_scope2,
                            html.Br(),html.Br(),
                            html.H5('Which Projection?', style={'textAlign': 'center', 'color': colors["text"]}),
                            radio_projection2
                        ], style={'width': '30%'}, className='slicerblue')
                    ], style={'display': 'flex'})
                ]),
                dcc.Tab(label='Pie Chart', children=[
                    html.Div([
                        html.Div([
                            dcc.Graph(figure=total_deaths())
                        ], style={'width': '100%', 'height': '480px'}, className='slicerblue')
                    ], style={'display': 'flex'})
                ])
            ]),
            html.Br(),

            html.Div([
                html.Div([
                    html.Br(),
                    html.H5('Country Choice', style={'textAlign': 'center', 'color': colors["text"]}),
                    dropdown_country_deaths,
                    html.Br(),
                    html.H5('Options', style={'textAlign': 'center', 'color': colors["text"]}),
                    dropdown_deaths,
                    html.Br(),
                    radio_lin_log_deaths
                ], style={'width': '30%'}, className='slicerblue'),
                html.Div([
                    dcc.Graph(id='new_deaths_graph')
                ], style={'width': '70%'}, className='graphblue')
            ], style={'display': 'flex'})
        ]),

        # Tests
        dcc.Tab(label='Tests', children=[
            html.Br(),html.Br(),

            html.Div([
                html.Div([
                    table
                ], style={'width': '100%', 'height': '440px'}, className='slicerblue'),
            ], style={'display': 'flex'}),
            html.Br(),html.Br(),

            dcc.Tabs([
                dcc.Tab(label='World Map', children=[
                    html.Br(),html.Br(),
                    html.Div([
                        html.Div([
                            dcc.Graph(id='world_map_tests')
                        ], style={'width': '70%'}, className='graphblue'),
                        html.Div([
                            html.Br(),
                            html.H5('Options to visualize', style={'textAlign': 'center', 'color': colors["text"]}),
                            dropdown_tests,
                            html.Br(),
                            html.H5('Continent Choice', style={'textAlign': 'center', 'color': colors["text"]}),
                            dropdown_scope3,
                            html.Br(),
                            html.H5('Which Projection?', style={'textAlign': 'center', 'color': colors["text"]}),
                            radio_projection3
                        ], style={'width': '30%'}, className='slicerblue')
                    ], style={'display': 'flex'})
                ]),
                dcc.Tab(label='Bar Chart', children=[
                    html.Br(),html.Br(),
                    html.Div([
                        html.Div([
                            html.Br(),html.Br(),
                            html.H5('Options to visualize', style={'textAlign': 'center', 'color': colors["text"]}),
                            dropdown_tests2
                        ], style={'width': '30%'}, className='slicerblue'),
                        html.Div([
                            dcc.Graph(id='bar_tests')
                        ], style={'width': '100%'}, className='graphblue')
                    ], style={'display': 'flex'})
                ])
            ])
        ]),

        # Vaccinations
        dcc.Tab(label='Vaccinations', children=[
            html.Br(),html.Br(),

            html.Div([
                html.Div([
                    dcc.Graph(figure=vac_graph())
                ], style={'width': '100%', 'height': '480px'}, className='slicerblue'),
            ], style={'display': 'flex'}),

            html.Div([
                html.Div([
                    html.Br(),
                    html.H5('Country Choice', style={'textAlign': 'center', 'color': colors["text"]}),
                    dropdown_country,
                    html.Br(),
                    html.H5('Options', style={'textAlign': 'center', 'color': colors["text"]}),
                    dropdown_vaccination,
                    html.Br(),
                    radio_lin_log_vac
                ], style={'width': '30%'}, className='slicerblue'),
                html.Div([
                    dcc.Graph(id='scatter_graph')
                ], style={'width': '70%'}, className='graphblue')
            ], style={'display': 'flex'})
        ])
    ]
)


# Navbar
nav_home = dbc.NavItem(dbc.NavLink("Informations about Covid-19", href="/", active="exact"), style={'align': 'right'})

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
                html.H1('What do we know about Covid-19?', style={'textAlign': 'center', 'color': colors["nav"]})
            ], width=12)
        ]),
        dbc.Row([
            dbc.Col([
                html.H5('The COVID-19 virus, name given by the World Health Organisation to the '
                'disease caused by the new coronavirus SARS-COV-2, can cause severe respiratory '
                'infections, such as pneumonia. This virus was first identified in humans in late '
                '2019 in the Chinese city of Wuhan, Hubei province, and cases have been confirmed '
                'in other countries.', style={'textAlign': 'justify', 'paddingLeft': '20px', 'paddingRight': '20px',
                'paddingTop': '20px'}),
                
                html.H5("This pandemic has spread rapidly around the world, having a major impact on people's "
                'lives. Consequently, information about it has been growing, creating a lot of misinformation. '
                'Therefore, this dashboard seeks to make sense of the current pandemic data in order to better '
                'understand its impact on each country and continent.',
                style={'textAlign': 'justify', 'paddingLeft': '20px', 'paddingRight': '20px',
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
                html.A('Dataset: Our World in Data', href="https://github.com/owid/covid-19-data/tree/master/public/data#%EF%B8%8F-download-our-complete-covid-19-dataset--csv--xlsx--json",
                style={'fontWeight': 'bold', 'color': 'grey'})
            ], width=12, style={'textAlign': 'center'}),
            html.Br(),
            dbc.Col([
                html.A('Group: Beatriz Gon??alves - m20210695, Gon??alo Lopes - m20210679, Guilherme Sim??es - m20211003, '
                'Jo??o Veloso - m20210696', style={'fontWeight': 'bold', 'color': 'grey'})
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
    fig = px.choropleth(df, 
        locations = 'iso_code',
        hover_name='location',
        color="total_cases",
        animation_frame="date",
        color_continuous_scale="YlOrRd",
        scope = scope.lower(),
        title='Total Covid-19 Cases',
        projection=['equirectangular', 'orthographic'][projection],
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
        data_bar.append(dict(type='scatter', x=x_bar, y=y_bar, name=country, mode='lines'))

    layout_linear = dict(yaxis=dict(title='New Cases Per Million', type=['linear', 'log'][scale]),
        title=dict(text='New Cases Per Million from 2020 to 2022'))

    return go.Figure(data=data_bar, layout=layout_linear)


# Deaths
@app.callback(
    Output("new_deaths_graph", "figure"),
    [Input("country_drop_deaths", "value"), Input("lin_log_deaths", "value"), Input('deaths_option', "value")]
)
def new_deaths(countries, scale, death):
    data_sc = []

    for country in countries:
        df_sc = df.loc[(df['location'] == country)]
        x_sc = df_sc['date']
        y_sc = df_sc[death]
        data_sc.append(dict(type='scatter', x=x_sc, y=y_sc, name=country, mode='lines'))

    layout_sc = dict(yaxis=dict(title=death.replace('_', ' '), type=['linear', 'log'][scale]),
        title=dict(text=death.replace('_', ' ').capitalize()))

    return go.Figure(data=data_sc, layout=layout_sc)

@app.callback(
    Output("total_deaths_graph", "figure"),
    [Input("projection2", "value"), Input("scope_continent2", "value")]
)
def total_deaths(projection, scope):
    fig = px.choropleth(df, 
        locations = 'iso_code',
        hover_name='location',
        color="total_deaths",
        animation_frame="date",
        color_continuous_scale="amp",
        scope = scope.lower(),
        projection=['equirectangular', 'orthographic'][projection],
        height=700)
    return fig


# Tests
@app.callback(
    Output("world_map_tests", "figure"),
    [Input("scope_continent3", "value"), Input("projection3", "value"), Input("tests_option", "value")]
)
def world_plot(scope, projection, test):
    fig = px.choropleth(df,
        locations = 'iso_code',
        hover_name='location',
        color=test, 
        animation_frame="date",
        scope = scope.lower(),
        projection=['equirectangular', 'orthographic'][projection],
        color_continuous_scale=[(0, 'rgba(255,254,230,255)'), (0.5, 'rgba(0,69,40,255)'), (1.0, 'rgb(0,0,0)')],
        height=700)
    return fig

@app.callback(
    Output("bar_tests", "figure"),
    [Input("tests_option2", "value")]
)
def bar_plot(test):
    return px.bar(df, x="continent", y=test, animation_frame="date", color="continent", hover_name="location")


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
        data_scatter.append(dict(type='scatter', x=x_scatter, y=y_scatter, name=country, mode='lines'))

    layout_scatter = dict(yaxis=dict(title=vaccination.replace('_', ' '), type=['linear', 'log'][scale]))
    
    return go.Figure(data=data_scatter, layout=layout_scatter)


if __name__ == '__main__':
    app.run_server(debug=True)