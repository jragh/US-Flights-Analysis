import polars as pl
import dash_bootstrap_components as dbc
from dash import html, dcc
import plotly_express as px

def generateRouteCarrierPassengerUtilization(selected_viz, selected_airport_1, selected_airport_2, sqlite_path):

    routes_visual_desc = """Displays the Passenger Utilization Percentage (Number of Passengers / Number of Available Seats) for the airport pair by associated carirers.
    Larger Carriers are shown individually, while Smaller Carriers (Carrying less than one percent of passengers for the airport pair) are grouped into 'Other Carriers'.
    Data shown on a monthly basis for the year of 2023."""

    ## This is a SQL query to pull t
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

    routes_polars = pl.read_database_uri(query=routes_carriers_pass_util_query, engine='adbc', uri=sqlite_path).select(['Unique Carrier Simplified', 'Month', 'Total Passengers', 'Total Seats', 'Total Flights']).group_by([pl.col('Unique Carrier Simplified'), pl.col('Month')]).sum()

    routes_bar_figure = px.bar(data_frame=routes_polars, x='Month', y='Total Passengers',text_auto='0.3s'
                          ,custom_data=['Total Passengers', 'Total Flights', 'Total Seats'], facet_col='Unique Carrier Simplified', facet_col_wrap=1)
    
    print(routes_bar_figure)



    return_children = [

        html.H2(f"{selected_viz}", id='routes-graph-header', style={'marginBottom': '0.1em'}),
        html.P(f'{selected_airport_1} & {selected_airport_2}', id='routes-graph-subheader', className='text-muted', style={'marginBottom': '0.2em'}),
        html.Hr(className='my-2'),
        html.P(routes_visual_desc, className='mb-2 text-muted', id='routes-graph-desc', style={'fontSize': '0.85em'}), 
        dcc.Graph(id='routes-graph', style={'height':'54vh'}, figure=routes_bar_figure)

    ]

    return return_children