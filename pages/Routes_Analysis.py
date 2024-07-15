import polars as pl
from dash import html, dcc, Input, Output, State, callback, no_update
import dash_bootstrap_components as dbc
import plotly_express as px

import dash

from .RoutesAnalyticsText import routes_text

from .Routes_Carriers_Revenue import generateRouteCarrierRevenue

from .Routes_Carriers_Passenger_Utilization import generateRouteCarrierPassengerUtilization

dash.register_page(__name__, path='/RouteAnalytics')

sqlite_path = 'sqlite:///US_Flights_Analytics.db'

routes_visual_list = ['Market Pairs: Revenue By Carrier', 'Airport Pairs: Passenger Util % By Carrier']

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

    sqlite_path = 'sqlite:///US_Flights_Analytics.db'

    if selected_viz == 'Market Pairs: Revenue By Carrier':

        airports_df = pl.read_database_uri(engine='adbc', uri=sqlite_path, query = """select ORIGIN_AIRPORT_NAME as [AIRPORT_NAME]
            from T100_SEGMENT_ALL_CARRIER_2023_FARES
            UNION
            select DEST_AIRPORT_NAME as [AIRPORT_NAME]
            from T100_SEGMENT_ALL_CARRIER_2023_FARES;"""
            )
        
        airport_filter_list = sorted([val['AIRPORT_NAME'] for val in airports_df.select(['AIRPORT_NAME']).unique().to_dicts()])


        return '', '', airport_filter_list, [], True, generateRouteCarrierRevenue(selected_viz, 'Los Angeles, CA: Los Angeles International', 'New York, NY: John F. Kennedy International', sqlite_path)
    
    elif selected_viz == 'Airport Pairs: Passenger Util % By Carrier':

        airports_df = pl.read_database_uri(query="select AIRPORT_NAME from T100_AIRPORT_SELECTION;", engine='adbc', uri=sqlite_path)

        airport_filter_list = sorted([val['AIRPORT_NAME'] for val in airports_df.select(['AIRPORT_NAME']).unique().to_dicts()])

        return '', '', airport_filter_list, [], True, generateRouteCarrierPassengerUtilization(selected_viz, 'Los Angeles, CA: Los Angeles International', 'New York, NY: John F. Kennedy International', sqlite_path)




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
    
    if selected_viz == 'Airport Pairs: Passenger Util % By Carrier' and selected_airport_1 != '':

        sqlite_path = 'sqlite:///US_Flights_Analytics.db'

        airports_df = pl.read_database_uri(engine='adbc', uri=sqlite_path, query = f"""
            select ORIGIN_AIRPORT_NAME as [AIRPORT_NAME]
            from T100_SEGMENT_ALL_CARRIER_2023_AIRPORTS_LOOKUP
            where DEST_AIRPORT_NAME == '{selected_airport_1}'
            UNION
            select DEST_AIRPORT_NAME as [AIRPORT_NAME]
            from T100_SEGMENT_ALL_CARRIER_2023_AIRPORTS_LOOKUP
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

    ## First section for Market Pairs Revenue Graph Analysis ##
    elif selected_viz == 'Market Pairs: Revenue By Carrier' and (selected_airport_2 == '' or selected_airport_2.strip() == ''):

        return no_update
    
    elif selected_viz == 'Market Pairs: Revenue By Carrier' and (selected_airport_2 != '' or selected_airport_2.strip() != ''):

        sqlite_path = 'sqlite:///US_Flights_Analytics.db'

        return generateRouteCarrierRevenue(selected_viz, selected_airport_1, selected_airport_2, sqlite_path)


    ## Second Section for Airport Pairs Passenger Utilization Analysis ##
    elif selected_viz == 'Airport Pairs: Passenger Util % By Carrier' and (selected_airport_2 == '' or selected_airport_2.strip() == ''):

        return no_update
    
    elif selected_viz == 'Airport Pairs: Passenger Util % By Carrier' and (selected_airport_2 != '' or selected_airport_2.strip() != ''):

        sqlite_path = 'sqlite:///US_Flights_Analytics.db'

        return generateRouteCarrierPassengerUtilization(selected_viz, selected_airport_1, selected_airport_2, sqlite_path)
    

## Callback for the Routes Description Accordion ##
@callback(

    Output(component_id='route-viz-accordion', component_property='active_item'),
    Input(component_id='routes-viz-selection', component_property='value')

)
def accordionActiveItemCallback(selected_viz):

    if selected_viz == routes_visual_list[0]:

        return 'routes-item-1'
    


## Need to add a callback for the Graph display based on selection ##
## If All Carriers, then display entire aggregate ##
## Else if individual graph, then display individual carrier by 12 months breakdown, showing utilization ##
@callback(

    Output(component_id='routes-graph', component_property='figure'),
    Input(component_id='routes-graph-mini-select', component_property='value'),
    State(component_id='routes-viz-selection', component_property='value'),
    State(component_id='routes-airport-selection-1', component_property='value'),
    State(component_id='routes-airport-selection-2', component_property='value'),
    prevent_initial_call=True


)
def changeRoutesGraphVizTwo(selected_carrier, selected_viz, selected_airport_1, selected_airport_2):

    sqlite_path = 'sqlite:///US_Flights_Analytics.db'

    if selected_viz == 'Airport Pairs: Passenger Util % By Carrier':

        if selected_carrier == '' or selected_carrier.strip() == '' or selected_carrier is None or selected_carrier == 'All Carriers':

            ## This is a SQL query to pull the Passengers, Seats, and Flights for the route (Both Ways)
            ## Split By Carrier, individual Carrier will be another query for this ##
            routes_carriers_pass_util_query = f"""

                with cte as (

                select UNIQUE_CARRIER_NAME, 
                cast(MONTH AS INT) AS [MONTH],
                SUM(CAST(PASSENGERS AS INT)) AS [Total Passengers],
                SUM(CAST(SEATS AS INT)) AS [Total Seats],
                SUM(CAST([DEPARTURES_PERFORMED] AS INT)) AS [Total Flights]

                FROM T100_SEGMENT_ALL_CARRIER_2023_AIRPORTS_LOOKUP 

                WHERE DEST_AIRPORT_NAME in ('{selected_airport_1}', '{selected_airport_2}')
                and ORIGIN_AIRPORT_NAME in ('{selected_airport_1}', '{selected_airport_2}')
                and ORIGIN_AIRPORT_NAME <> DEST_AIRPORT_NAME
                AND CAST(PASSENGERS AS INT) >= 1
                and CAST([DEPARTURES_PERFORMED] AS INT) >= 1
                group by  UNIQUE_CARRIER_NAME,CAST(MONTH as int)

                ), 


                grouped_totals as (
                select UNIQUE_CARRIER_NAME,
                SUM(CAST(PASSENGERS AS INT)) as [TOTAL_PASSENGERS],
                SUM(CAST(PASSENGERS AS FLOAT)) / (select SUM(CAST([PASSENGERS] AS FLOAT)) FROM T100_SEGMENT_ALL_CARRIER_2023_AIRPORTS_LOOKUP 

                WHERE DEST_AIRPORT_NAME in ('{selected_airport_1}', '{selected_airport_2}')
                and ORIGIN_AIRPORT_NAME in ('{selected_airport_1}', '{selected_airport_2}')
                and ORIGIN_AIRPORT_NAME <> DEST_AIRPORT_NAME
                AND CAST(PASSENGERS AS INT) >= 1
                and CAST([DEPARTURES_PERFORMED] AS INT) >= 1) as [PCT_ANALYSIS]

                FROM T100_SEGMENT_ALL_CARRIER_2023_AIRPORTS_LOOKUP 

                WHERE DEST_AIRPORT_NAME in ('{selected_airport_1}', '{selected_airport_2}')
                and ORIGIN_AIRPORT_NAME in ('{selected_airport_1}', '{selected_airport_2}')
                and ORIGIN_AIRPORT_NAME <> DEST_AIRPORT_NAME
                AND CAST(PASSENGERS AS INT) >= 1
                and CAST([DEPARTURES_PERFORMED] AS INT) >= 1
                group by UNIQUE_CARRIER_NAME
                )


                select
                CASE WHEN CAST(gt.[PCT_ANALYSIS] as float) < 0.01 THEN 'Other Carriers' else cte.UNIQUE_CARRIER_NAME end as [Unique Carrier Simplified],
                CAST(cte.[Month] as int) as [Month Number],
                mlu.MONTH_NAME_SHORT as [Month],
                SUM(CAST(cte.[Total Passengers] as int)) as [Total Passengers],
                SUM(CAST(cte.[Total Seats] as int)) as [Total Seats],
                SUM(CAST(cte.[Total Flights] as int)) as [Total Flights]

                from cte
                left join grouped_totals gt
                on cte.UNIQUE_CARRIER_NAME = gt.UNIQUE_CARRIER_NAME

                left join MONTHS_LOOKUP mlu
                on cte.[Month] = mlu.[Month]

                group by CASE WHEN CAST(gt.[PCT_ANALYSIS] as float) < 0.01 THEN 'Other Carriers' else cte.UNIQUE_CARRIER_NAME end,
                CAST(cte.[Month] as int),
                mlu.[MONTH_NAME_SHORT]


            """

            routes_polars = pl.read_database_uri(query=routes_carriers_pass_util_query, 
                                                 engine='adbc', 
                                                 uri=sqlite_path).select(
                                                     ['Unique Carrier Simplified', 'Total Passengers', 'Total Seats', 'Total Flights']
                                                     ).group_by(pl.col('Unique Carrier Simplified')).sum()

            routes_bar_figure = px.bar(data_frame=routes_polars, x='Unique Carrier Simplified', y=['Total Passengers', 'Total Seats']
                                   ,text_auto='0.3s', barmode='group'
                                   ,color_discrete_map={'Total Passengers': '#E89C31', 'Total Seats': '#F2C689'})
            
            return routes_bar_figure
        
        elif selected_carrier != '' and selected_carrier.strip() != '' and selected_carrier is not None and selected_carrier != 'All Carriers':

            routes_carriers_pass_util_query = f"""

                with cte as (

                select UNIQUE_CARRIER_NAME, 
                cast(MONTH AS INT) AS [MONTH],
                SUM(CAST(PASSENGERS AS INT)) AS [Total Passengers],
                SUM(CAST(SEATS AS INT)) AS [Total Seats],
                SUM(CAST([DEPARTURES_PERFORMED] AS INT)) AS [Total Flights]

                FROM T100_SEGMENT_ALL_CARRIER_2023_AIRPORTS_LOOKUP 

                WHERE DEST_AIRPORT_NAME in ('{selected_airport_1}', '{selected_airport_2}')
                and ORIGIN_AIRPORT_NAME in ('{selected_airport_1}', '{selected_airport_2}')
                and ORIGIN_AIRPORT_NAME <> DEST_AIRPORT_NAME
                AND CAST(PASSENGERS AS INT) >= 1
                and CAST([DEPARTURES_PERFORMED] AS INT) >= 1
                group by  UNIQUE_CARRIER_NAME,CAST(MONTH as int)

                ), 


                grouped_totals as (
                select UNIQUE_CARRIER_NAME,
                SUM(CAST(PASSENGERS AS INT)) as [TOTAL_PASSENGERS],
                SUM(CAST(PASSENGERS AS FLOAT)) / (select SUM(CAST([PASSENGERS] AS FLOAT)) FROM T100_SEGMENT_ALL_CARRIER_2023_AIRPORTS_LOOKUP 

                WHERE DEST_AIRPORT_NAME in ('{selected_airport_1}', '{selected_airport_2}')
                and ORIGIN_AIRPORT_NAME in ('{selected_airport_1}', '{selected_airport_2}')
                and ORIGIN_AIRPORT_NAME <> DEST_AIRPORT_NAME
                AND CAST(PASSENGERS AS INT) >= 1
                and CAST([DEPARTURES_PERFORMED] AS INT) >= 1) as [PCT_ANALYSIS]

                FROM T100_SEGMENT_ALL_CARRIER_2023_AIRPORTS_LOOKUP 

                WHERE DEST_AIRPORT_NAME in ('{selected_airport_1}', '{selected_airport_2}')
                and ORIGIN_AIRPORT_NAME in ('{selected_airport_1}', '{selected_airport_2}')
                and ORIGIN_AIRPORT_NAME <> DEST_AIRPORT_NAME
                AND CAST(PASSENGERS AS INT) >= 1
                and CAST([DEPARTURES_PERFORMED] AS INT) >= 1
                group by UNIQUE_CARRIER_NAME
                )


                select
                CASE WHEN CAST(gt.[PCT_ANALYSIS] as float) < 0.01 THEN 'Other Carriers' else cte.UNIQUE_CARRIER_NAME end as [Unique Carrier Simplified],
                CAST(cte.[Month] as int) as [Month Number],
                mlu.MONTH_NAME_SHORT as [Month],
                SUM(CAST(cte.[Total Passengers] as int)) as [Total Passengers],
                SUM(CAST(cte.[Total Seats] as int)) as [Total Seats],
                SUM(CAST(cte.[Total Flights] as int)) as [Total Flights]

                from cte
                left join grouped_totals gt
                on cte.UNIQUE_CARRIER_NAME = gt.UNIQUE_CARRIER_NAME

                left join MONTHS_LOOKUP mlu
                on cte.[Month] = mlu.[Month]

                where CASE WHEN CAST(gt.[PCT_ANALYSIS] as float) < 0.01 THEN 'Other Carriers' else cte.UNIQUE_CARRIER_NAME end = '{selected_carrier}'

                group by CASE WHEN CAST(gt.[PCT_ANALYSIS] as float) < 0.01 THEN 'Other Carriers' else cte.UNIQUE_CARRIER_NAME end,
                CAST(cte.[Month] as int),
                mlu.[MONTH_NAME_SHORT]    

            """

            routes_polars = pl.read_database_uri(query=routes_carriers_pass_util_query, 
                                                 engine='adbc', 
                                                 uri=sqlite_path)
            
            routes_bar_figure = px.bar(routes_polars, x='Month', y=['Total Passengers', 'Total Seats']
                                   ,text_auto='0.3s', barmode='group'
                                   ,color_discrete_map={'Total Passengers': '#E89C31', 'Total Seats': '#F2C689'},
                                   title=f"Selected Carrier: {selected_carrier}")
            
            return routes_bar_figure
        
        else: 

            return no_update

    else:

        return no_update