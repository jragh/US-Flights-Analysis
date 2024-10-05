import polars as pl
from dash import html, dcc, Input, Output, State, callback, no_update
import dash_bootstrap_components as dbc
import plotly_express as px
import os

import dash

from .RoutesAnalyticsText import routes_text

from .Routes_Carriers_Revenue import generateRouteCarrierRevenue

from .Routes_Carriers_Passenger_Utilization import generateRouteCarrierPassengerUtilization

from .Routes_Scatter_Analysis_Carriers import generateScatterCarrierRouteLoadFactor, updateScatterCarrierRouteLoadFactor

dash.register_page(__name__, 
                   path='/RouteAnalytics', 
                   title="US Flight Analysis - Route Analytics", 
                   description='A deeper dive on Market Pairs and Air Travel Routes across the United States.',
                   image="RoutesAnalysisMetaImage.png")

sqlite_path = os.environ['POSTGRES_URI_LOCATION']

routes_visual_list = ['Market Pairs: Revenue By Carrier', 'Airport Pairs: Passenger Util % By Carrier', 'Scatter Analysis: Load Factor By Carrier']

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
    Output(component_id='routes-airport-selection-1', component_property='disabled'),
    Output(component_id='routes-airport-selection-2', component_property='disabled'),
    Output(component_id='routes-visual-div', component_property='children'),
    Output(component_id='routes-airport-store-1', component_property='data'),
    Output(component_id='routes-airport-store-2', component_property='data'),
    Input(component_id='routes-viz-selection', component_property='value')

)
def routesVisualSetup(selected_viz):

    sqlite_path = os.environ['POSTGRES_URI_LOCATION']

    if selected_viz == 'Market Pairs: Revenue By Carrier':

        airports_df = pl.read_database_uri(engine='adbc', uri=sqlite_path, query = """
                                           select ORIGIN_AIRPORT_NAME as "AIRPORT_NAME"
                                        from T100_SEGMENT_ALL_CARRIER_2023_FARES
                                        UNION
                                        select DEST_AIRPORT_NAME as "AIRPORT_NAME"
                                        from T100_SEGMENT_ALL_CARRIER_2023_FARES"""
                                           )
        
        airport_filter_list = sorted([val['AIRPORT_NAME'] for val in airports_df.select(['AIRPORT_NAME']).unique().to_dicts()])


        return '', '', airport_filter_list, [], False, True, generateRouteCarrierRevenue(selected_viz, 'Los Angeles, CA: Los Angeles International', 'New York, NY: John F. Kennedy International', sqlite_path), no_update, no_update
    
    elif selected_viz == 'Airport Pairs: Passenger Util % By Carrier':

        airports_df = pl.read_database_uri(query="""
                                           select AIRPORT_NAME as "AIRPORT_NAME" 
                                           from T100_AIRPORT_SELECTION
                                           """, engine='adbc', uri=sqlite_path)

        airport_filter_list = sorted([val['AIRPORT_NAME'] for val in airports_df.select(['AIRPORT_NAME']).unique().to_dicts()])

        return '', '', airport_filter_list, [], False, True, generateRouteCarrierPassengerUtilization(selected_viz, 'Los Angeles, CA: Los Angeles International', 'New York, NY: John F. Kennedy International', sqlite_path), {'airport-name-1': 'Los Angeles, CA: Los Angeles International'}, {'airport-name-2': 'New York, NY: John F. Kennedy International'}


    elif selected_viz == 'Scatter Analysis: Load Factor By Carrier':

        return '', '', [], [], True, True, generateScatterCarrierRouteLoadFactor(selected_viz=selected_viz, selected_carrier='', sqlite_path=sqlite_path), {'airport-name-1': 'Los Angeles, CA: Los Angeles International'}, {'airport-name-2': 'New York, NY: John F. Kennedy International'}


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

        sqlite_path = os.environ['POSTGRES_URI_LOCATION']

        airports_df = pl.read_database_uri(engine='adbc', uri=sqlite_path, query = f"""
            select ORIGIN_AIRPORT_NAME as "AIRPORT_NAME"
            from T100_SEGMENT_ALL_CARRIER_2023_FARES
            where dest_airport_name like '{selected_airport_1}'
            UNION
            select DEST_AIRPORT_NAME as "AIRPORT_NAME"
            from T100_SEGMENT_ALL_CARRIER_2023_FARES
            where origin_airport_name like '{selected_airport_1}'
            """
        )
        
        airport_filter_list_2 = sorted([val['AIRPORT_NAME'] for val in airports_df.select(['AIRPORT_NAME']).unique().to_dicts()])

        return False, airport_filter_list_2, ''
    
    if selected_viz == 'Airport Pairs: Passenger Util % By Carrier' and selected_airport_1 != '':

        sqlite_path = os.environ['POSTGRES_URI_LOCATION']

        airports_df = pl.read_database_uri(engine='adbc', uri=sqlite_path, query = f"""
            select ORIGIN_AIRPORT_NAME as "AIRPORT_NAME"
            from T100_SEGMENT_ALL_CARRIER_2023_AIRPORTS_LOOKUP
            where dest_airport_name like '{selected_airport_1}'
            and CAST(Passengers as real) > 0 AND CAST(SEATS AS real) > 0 and CAST(departures_performed as real) > 0
            UNION
            select DEST_AIRPORT_NAME as "AIRPORT_NAME"
            from T100_SEGMENT_ALL_CARRIER_2023_AIRPORTS_LOOKUP
            where origin_airport_name like '{selected_airport_1}'
            and CAST(Passengers as real) > 0 AND CAST(SEATS AS real) > 0 and CAST(departures_performed as real) > 0
            """
        )

        airport_filter_list_2 = sorted([val['AIRPORT_NAME'] for val in airports_df.select(['AIRPORT_NAME']).unique().to_dicts()])

        return False, airport_filter_list_2, ''
    
    else:

        return True, [], ''

## Second Callback to handle whenever the first dropdown is set, and the second dropdown is selected
@callback(

    Output(component_id='routes-visual-div', component_property='children', allow_duplicate=True),
    Output(component_id='routes-airport-store-1', component_property='data', allow_duplicate=True),
    Output(component_id='routes-airport-store-2', component_property='data', allow_duplicate=True),
    State(component_id='routes-viz-selection', component_property='value'),
    State(component_id='routes-airport-selection-1', component_property='value'),
    Input(component_id='routes-airport-selection-2', component_property='value'),
    prevent_initial_call=True
    
)

def generateGraph(selected_viz, selected_airport_1, selected_airport_2):

    if selected_airport_2 is None:

        return no_update, no_update, no_update

    ## First section for Market Pairs Revenue Graph Analysis ##
    elif selected_viz == 'Market Pairs: Revenue By Carrier' and (selected_airport_2 == '' or selected_airport_2.strip() == ''):

        return no_update, no_update, no_update
    
    elif selected_viz == 'Market Pairs: Revenue By Carrier' and (selected_airport_2 != '' or selected_airport_2.strip() != ''):

        sqlite_path = os.environ['POSTGRES_URI_LOCATION']

        return generateRouteCarrierRevenue(selected_viz, selected_airport_1, selected_airport_2, sqlite_path), no_update, no_update


    ## Second Section for Airport Pairs Passenger Utilization Analysis ##
    elif selected_viz == 'Airport Pairs: Passenger Util % By Carrier' and (selected_airport_2 == '' or selected_airport_2.strip() == ''):

        return no_update, no_update, no_update
    
    elif selected_viz == 'Airport Pairs: Passenger Util % By Carrier' and (selected_airport_2 != '' or selected_airport_2.strip() != ''):

        sqlite_path = os.environ['POSTGRES_URI_LOCATION']

        return generateRouteCarrierPassengerUtilization(selected_viz, selected_airport_1, selected_airport_2, sqlite_path), {'airport-name-1': f"{selected_airport_1}"}, {'airport-name-2': f"{selected_airport_2}"}

    elif selected_viz == 'Scatter Analysis: Load Factor By Carrier':

        return no_update, no_update, no_update  

## Callback for the Routes Description Accordion ##
@callback(

    Output(component_id='route-viz-accordion', component_property='active_item'),
    Input(component_id='routes-viz-selection', component_property='value')

)
def accordionActiveItemCallback(selected_viz):

    if selected_viz == routes_visual_list[0]:

        return 'routes-item-1'
    
    elif selected_viz == routes_visual_list[1]:

        return 'routes-item-2'
    
    elif selected_viz == routes_visual_list[2]:

        return 'routes-item-3'
    


## Need to add a callback for the Graph display based on selection ##
## If All Carriers, then display entire aggregate ##
## Else if individual graph, then display individual carrier by 12 months breakdown, showing utilization ##
@callback(

    Output(component_id='routes-graph', component_property='figure'),
    Output(component_id='routes-graph-subheader', component_property='children'),
    Input(component_id='routes-graph-mini-select', component_property='value'),
    State(component_id='routes-viz-selection', component_property='value'),
    State(component_id='routes-airport-store-1', component_property='data'),
    State(component_id='routes-airport-store-2', component_property='data'),
    prevent_initial_call=True


)
def changeRoutesGraphVizTwo(selected_carrier, selected_viz, stored_airport_1, stored_airport_2):

    selected_airport_1 = stored_airport_1['airport-name-1']

    selected_airport_2 = stored_airport_2['airport-name-2']

    sqlite_path = os.environ['POSTGRES_URI_LOCATION']

    if selected_viz == 'Airport Pairs: Passenger Util % By Carrier':

        if selected_carrier == '' or selected_carrier.strip() == '' or selected_carrier is None or selected_carrier == 'All Carriers':

            ## This is a SQL query to pull the Passengers, Seats, and Flights for the route (Both Ways)
            ## Split By Carrier, individual Carrier will be another query for this ##
            routes_carriers_pass_util_query = f"""

                with cte as (

                select UNIQUE_CARRIER_NAME, 
                cast(MONTH AS real) AS "MONTH",
                SUM(CAST(PASSENGERS AS real)) AS "Total Passengers",
                SUM(CAST(SEATS AS real)) AS "Total Seats",
                SUM(CAST(departures_performed AS real)) AS "Total Flights"

                FROM T100_SEGMENT_ALL_CARRIER_2023_AIRPORTS_LOOKUP 

                WHERE DEST_AIRPORT_NAME in ('{selected_airport_1}', '{selected_airport_2}')
                and ORIGIN_AIRPORT_NAME in ('{selected_airport_1}', '{selected_airport_2}')
                and ORIGIN_AIRPORT_NAME <> DEST_AIRPORT_NAME
                AND CAST(PASSENGERS AS real) >= 1
                and CAST(departures_performed AS real) >= 1
                group by UNIQUE_CARRIER_NAME, CAST(MONTH as real)

                ), 


                grouped_totals as (
                select UNIQUE_CARRIER_NAME,
                SUM(CAST(PASSENGERS AS real)) as "TOTAL_PASSENGERS",
                SUM(CAST(PASSENGERS AS double precision)) / (select SUM(CAST(PASSENGERS AS double precision)) FROM T100_SEGMENT_ALL_CARRIER_2023_AIRPORTS_LOOKUP 

                WHERE DEST_AIRPORT_NAME in ('{selected_airport_1}', '{selected_airport_2}')
                and ORIGIN_AIRPORT_NAME in ('{selected_airport_1}', '{selected_airport_2}')
                and ORIGIN_AIRPORT_NAME <> DEST_AIRPORT_NAME
                AND CAST(PASSENGERS AS real) >= 1
                and CAST(DEPARTURES_PERFORMED AS real) >= 1) as "PCT_ANALYSIS"

                FROM T100_SEGMENT_ALL_CARRIER_2023_AIRPORTS_LOOKUP 

                WHERE DEST_AIRPORT_NAME in ('{selected_airport_1}', '{selected_airport_2}')
                and ORIGIN_AIRPORT_NAME in ('{selected_airport_1}', '{selected_airport_2}')
                and ORIGIN_AIRPORT_NAME <> DEST_AIRPORT_NAME
                AND CAST(PASSENGERS AS real) >= 1
                and CAST(DEPARTURES_PERFORMED AS real) >= 1
                group by UNIQUE_CARRIER_NAME
                )


                select
                CASE WHEN CAST(gt."PCT_ANALYSIS" as double precision) < 0.01 THEN 'Other Carriers' else cte.UNIQUE_CARRIER_NAME end as "Unique Carrier Simplified",
                CAST(cte."MONTH" as real) as "Month Number",
                mlu.MONTH_NAME_SHORT as "Month",
                SUM(CAST(cte."Total Passengers" as real)) as "Total Passengers",
                SUM(CAST(cte."Total Seats" as real)) as "Total Seats",
                SUM(CAST(cte."Total Flights" as real)) as "Total Flights"

                from cte
                left join grouped_totals gt
                on cte.UNIQUE_CARRIER_NAME = gt.UNIQUE_CARRIER_NAME

                left join MONTHS_LOOKUP mlu
                on cte."MONTH" = mlu.month

                group by CASE WHEN CAST(gt."PCT_ANALYSIS" as double precision) < 0.01 THEN 'Other Carriers' else cte.UNIQUE_CARRIER_NAME end,
                CAST(cte."MONTH" as real),
                mlu.month_name_short


            """

            routes_polars = pl.read_database_uri(query=routes_carriers_pass_util_query, 
                                                 engine='adbc', 
                                                 uri=sqlite_path).select(
                                                     ['Unique Carrier Simplified', 'Total Passengers', 'Total Seats', 'Total Flights']
                                                     ).group_by(pl.col('Unique Carrier Simplified')).sum()

            routes_bar_figure = px.bar(data_frame=routes_polars, x='Unique Carrier Simplified', y=['Total Passengers', 'Total Seats']
                                   ,text_auto='0.3s', barmode='group'
                                   ,color_discrete_map={'Total Passengers': '#E89C31', 'Total Seats': '#F2C689'})
            
            routes_bar_figure.update_xaxes(categoryorder='total descending')

            routes_bar_figure.update_traces(textposition='outside', textangle=0)

            routes_bar_figure.update_yaxes( showgrid=True, zeroline=False, showline=False, showticklabels=True, tickwidth=2, gridcolor="rgba(30, 63, 102, 0.15)")

            routes_bar_figure.update_xaxes(linewidth=2.5, showgrid=False, linecolor='rgb(204, 204, 204)', title=None)

            routes_bar_figure.update_layout(plot_bgcolor='#f9f9f9', paper_bgcolor="#f9f9f9", legend_title=None, 
                                            legend=dict(orientation="h", xanchor="center", x=0.5, yanchor='bottom', y=1.1), 
                                            hovermode="x unified", xaxis_title=None,
                                            margin={'l':10, 'r': 10, 't': 20, 'b': 5},
                                            yaxis={'tickfont': {'size': 10}, 'title': 'Total Passengers or Seats'})


            
            return routes_bar_figure, no_update
        
        elif selected_carrier != '' and selected_carrier.strip() != '' and selected_carrier is not None and selected_carrier != 'All Carriers':

            months_text = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

            routes_carriers_pass_util_query = f"""

                with cte as (

                select UNIQUE_CARRIER_NAME, 
                cast(MONTH AS real) AS "MONTH",
                SUM(CAST(PASSENGERS AS real)) AS "Total Passengers",
                SUM(CAST(SEATS AS real)) AS "Total Seats",
                SUM(CAST(departures_performed AS real)) AS "Total Flights"

                FROM T100_SEGMENT_ALL_CARRIER_2023_AIRPORTS_LOOKUP 

                WHERE DEST_AIRPORT_NAME in ('{selected_airport_1}', '{selected_airport_2}')
                and ORIGIN_AIRPORT_NAME in ('{selected_airport_1}', '{selected_airport_2}')
                and ORIGIN_AIRPORT_NAME <> DEST_AIRPORT_NAME
                AND CAST(PASSENGERS AS real) >= 1
                and CAST(departures_performed AS real) >= 1
                group by  UNIQUE_CARRIER_NAME,CAST(MONTH as real)

                ), 


                grouped_totals as (
                select UNIQUE_CARRIER_NAME,
                SUM(CAST(PASSENGERS AS real)) as "TOTAL_PASSENGERS",
                SUM(CAST(PASSENGERS AS double precision)) / (select SUM(CAST(PASSENGERS AS double precision)) FROM T100_SEGMENT_ALL_CARRIER_2023_AIRPORTS_LOOKUP 

                WHERE DEST_AIRPORT_NAME in ('{selected_airport_1}', '{selected_airport_2}')
                and ORIGIN_AIRPORT_NAME in ('{selected_airport_1}', '{selected_airport_2}')
                and ORIGIN_AIRPORT_NAME <> DEST_AIRPORT_NAME
                AND CAST(PASSENGERS AS real) >= 1
                and CAST(departures_performed AS real) >= 1) as "PCT_ANALYSIS"

                FROM T100_SEGMENT_ALL_CARRIER_2023_AIRPORTS_LOOKUP 

                WHERE DEST_AIRPORT_NAME in ('{selected_airport_1}', '{selected_airport_2}')
                and ORIGIN_AIRPORT_NAME in ('{selected_airport_1}', '{selected_airport_2}')
                and ORIGIN_AIRPORT_NAME <> DEST_AIRPORT_NAME
                AND CAST(PASSENGERS AS real) >= 1
                and CAST(departures_performed AS real) >= 1
                group by UNIQUE_CARRIER_NAME
                )


                select
                CASE WHEN CAST(gt."PCT_ANALYSIS" as double precision) < 0.01 THEN 'Other Carriers' else cte.UNIQUE_CARRIER_NAME end as "Unique Carrier Simplified",
                CAST(cte."MONTH" as real) as "Month Number",
                mlu.MONTH_NAME_SHORT as "Month",
                SUM(CAST(cte."Total Passengers" as real)) as "Total Passengers",
                SUM(CAST(cte."Total Seats" as real)) as "Total Seats",
                SUM(CAST(cte."Total Flights" as real)) as "Total Flights"

                from cte
                left join grouped_totals gt
                on cte.UNIQUE_CARRIER_NAME = gt.UNIQUE_CARRIER_NAME

                left join MONTHS_LOOKUP mlu
                on cte."MONTH" = mlu.month 

                where CASE WHEN CAST(gt."PCT_ANALYSIS" as double precision) < 0.01 THEN 'Other Carriers' else cte.UNIQUE_CARRIER_NAME end = '{selected_carrier}'

                group by CASE WHEN CAST(gt."PCT_ANALYSIS" as double precision) < 0.01 THEN 'Other Carriers' else cte.UNIQUE_CARRIER_NAME end,
                CAST(cte."MONTH" as real),
                mlu.month_name_short    

            """

            routes_polars = pl.read_database_uri(query=routes_carriers_pass_util_query, 
                                                 engine='adbc', 
                                                 uri=sqlite_path)
            
            routes_polars = routes_polars.with_columns((pl.col('Total Passengers') / pl.col('Total Seats')).alias('Passenger Utilization Pct'))
            
            routes_bar_figure = px.bar(routes_polars, x='Month', y=['Total Passengers', 'Total Seats']
                                   ,text_auto='0.3s', barmode='group'
                                   ,color_discrete_map={'Total Passengers': '#E89C31', 'Total Seats': '#F2C689'} )
            
            routes_bar_figure.update_traces(textposition='outside', textangle=0)

            routes_bar_figure.update_yaxes( showgrid=True, zeroline=False, showline=False, showticklabels=True, tickwidth=2, gridcolor="rgba(30, 63, 102, 0.15)")

            ## Add in Line Figure
            line_figure = px.line(routes_polars.select(['Month', 'Passenger Utilization Pct']),
                                  x='Month', y='Passenger Utilization Pct', category_orders={'Month': months_text}, markers=True)
            
            line_figure.update_xaxes(type='category')

            line_figure.update_traces(yaxis ="y2", line_color="rgba(255, 183, 3, 0.6)", name='Passenger Utilization Pct', showlegend=True)

            ## Add Line figure into Bar figure
            routes_bar_figure.add_traces(list(line_figure.select_traces())).update_layout(yaxis2={"overlaying":"y", "side":"right", 'rangemode': "tozero", "tickformat":'.1%', "title": "Seats / Passengers (%)"},
                                                                  yaxis1={"rangemode": "normal", "title" : "Total Seats or Passengers"})

            routes_bar_figure.update_xaxes(categoryorder='array', categoryarray=months_text, linewidth=2.5, showgrid=False, linecolor='rgb(204, 204, 204)', title=None)

            routes_bar_figure.update_layout(plot_bgcolor='#f9f9f9', paper_bgcolor="#f9f9f9", legend_title=None, 
                                            legend=dict(orientation="h", xanchor="center", x=0.5, yanchor='bottom', y=-0.25), 
                                            hovermode="x unified", xaxis_title=None,
                                            margin={'l':10, 'r': 10, 't': 10, 'b': 5},
                                            yaxis={'tickfont': {'size': 10}}, yaxis2={'tickfont': {'size': 10}})


            routes_bar_figure.update_traces(marker_color="#023E8A", selector={"name": "Total Seats"}, marker={"cornerradius":4})

            routes_bar_figure.update_traces(marker_color="#A2D2FF", selector={"name": "Total Passengers"}, marker={"cornerradius":4})

            routes_bar_figure.update_traces(hovertemplate="%{y}")
            
            return routes_bar_figure, no_update
        
        else: 

            return no_update, no_update
        
    elif selected_viz == 'Scatter Analysis: Load Factor By Carrier':

        sqlite_path = os.environ['POSTGRES_URI_LOCATION']

        print(selected_carrier)

        if selected_carrier is None or selected_carrier.strip() == '' or selected_carrier == 'All Carriers':

            return updateScatterCarrierRouteLoadFactor('', sqlite_path=sqlite_path, min_flights=200), 'Scatter Analysis: All Carriers'
        
        else:

            return updateScatterCarrierRouteLoadFactor(selected_carrier=selected_carrier, sqlite_path=sqlite_path, min_flights=200), f'Scatter Analysis: {selected_carrier}'



    else:

        return no_update
    