import polars as pl
from dash import html, dcc, Input, Output, State, callback, ctx, no_update
import dash_bootstrap_components as dbc
import plotly_express as px
import os

import dash

from .Passenger_Utilization_Summary import summary
from .PassengerAnalyticsText import passengerText
from .flightsNavbar import navbar_named

from .Passenger_Utilization_Carrier_Routes import passengerUtilizationCarrierRoutes
from .Passenger_Utilization_Carrier_Top10_Toggle import passengerUtilizationCarrierTopTenRoutes, passengerCountsCarrierTopTenRoutes

dash.register_page(__name__, 
                   path='/PassengerAnalytics',
                   title="US Flight Analysis - Passenger Analytics",
                   description="Discover insights on Passenger Airline travel throughout the United States using Passenger and Available Seat counts!",
                   image="passenger_analytics.png")

sqlite_path = os.environ['POSTGRES_URI_LOCATION']

dbc_css = "https://cdn.jsdelivr.net/gh/AnnMarieW/dash-bootstrap-templates/dbc.min.css"

passenger_viz_list = ['Passengers By Carrier', 'Passenger Utilization By Carrier (%)', 'Passenger Utilization Details', 'Top 10 Passenger Routes By Carrier']

analytics_df = pl.read_database_uri(query="""
                                    SELECT * FROM T100_SEGMENT_ALL_CARRIER_2023 
                                    where CAST(PASSENGERS as real) > 0 
                                    and CAST(SEATS as real) > 0 
                                    and CAST(DEPARTURES_PERFORMED as real) > 0 
                                    ORDER BY UNIQUE_CARRIER_NAME, ROUND(CAST(PASSENGERS as numeric), 2) desc""", uri=sqlite_path,engine='adbc')

## TODO: Idea for Carrier sorted list: Group by, then sort by Number of Passengers Flown descending, then select single column, to dicts, etc; 
carrier_filter_list = sorted([val['unique_carrier_name'] for val in analytics_df.select(['unique_carrier_name']).unique().to_dicts()])

## TODO: Remove Global variable when we have the sheet selection ##
textResults = passengerText()

layout = dbc.Container([
    
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
                                    dbc.Label('Airline Carrier Selection:  '),
                                    html.Div([dcc.Dropdown(options=carrier_filter_list, multi=False, searchable=True, clearable=True, 
                                                           placeholder='Select an Airline Carrier here...', id='passenger-carrier-selection',
                                                           style={'fontSize': '12px'})], className='dbc mb-2')

                                ], className='pt-3 pb-2'
                            ), className='bg-light text-dark border rounded-3'
                        )

                    ], width=12, md=8, id='carrier-selection-col', className='mb-2'),

                    dbc.Col([

                        dbc.Card(
                            dbc.CardBody([
                                dbc.Label('Visual Selection: '),
                                html.Div([dcc.Dropdown(options=passenger_viz_list, value='Passengers By Carrier', multi=False, searchable=True, clearable=False, 
                                                       placeholder='Select an Data Viz hre...', id='passenger-viz-selection',
                                                       style={'fontSize': '12px'})], className='dbc mb-2')

                            ], className='pt-3 pb-2'
                            ), className='bg-light text-dark border rounded-3'
                        )

                    ], width=12, md=4, id='visual-selection-col', className='mb-2')
                ]),

                

                
                

                ## Creating Graph Component for quick analytics ##
                dbc.Spinner([
                    html.Div([
                        html.H2('All Carriers: Number of Passengers Transported', id='graph-header'),
                        html.Hr(className='my-2'),
                        html.P('', className='mb-2', id='passenger-graph-desc'),

                        dcc.Graph(id='passengers-graph', style={'height': '50vh'})
                    ], className='p-4 bg-light text-dark border rounded-3', id='pass_visual_div')
                ], show_initially=True, spinner_style={'height': '3rem', 'width': '3rem'})


                

            ])], align="center")
            
            

        ], id='graph_section', width = 12, lg = 8, md = 12, xl = 8, xxl = 8, sm=12, class_name='px-2')

    ])
], fluid=True, className='mr-4 ml-4')

@callback(
    Output(component_id='pass_visual_div', component_property='children'),
    [Input(component_id='passenger-carrier-selection', component_property='value'),
     Input(component_id='passenger-viz-selection', component_property='value')
    ]
)
def passengers_carrier_selection(selected_carrier, selected_pass_viz):

    months_text = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

    ## First Return is Passengers By Carrier ##
    if selected_pass_viz == 'Passengers By Carrier':

        pass_graph_desc = 'Provides the total number of passengers transported on flights throughout the entire year for the given carrier. (All Carriers shown if none provided)'
        
        pass_carrier = pl.read_database_uri(query="""
                                            SELECT unique_carrier_name as "UNIQUE_CARRIER_NAME", 
                                            "month" as "MONTH", 
                                            "year" as "YEAR", 
                                            CAST("TOTAL PASSENGERS" as real) as "TOTAL PASSENGERS"
                                            FROM t100_passengers_by_carrier_2023""", 
                                            uri=sqlite_path,
                                            engine='adbc')
        
        print(pass_carrier.head(500))

        if selected_carrier is None or selected_carrier.strip() == '':

            bar_figure = px.bar(pass_carrier.select(['MONTH', 'TOTAL PASSENGERS']).group_by(pl.col('MONTH')).sum(), x='MONTH', y='TOTAL PASSENGERS',
                                text_auto='.2s', title='Passengers Transported By Month: All Carriers')

            bar_figure.update_traces(textposition='outside', textangle=0, marker_color="#0B2838", marker={"cornerradius":4})

            bar_figure.update_xaxes(categoryorder='array', categoryarray=months_text, linewidth=2.5, showgrid=False, linecolor='rgb(204, 204, 204)')

            bar_figure.update_yaxes( showgrid=True, zeroline=False, showline=False, showticklabels=True, tickwidth=2,gridcolor="rgba(30, 63, 102, 0.15)")

            bar_figure.update_layout(plot_bgcolor='white')

            return_children = [
                html.H2('All Carriers: Number of Passengers Transported', id='graph-header'),
                html.Hr(className='my-2'),
                html.P(pass_graph_desc, className='mb-2 text-muted', id='passenger-graph-desc'),
                dcc.Graph(figure=bar_figure, id='passengers-graph', style={'height': '52vh'})
            ]

            return return_children
        
        else:

            bar_figure = px.bar(pass_carrier.filter(pl.col("UNIQUE_CARRIER_NAME").eq(selected_carrier)), x='MONTH', y='TOTAL PASSENGERS',
                                text_auto='.2s', title=f'Passengers Transported By Month: {selected_carrier}')

            bar_figure.update_traces(textposition='outside', textangle=0, marker_color="#0B2838", marker={"cornerradius":4})

            bar_figure.update_xaxes(categoryorder='array', categoryarray=months_text, linewidth=2.5, showgrid=False, linecolor='rgb(204, 204, 204)')
            
            bar_figure.update_yaxes( showgrid=True, zeroline=False, showline=False, showticklabels=True, tickwidth=2, gridcolor="rgba(30, 63, 102, 0.15)")

            bar_figure.update_layout(plot_bgcolor='white')

            return_children = [
                html.H2(f'{selected_carrier}: Number of Passengers Transported', id='graph-header'),
                html.Hr(className='my-2'),
                html.P(pass_graph_desc, className='mb-2 text-muted', id='passenger-graph-desc'),
                dcc.Graph(figure=bar_figure, id='passengers-graph', style={'height': '52vh'})
            ]
            

            return return_children
        

    ## Second Return is for showing seat usage utilization ## 
    elif selected_pass_viz == 'Passenger Utilization By Carrier (%)':

        pass_graph_desc = 'Provides the percentage of seats used by passnegers (Passengers Divided By Seats) for the given carrier throughout the year. (All Carriers shown if none provided)'

        if selected_carrier is None or selected_carrier.strip() == '':

            pass_util_carrier = pl.read_database_uri(query="""
                                                     select a.month as "MONTH",
                                                     a.year as "YEAR",
                                                     a."TOTAL SEATS"::real,
                                                     a."TOTAL PASSENGERS"::real,
                                                     a."PASSENGER UTILIZATION PCT"::real
                                                     from T100_PASSENGER_UTILIZATION_TOTAL_2023 a 
                                                     left join MONTHS_LOOKUP b 
                                                     on a.MONTH = b.MONTH_NAME_SHORT::text 
                                                     order by CAST(b.MONTH as numeric) asc""", uri=sqlite_path,engine='adbc')

            bar_figure = px.bar(pass_util_carrier.select(['MONTH', 'TOTAL SEATS', 'TOTAL PASSENGERS']).group_by(pl.col('MONTH')).sum(),
                                x='MONTH', y=['TOTAL SEATS', 'TOTAL PASSENGERS'], title='Passenger Seat Utilization: All Carriers',
                                barmode='group', text_auto='.3s')
            
            bar_figure.update_traces(textposition='outside', textangle=0)

            bar_figure.update_yaxes( showgrid=True, zeroline=False, showline=False, showticklabels=True, tickwidth=2, gridcolor="rgba(30, 63, 102, 0.15)")

            ## Add in Line Figure
            line_figure = px.line(pass_util_carrier.select(['MONTH', 'PASSENGER UTILIZATION PCT']), x='MONTH', y='PASSENGER UTILIZATION PCT',
                                  category_orders={'MONTH': months_text}, markers=True)

            line_figure.update_xaxes(type='category')

            line_figure.update_traces(yaxis ="y2", line_color="rgba(255, 183, 3, 0.6)", name='PASSENGER UTILIZATION PCT', showlegend=True)

            bar_figure.add_traces(list(line_figure.select_traces())).update_layout(yaxis2={"overlaying":"y", "side":"right", 'rangemode': "tozero", "tickformat":'.1%', "title": "Seats / Passengers (%)"},
                                                                  yaxis1={"rangemode": "normal", "title" : "Total Seats or Passengers"})

            bar_figure.update_xaxes(categoryorder='array', categoryarray=months_text, linewidth=2.5, showgrid=False, linecolor='rgb(204, 204, 204)')

            bar_figure.update_layout(plot_bgcolor='white')

            ## Adding in Horizontal Legend
            bar_figure.update_layout(plot_bgcolor='white', legend_title=None, legend=dict(orientation="h", xanchor="center", x=0.5, yanchor='bottom', y=-0.32), hovermode="x unified", xaxis_title=None)

            ## Set Bar Colors ##
            bar_figure.update_traces(marker_color="#023E8A", selector={"name": "TOTAL SEATS"}, marker={"cornerradius":4})

            bar_figure.update_traces(marker_color="#A2D2FF", selector={"name": "TOTAL PASSENGERS"}, marker={"cornerradius":4})

            bar_figure.update_traces(hovertemplate="%{y}")

            return_children = [
                html.H2('All Carriers: Passenger Util. (%)', id='graph-header'),
                html.Hr(className='my-2'),
                html.P(pass_graph_desc, className='mb-2 text-muted', id='passenger-graph-desc'),
                dcc.Graph(figure=bar_figure, id='passengers-graph', style={'height': '52vh'})
            ]

            return return_children
        
        else:

            pass_util_carrier = pl.read_database_uri(query="""
                                                     select a.unique_carrier_name as "UNIQUE_CARRIER_NAME",
                                                     a."month" as "MONTH",
                                                     a."year" as "YEAR",
                                                     a."TOTAL SEATS"::real as "TOTAL SEATS",
                                                     a."TOTAL PASSENGERS"::real as "TOTAL PASSENGERS",
                                                     a."PASSENGER UTILIZATION PCT"::real as "PASSENGER UTILIZATION PCT" 
                                                     from T100_PASSENGER_UTILIZATION_BY_CARRIER_2023 a 
                                                     left join MONTHS_LOOKUP b on a.MONTH = b.MONTH_NAME_SHORT 
                                                     order by CAST(b.MONTH as int) asc""", uri=sqlite_path,engine='adbc')

            bar_figure = px.bar(pass_util_carrier.filter(pl.col('UNIQUE_CARRIER_NAME') == selected_carrier).select(['MONTH', 'TOTAL SEATS', 'TOTAL PASSENGERS']),
                                x='MONTH', y=['TOTAL SEATS', 'TOTAL PASSENGERS'], title=f'Passenger Seat Utilization Pct: {selected_carrier}',
                                barmode='group', text_auto='.3s')
            

            
            bar_figure.update_traces(textposition='outside', textangle=0)

            bar_figure.update_yaxes( showgrid=True, zeroline=False, showline=False, showticklabels=True, tickwidth=2, gridcolor="rgba(30, 63, 102, 0.15)")

            ## Add in Line Figure
            line_figure = px.line(pass_util_carrier.filter(pl.col('UNIQUE_CARRIER_NAME') == selected_carrier).select(['MONTH', 'PASSENGER UTILIZATION PCT']),
                                  x='MONTH', y='PASSENGER UTILIZATION PCT', category_orders={'MONTH': months_text}, markers=True)
            
            line_figure.update_xaxes(type='category')

            line_figure.update_traces(yaxis ="y2", line_color="rgba(255, 183, 3, 0.6)", name='PASSENGER UTILIZATION PCT', showlegend=True)

            bar_figure.add_traces(list(line_figure.select_traces())).update_layout(yaxis2={"overlaying":"y", "side":"right", 'rangemode': "tozero", "tickformat":'.1%', "title": "Seats / Passengers (%)"},
                                                                  yaxis1={"rangemode": "normal", "title" : "Total Seats or Passengers"})

            bar_figure.update_xaxes(categoryorder='array', categoryarray=months_text, linewidth=2.5, showgrid=False, linecolor='rgb(204, 204, 204)')

            ## Adding in Horizontal Legend
            bar_figure.update_layout(plot_bgcolor='white', legend_title=None, legend=dict(orientation="h", xanchor="center", x=0.5, yanchor='bottom', y=-0.32), hovermode="x unified", xaxis_title=None)

            ## Set Bar Colors ##
            bar_figure.update_traces(marker_color="#023E8A", selector={"name": "TOTAL SEATS"}, marker={"cornerradius":4})

            bar_figure.update_traces(marker_color="#A2D2FF", selector={"name": "TOTAL PASSENGERS"}, marker={"cornerradius":4})

            bar_figure.update_traces(hovertemplate="%{y}")

            return_children = [
                html.H2(f'{selected_carrier}: Passenger Seat Utilization Pct', id='graph-header'),
                html.Hr(className='my-2'),
                html.P(pass_graph_desc, className='mb-2 text-muted', id='passenger-graph-desc'),
                dcc.Graph(figure=bar_figure, id='passengers-graph', style={'height': '52vh'})
            ]

            return return_children
        
    
    ## Return Dash AG Grid for Summary Table on Passenger Utilization ##
    elif selected_pass_viz == 'Passenger Utilization Details':

        pass_graph_desc = 'Provides a summary table of Unique Routes, Passengers, Seats & Passenger Utilization Rate through the year for each carrier (Table is filterable)'

        dag_table = summary

        return_children = [
                html.H2('Passenger Utilization Details', id='graph-header'),
                html.Hr(className='my-2'),
                html.P(pass_graph_desc, className='mb-3 text-muted', id='passenger-graph-desc'),
                dag_table
        ]

        return return_children
    
    elif selected_pass_viz == 'Top 10 Passenger Routes By Carrier':

        if ctx.triggered_id == 'passenger-carrier-selection':

            if selected_carrier is None or selected_carrier.strip() == '':

                return no_update
            
            else:

                return passengerUtilizationCarrierRoutes(f'{selected_carrier}', sqlite_path=sqlite_path)

        elif ctx.triggered_id == 'passenger-viz-selection':

            if selected_carrier is None or selected_carrier.strip() == '':

                return passengerUtilizationCarrierRoutes('Porter Airlines, Inc.', sqlite_path=sqlite_path)
            
            else:

                return passengerUtilizationCarrierRoutes(f'{selected_carrier}', sqlite_path=sqlite_path)





@callback(
    Output(component_id='passenger-carrier-selection', component_property='disabled'),
    Output(component_id='passenger-carrier-selection', component_property='value'),
    [Input(component_id='passenger-viz-selection', component_property='value')],
    State(component_id='passenger-carrier-selection', component_property='value')
)
def pass_details_disable_carrier(selected_pass_viz, carrier_state):

    if selected_pass_viz == 'Passenger Utilization Details':

        return True, None
    
    return False, carrier_state


@callback(
    Output(component_id='passengers-graph', component_property='figure'),
    [Input(component_id='passengers-graph-mini-select', component_property='value')],
    State(component_id='passengers-carrier-routes-store', component_property='data'),
    prevent_initial_call=True
)
def togglePassengerCarrierTopRoutesFigure(route_toggle, stored_carrier):

    print('Hello Toggle!')

    if route_toggle == 2:

        ## Currently using global for sqlite path, will need to change this ## 
        return passengerUtilizationCarrierTopTenRoutes(route_toggle, stored_carrier['carrier-name'], sqlite_path=sqlite_path)
    
    elif route_toggle == 1:

        ## Again using global sqlite path, will need to change this to a local variation
        return passengerCountsCarrierTopTenRoutes(route_toggle, stored_carrier['carrier-name'], sqlite_path=sqlite_path)

    else: 

        return no_update



## This callback is for the Passenger Visual Text Accordion ##
## Button will become active based on the visual selection that user inputs ##
@callback(
    Output(component_id='passenger-viz-accordion', component_property='active_item'),
    [Input(component_id='passenger-viz-selection', component_property='value')]
)
def accordionActiveItemCallback(selected_viz):

    if selected_viz == passenger_viz_list[0]:

        return 'passengers-item-1'
    
    elif selected_viz == passenger_viz_list[1]:

        return 'passengers-item-2'
    
    elif selected_viz == passenger_viz_list[2]:

        return 'passengers-item-3'
    
    elif selected_viz == passenger_viz_list[3]:

        return 'passengers-item-4'