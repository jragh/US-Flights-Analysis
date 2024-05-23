import polars as pl
from dash import html, dcc, Input, Output, State, callback
import dash_bootstrap_components as dbc
import plotly_express as px

import dash

import flask

from .flightsNavbar import navbar_named
from .AirportAnalyticsText import airport_text

dash.register_page(__name__, path='/AirportAnalytics')

textResults = airport_text()

sqlite_path = 'sqlite:///US_Flights_Analytics.db'

airports_df = pl.read_database_uri(engine='adbc', uri='sqlite:///US_Flights_Analytics.db', query = """select b.[DESCRIPTION] as [CITY AIRPORT NAME], 
                                   count(*) as [NUMBER OF RECORDS]
from [T100_SEGMENT_ALL_CARRIER_2023] a
left join T100_AIRPORT_CODE_LOOKUP_2023 b
on a.[ORIGIN_AIRPORT_ID] = b.[CODE]
where CAST(a.[PASSENGERS] AS INT) > 0
and CAST(a.[SEATS] AS INT) > 0
AND CAST(a.[DEPARTURES_PERFORMED] as int) > 0
and b.[DESCRIPTION] is not null
and a.[ORIGIN_COUNTRY_NAME] LIKE 'United States'
group by b.[DESCRIPTION]
ORDER BY b.[DESCRIPTION] ASC;"""
)

airport_filter_list = sorted([val['CITY AIRPORT NAME'] for val in airports_df.select(['CITY AIRPORT NAME']).unique().to_dicts()])

airports_visual_list = ["Passengers By Routes (Scatter)"]


layout = html.Div([dbc.Container([
    dbc.Row([
        dbc.Col([
            navbar_named('Airport Analytics')
        ], width=12)
    ]),
    dbc.Row([

        dbc.Col(children = textResults,
                 id='sidebar', className = 'textSidebar',width = 12, lg = 4, md =12, xl = 4, xxl = 4, sm = 12, align='start'),

        dbc.Col(children=[

            dbc.Row([dbc.Col([

                ## Header for the Graph Section
                html.Hr(),

                dbc.Row([
                    dbc.Col([
                        
                        dbc.Card(
                            dbc.CardBody(
                                [
                                    dbc.Label('Visual Selection: '),
                                    html.Div([dcc.Dropdown(options=airports_visual_list, multi=False, searchable=True, clearable=True, 
                                                           placeholder='Select a visual here...', id='airport-visual-selection',
                                                           style={'fontSize': '12px'})], className='dbc mb-2')
                                ], className='pt-3 pb-2'
                            ), className='bg-light text-dark border rounded-3'
                        )

                    ], width=12, md=4, id='carrier-selection-col', className='mb-2'),

                    dbc.Col([

                        dbc.Card(
                            dbc.CardBody([
                                dbc.Label('Airport Selection:  '),
                                html.Div([dcc.Dropdown(options=airport_filter_list, multi=False, searchable=True, clearable=True, 
                                                           placeholder='Select an Airport from here...', id='airport-airport-selection',
                                                           style={'fontSize': '12px'})], className='dbc mb-2')
                            ], className='pt-3 pb-2'
                            ), className='bg-light text-dark border rounded-3'
                        )

                    ], width=12, md=8, id='visual-selection-col', className='mb-2')
                ]),

                

                
                

                ## Creating Graph Component for quick analytics ##
                dbc.Spinner([
                    html.Div([
                        html.H2('', id='airports-graph-header'),
                        html.Hr(className='my-2'),
                        html.P('', className='mb-2', id='airports-graph-desc'),

                        dcc.Graph(id='airports-graph', style={'height': '50vh'})
                    ], className='p-4 bg-light text-dark border rounded-3', id='airports_visual_div')
                ], show_initially=True, spinner_style={'height': '3rem', 'width': '3rem'})


                

            ])], align="center")
            
            

        ], id='airports-graph_section', width = 12, lg = 8, md = 12, xl = 8, xxl = 8, sm=12, class_name='px-2')

    ])
], fluid=True, className='mr-4 ml-4')], style={'margin': 0})


@callback(
    Output(component_id='airports-visual-div', component_property='children'),
    [Input(component_id='airport-visual-selection', component_property='value'),
     Input(component_id='airport-airport-selection', component_property='value')
     ]
)

def select_airport_visual(selected_viz, selected_airport):

    if selected_viz == 'Passengers By Routes (Scatter)':

        airport_visual_desc = "Passengers By Routes highlights the number of passengers transported by a given carrier against the amount of cities that are reachable using that carrier. If no airport is selected, then the analysis if for the entire United States. Size of bubble shows number of flights that departed from the given airport."

        ## If Statement for scatterplot when there is no airport selected ##
        if selected_airport is None or selected_airport.strip() == '':

            return_children = [



            ]

            return return_children

        
        else:

            return_children = [



            ]

            return return_children

