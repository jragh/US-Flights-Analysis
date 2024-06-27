import polars as pl
import dash_bootstrap_components as dbc
from dash import html, dcc
import plotly_express as px

def generateRouteCarrierRevenue(selected_viz, selected_airport_1, selected_airport_2, sqlite_path):

    routes_visual_desc = """Displays the Estimated Revenue for the Airport Pair by associated carriers. 
    Will focus on the top 5 carriers for the route, smaller carriers will be lumped into 'Other Carriers'.
    Estimated Revenue based on Average Fare for the given market(s)"""


    routes_carriers_revenue_query = f"""with cte as (

        select * from T100_SEGMENT_ALL_CARRIER_2023_FARES
        where ORIGIN_AIRPORT_NAME = '{selected_airport_1}'
        AND DEST_AIRPORT_NAME = '{selected_airport_2}'
        and CAST(PASSENGERS AS INT) > 0 and CAST(DEPARTURES_PERFORMED AS INT) > 0

        UNION

        select * from T100_SEGMENT_ALL_CARRIER_2023_FARES
        where ORIGIN_AIRPORT_NAME = '{selected_airport_2}'
        AND DEST_AIRPORT_NAME = '{selected_airport_1}'
        and CAST(PASSENGERS AS INT) > 0 and CAST(DEPARTURES_PERFORMED AS INT) > 0

        ),

        split_rank as (
        
        select UNIQUE_CARRIER_NAME, 
        SUM(CAST(PASSENGERS AS INT) * CAST(AVERAGE_FARE AS FLOAT)),
        RANK() OVER (order by SUM(CAST(PASSENGERS AS INT) * CAST(AVERAGE_FARE AS FLOAT)) desc) [CARRIER_RANKING]
        from cte
        group by UNIQUE_CARRIER_NAME
        order by RANK() OVER (order by SUM(CAST(PASSENGERS AS INT) * CAST(AVERAGE_FARE AS FLOAT)) desc) asc

        )

        select cte.UNIQUE_CARRIER_NAME, 
        sr.[CARRIER_RANKING],
        case when CAST(sr.[CARRIER_RANKING] as int) > 5 then 'Other Carriers' else cte.UNIQUE_CARRIER_NAME end as [Carrier Name],
        cte.AIRCRAFT_TYPE,
        AVG(cast(cte.AVERAGE_FARE as float)) AS [Average Fare], 
        SUM(CAST(cte.PASSENGERS AS INT) * CAST(cte.AVERAGE_FARE AS FLOAT)) as [Total Revenue],
        SUM(CAST(cte.PASSENGERS AS INT)) as [Total Passengers],
        SUM(CAST(cte.DEPARTURES_PERFORMED AS INT)) AS [Total Flights]
        from cte
        left join split_rank sr
        on cte.UNIQUE_CARRIER_NAME = sr.UNIQUE_CARRIER_NAME
        GROUP BY cte.UNIQUE_CARRIER_NAME, 
        sr.[CARRIER_RANKING],
        case when CAST(sr.[CARRIER_RANKING] as int) > 5 then 'Other Carriers' else cte.UNIQUE_CARRIER_NAME end,
        cte.AIRCRAFT_TYPE
        ORDER BY cte.UNIQUE_CARRIER_NAME, sr.[CARRIER_RANKING], cte.AIRCRAFT_TYPE
        
    """

    routes_polars = pl.read_database_uri(query=routes_carriers_revenue_query, engine='adbc', uri=sqlite_path)

    h_bar_figure = px.bar(routes_polars, x='Total Revenue', y='Carrier Name',color='AIRCRAFT_TYPE', text_auto='0.3s',
                          orientation='h', barmode='stack')
    
    h_bar_figure.update_traces(textfont_size=10, marker={"cornerradius":4}, textposition='inside', textangle=0,
                               hovertemplate='<b>%{y}</b><br><br>%{data.name}: %{x:$.3s}<extra></extra>')