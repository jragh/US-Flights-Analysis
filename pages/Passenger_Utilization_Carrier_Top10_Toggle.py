import polars as pl

from dash import dcc, html
import dash_bootstrap_components as dbc
import plotly_express as px


def passengerUtilizationCarrierTopTenRoutes(toggle_status, selected_carrier, sqlite_path):

    sqlite_carrier_routes_query = f"""

    with main_grouping as (
    select UNIQUE_CARRIER_NAME,
    DEST_AIRPORT_NAME,
    DEST || ': ' || DEST_CITY_NAME as [DEST_CODE_CITY],
    ORIGIN_AIRPORT_NAME,
    ORIGIN || ': ' || ORIGIN_CITY_NAME as [ORIGIN_CODE_CITY],
    SUM(CAST(PASSENGERS AS INT)) as [TOTAL_PASSENGERS],
    SUM(CAST(SEATS AS INT)) as [TOTAL_SEATS]

    from T100_SEGMENT_ALL_CARRIER_2023_AIRPORTS_LOOKUP

    where DEST_AIRPORT_NAME != ORIGIN_AIRPORT_NAME
    and CAST(PASSENGERS as INT) > 0
    and CAST(DEPARTURES_PERFORMED as INT) > 0

    group by
    UNIQUE_CARRIER_NAME,
    DEST_AIRPORT_NAME,
    DEST || ': ' || DEST_CITY_NAME,
    ORIGIN_AIRPORT_NAME,
    ORIGIN || ': ' || ORIGIN_CITY_NAME 
    ),

    sorting as (
    select *,
    CASE 
        when DEST_CODE_CITY > ORIGIN_CODE_CITY then DEST_CODE_CITY || ' & ' || ORIGIN_CODE_CITY
        when ORIGIN_CODE_CITY > DEST_CODE_CITY then ORIGIN_CODE_CITY || ' & ' || DEST_CODE_CITY
        else 3 end as [AIRPORT_PAIR]
    from main_grouping
    )

    select UNIQUE_CARRIER_NAME,
    [AIRPORT_PAIR],
    SUM(CAST(TOTAL_PASSENGERS as INT)) as [TOTAL PASSENGERS],
    SUM(CAST(TOTAL_SEATS as INT)) as [TOTAL SEATS],

    (SUM(CAST(TOTAL_PASSENGERS as FLOAT)) / SUM(CAST(TOTAL_SEATS as FLOAT))) as [PASSENGER UTIL PCT],

    ROW_NUMBER() OVER (PARTITION BY UNIQUE_CARRIER_NAME order by SUM(CAST(TOTAL_PASSENGERS as INT)) desc) as [PASSENGER RANKING]

    from sorting

    where UNIQUE_CARRIER_NAME = '{selected_carrier}'

    group by UNIQUE_CARRIER_NAME,
    [AIRPORT_PAIR]

    order by UNIQUE_CARRIER_NAME, SUM(CAST(TOTAL_PASSENGERS as INT)) desc;

    """

    polars_carrier_routes= pl.read_database_uri(uri=sqlite_path, query=sqlite_carrier_routes_query, engine='adbc')

    polars_carrier_routes = polars_carrier_routes.filter(pl.col('PASSENGER RANKING') <= 10)

    polars_carrier_category_order = polars_carrier_routes.sort(pl.col('PASSENGER RANKING'), descending=True).select(pl.col('AIRPORT_PAIR')).to_series().to_list()

    polars_barchart = px.bar(polars_carrier_routes, x="PASSENGER UTILIZATION PCT", y="AIRPORT_PAIR", text_auto='0.3%', orientation='h',
                             category_orders=polars_carrier_category_order)

    return polars_barchart