import polars as pl
from dash import html, dcc, Input, Output, State, callback, no_update
import dash_bootstrap_components as dbc
import plotly_express as px

import dash

from .RoutesAnalyticsText import routes_text

from .Routes_Carriers_Revenue import generateRouteCarrierRevenue

dash.register_page(__name__, path='/RouteAnalytics')

sqlite_path = 'sqlite:///US_Flights_Analytics.db'

routes_visual_list = ['Market Pairs: Revenue By Carrier']

textResults = routes_text()

layout = html.Div([dbc.Container([
    
    dbc.Row([

        dbc.Col(children = textResults,
                 id='sidebar', className = 'textSidebar',width = 12, lg = 4, md =12, xl = 4, xxl = 4, sm = 12, align='start'),

        dbc.Col(children=[

            dbc.Row([dbc.Col([

                dbc.Row([
                    dbc.Col([
                        
                        dbc.Card(
                            dbc.CardBody(
                                [
                                    dbc.Label('Visual Selection: '),
                                    html.Div([dcc.Dropdown(value=routes_visual_list[0], options=routes_visual_list, multi=False, searchable=True, clearable=False, 
                                                           placeholder='Select a visual here...', id='routes-viz-selection',
                                                           style={'fontSize': '12px'})], className='dbc mb-2')
                                ], className='pt-2 pb-2'
                            ), className='bg-light text-dark border rounded-3'
                        )

                    ], width=12, md=4, id='visual-selection-col', className='mb-2'),

                    dbc.Col([

                        dbc.Card(
                            dbc.CardBody([
                                dbc.Label('Airport Selection #1'),
                                html.Div([dcc.Dropdown(value='', options=[], multi=False, searchable=True, clearable=True, 
                                                           placeholder='Select the first airport...', id='routes-airport-selection-1',
                                                           style={'fontSize': '12px'})], className='dbc mb-2')
                            ], className='pt-2 pb-2'
                            ), className='bg-light text-dark border rounded-3'
                        )

                    ], width=12, md=4, id='airport-selection-col-1', className='mb-2'),

                    dbc.Col([

                        dbc.Card(
                            dbc.CardBody([
                                dbc.Label('Airport Selection #2'),
                                html.Div([dcc.Dropdown(value='', options=[], multi=False, searchable=True, clearable=True,
                                                           placeholder='Select the second airport...', id='routes-airport-selection-2',
                                                           style={'fontSize': '12px'}, disabled=True)], className='dbc mb-2')
                            ], className='pt-2 pb-2'
                            ), className='bg-light text-dark border rounded-3'
                        )

                    ], width=12, md=4, id='airport-selection-col-2', className='mb-2')
                ], justify='even'),

                

                
                

                ## Creating Graph Component for quick analytics ##
                dbc.Spinner([
                    html.Div([
                        html.H2('', id='routes-graph-header'),
                        html.Hr(className='my-2'),
                        html.P('', className='mb-2', id='routes-graph-desc'),

                        dcc.Graph(id='routes-graph', style={'display': 'block'})
                    ], className='p-4 bg-light text-dark border rounded-3', id='routes-visual-div')
                ], show_initially=True, spinner_style={'height': '3rem', 'width': '3rem'})


                

            ])], align="center")
            
            

        ], id='routes_graph_section', width = 12, lg = 8, md = 12, xl = 8, xxl = 8, sm=12, class_name='px-2')

    ])
], fluid=True, className='mr-4 ml-4')], style={'margin': 0})

## Callback for viz selection 
## Will need to throw in an update for an initial visualization when switched over
## Return the children to the div with the updated graph
@callback(
        
    Output(component_id='routes-airport-selection-1', component_property='value'),
    Output(component_id='routes-airport-selection-2', component_property='value'),
    Output(component_id='routes-airport-selection-1', component_property='options'),
    Output(component_id='routes-airport-selection-2', component_property='options'),
    Output(component_id='routes-airport-selection-2', component_property='disabled'),
    Output(component_id='routes-visual-div', component_property='children'),
    Input(component_id='routes-viz-selection', component_property='value')

)
def routesVisualSetup(selected_viz):

    if selected_viz == 'Market Pairs: Revenue By Carrier':

        sqlite_path = 'sqlite:///US_Flights_Analytics.db'

        airports_df = pl.read_database_uri(engine='adbc', uri=sqlite_path, query = """select ORIGIN_AIRPORT_NAME as [AIRPORT_NAME]
            from T100_SEGMENT_ALL_CARRIER_2023_FARES
            UNION
            select DEST_AIRPORT_NAME as [AIRPORT_NAME]
            from T100_SEGMENT_ALL_CARRIER_2023_FARES;"""
            )
        
        airport_filter_list = sorted([val['AIRPORT_NAME'] for val in airports_df.select(['AIRPORT_NAME']).unique().to_dicts()])


        return '', '', airport_filter_list, [], True, generateRouteCarrierRevenue(selected_viz, 'Los Angeles, CA: Los Angeles International', 'New York, NY: John F. Kennedy International', sqlite_path)

## Callback for the Description Accordion ##



## First Callback to handle the first location
## Will activate the second dropdown menu for selection
@callback(

    Output(component_id='routes-airport-selection-2', component_property='disabled', allow_duplicate=True),
    Output(component_id='routes-airport-selection-2', component_property='options', allow_duplicate=True),
    Output(component_id='routes-airport-selection-2', component_property='value', allow_duplicate=True),
    State(component_id='routes-viz-selection', component_property='value'),
    Input(component_id='routes-airport-selection-1', component_property='value'),
    prevent_initial_call=True

)

def routesActivateSecondAirport(selected_viz, selected_airport_1):

    if selected_viz == 'Market Pairs: Revenue By Carrier' and selected_airport_1 != '':

        sqlite_path = 'sqlite:///US_Flights_Analytics.db'

        airports_df = pl.read_database_uri(engine='adbc', uri=sqlite_path, query = f"""
            select ORIGIN_AIRPORT_NAME as [AIRPORT_NAME]
            from T100_SEGMENT_ALL_CARRIER_2023_FARES
            where DEST_AIRPORT_NAME == '{selected_airport_1}'
            UNION
            select DEST_AIRPORT_NAME as [AIRPORT_NAME]
            from T100_SEGMENT_ALL_CARRIER_2023_FARES
            where ORIGIN_AIRPORT_NAME == '{selected_airport_1}';
            """
        )
        
        airport_filter_list_2 = sorted([val['AIRPORT_NAME'] for val in airports_df.select(['AIRPORT_NAME']).unique().to_dicts()])

        return False, airport_filter_list_2, ''
    
    else:

        return True, [], ''

## Second Callback to handle whenever the first dropdown is set, and the second dropdown is selected
@callback(

    Output(component_id='routes-visual-div', component_property='children', allow_duplicate=True),
    State(component_id='routes-viz-selection', component_property='value'),
    State(component_id='routes-airport-selection-1', component_property='value'),
    Input(component_id='routes-airport-selection-2', component_property='value'),
    prevent_initial_call=True
    
)

def generateGraph(selected_viz, selected_airport_1, selected_airport_2):

    if selected_airport_2 is None:

        return no_update

    elif selected_viz == 'Market Pairs: Revenue By Carrier' and (selected_airport_2 == '' or selected_airport_2.strip() == ''):

        return no_update
    
    elif selected_viz == 'Market Pairs: Revenue By Carrier' and (selected_airport_2 != '' or selected_airport_2.strip() != ''):

        sqlite_path = 'sqlite:///US_Flights_Analytics.db'

        return generateRouteCarrierRevenue(selected_viz, selected_airport_1, selected_airport_2, sqlite_path)
    

## Callback for the Routes Description Accordion ##
@callback(

    Output(component_id='route-viz-accordion', component_property='active_item'),
    Input(component_id='routes-viz-selection', component_property='value')

)
def accordionActiveItemCallback(selected_viz):

    if selected_viz == routes_visual_list[0]:

        return 'routes-item-1'