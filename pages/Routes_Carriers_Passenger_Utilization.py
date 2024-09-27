import polars as pl
import dash_bootstrap_components as dbc
from dash import html, dcc
import plotly_express as px


## TODO: Add in a dcc.Store for selected_airport_1 and selected_airport_2 for the carrier callback to use ##
## Important because current callback is linked to a live value, not a store when this function is fired ##
def generateRouteCarrierPassengerUtilization(selected_viz, selected_airport_1, selected_airport_2, sqlite_path):

    routes_visual_desc = """Displays the Passenger Utilization Percentage (Number of Passengers / Number of Available Seats) for the airport pair by associated carirers.
    Larger Carriers are shown individually, while Smaller Carriers (Carrying less than one percent of passengers for the airport pair) are grouped into 'Other Carriers'.
    Data shown on a monthly basis for the year of 2023."""
    ## This is a SQL query to pull the Passengers, Seats, and Flights for the route (Both Ways)
    ## Split By Carrier, individual Carrier will be another query for this ##
    routes_carriers_pass_util_query = f"""
        with cte as (
        select UNIQUE_CARRIER_NAME, 
        cast(MONTH AS real) AS "MONTH",
        SUM(CAST(PASSENGERS AS real)) AS "Total Passengers",
        SUM(CAST(SEATS AS real)) AS "Total Seats",
        SUM(CAST(DEPARTURES_PERFORMED AS real)) AS "Total Flights"
        FROM T100_SEGMENT_ALL_CARRIER_2023_AIRPORTS_LOOKUP 
        WHERE DEST_AIRPORT_NAME in ('{selected_airport_1}', '{selected_airport_2}')
        and ORIGIN_AIRPORT_NAME in ('{selected_airport_1}', '{selected_airport_2}')
        and ORIGIN_AIRPORT_NAME <> DEST_AIRPORT_NAME
        AND CAST(PASSENGERS AS real) >= 1
        and CAST(DEPARTURES_PERFORMED AS real) >= 1
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
        on cte."MONTH" = mlu."month"
        
        group by CASE WHEN CAST(gt."PCT_ANALYSIS" as double precision) < 0.01 THEN 'Other Carriers' else cte.UNIQUE_CARRIER_NAME end,
        CAST(cte."MONTH" as real),
        mlu.MONTH_NAME_SHORT
    """
    routes_polars = pl.read_database_uri(query=routes_carriers_pass_util_query, engine='adbc', uri=sqlite_path).select(['Unique Carrier Simplified', 'Total Passengers', 'Total Seats', 'Total Flights']).group_by(pl.col('Unique Carrier Simplified')).sum()
    
    routes_polars_carrier_list = routes_polars.select(['Unique Carrier Simplified']).unique(maintain_order=True).to_series().to_list()
    
    routes_polars_carrier_list.insert(0, 'All Carriers')
    
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
    
    routes_bar_figure.update_traces(selector={"name": "Total Seats"}, marker={"cornerradius":6})

    routes_bar_figure.update_traces(selector={"name": "Total Passengers"}, marker={"cornerradius":6})

    return_children = [
        
        html.H2(f"{selected_viz}", id='routes-graph-header', style={'marginBottom': '0.1em'}),
        html.P(f'{selected_airport_1} & {selected_airport_2}', id='routes-graph-subheader', className='text-muted', style={'marginBottom': '0.2em'}),
        html.Hr(className='my-2'),
        html.P(routes_visual_desc, className='mb-2 text-muted', id='routes-graph-desc', style={'fontSize': '0.85em'}), 
        html.Span(children=[
            
            html.Small('Carrier Selection: ', className='text-muted mx-2 mt-1 mb-2'),
            dbc.Select(id='routes-graph-mini-select', size='sm', options=routes_polars_carrier_list, class_name='routes-graph-util-select')
        
        ], className='routes-graph-util-span mb-2'),
        dcc.Graph(id='routes-graph', style={'height':'48vh'}, figure=routes_bar_figure)

    ]
    
    return return_children