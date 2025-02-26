import polars as pl

from dash import dcc, html
import dash_bootstrap_components as dbc
import plotly_express as px


def passengerUtilizationCarrierTopTenRoutes(toggle_status, selected_carrier, sqlite_path):

    sqlite_carrier_routes_query = f"""

    with main_grouping as (
    select UNIQUE_CARRIER_NAME as "UNIQUE_CARRIER_NAME",
    DEST_AIRPORT_NAME as "DEST_AIRPORT_NAME",
    CONCAT(DEST, ': ', DEST_CITY_NAME) as "DEST_CODE_CITY",
    ORIGIN_AIRPORT_NAME as "ORIGIN_AIRPORT_NAME",
    CONCAT(ORIGIN, ': ', ORIGIN_CITY_NAME) as "ORIGIN_CODE_CITY",
    SUM(CAST(PASSENGERS AS real)) as "TOTAL_PASSENGERS",
    SUM(CAST(SEATS AS real)) as "TOTAL_SEATS"

    from T100_SEGMENT_ALL_CARRIER_2023_AIRPORTS_LOOKUP

    where DEST_AIRPORT_NAME != ORIGIN_AIRPORT_NAME
    and CAST(PASSENGERS as real) > 0
    and CAST(DEPARTURES_PERFORMED as real) > 0

    group by
    UNIQUE_CARRIER_NAME,
    DEST_AIRPORT_NAME,
    CONCAT(DEST, ': ', DEST_CITY_NAME),
    ORIGIN_AIRPORT_NAME,
    CONCAT(ORIGIN, ': ', ORIGIN_CITY_NAME) 
    ),
    
    sorting as (
    select b.*,
    CASE 
        when b."DEST_CODE_CITY" > b."ORIGIN_CODE_CITY" then CONCAT(b."DEST_CODE_CITY", ' & ', b."ORIGIN_CODE_CITY")
        when b."ORIGIN_CODE_CITY" > b."DEST_CODE_CITY" then CONCAT(b."ORIGIN_CODE_CITY", ' & ', b."DEST_CODE_CITY")
        else '3' end as "AIRPORT_PAIR"
    from main_grouping b
    )
    
    select "UNIQUE_CARRIER_NAME",
    "AIRPORT_PAIR",
    SUM(CAST("TOTAL_PASSENGERS" as real)) as "Total Passengers",
    SUM(CAST("TOTAL_SEATS" as real)) as "Total Seats",

    (SUM(CAST("TOTAL_PASSENGERS" as double precision)) / SUM(CAST("TOTAL_SEATS" as double precision))) as "PASSENGER UTIL PCT",

    ROW_NUMBER() OVER (PARTITION BY "UNIQUE_CARRIER_NAME" order by SUM(CAST("TOTAL_PASSENGERS" as real)) desc) as "PASSENGER RANKING"

    from sorting

    where "UNIQUE_CARRIER_NAME" = '{selected_carrier}'

    group by "UNIQUE_CARRIER_NAME",
    "AIRPORT_PAIR"

    order by "UNIQUE_CARRIER_NAME", SUM(CAST("TOTAL_PASSENGERS" as real)) desc

    """

    polars_carrier_routes= pl.read_database_uri(uri=sqlite_path, query=sqlite_carrier_routes_query, engine='adbc')

    polars_carrier_routes = polars_carrier_routes.filter(pl.col('PASSENGER RANKING') <= 10)

    polars_carrier_category_order = polars_carrier_routes.sort(pl.col('Total Seats'), descending=False).select(pl.col('AIRPORT_PAIR')).to_series().to_list()

    polars_barchart = px.bar(data_frame=polars_carrier_routes, x='PASSENGER UTIL PCT', y="AIRPORT_PAIR", text_auto='0.2%', orientation='h',
                             custom_data=["Total Seats", "Total Passengers"])

    polars_barchart.update_traces(textfont_size=10, marker={"cornerradius":4},
                                  hovertemplate='''<b>%{y}</b><br><br><i>Passenger Util</i>: %{x:.2%}<br><i>Total Passengers</i>: %{customdata[1]:.3s}<br><i>Total Seats</i>: %{customdata[0]:.3s}''',
                                  showlegend=False, marker_color="#E89C31", textposition='outside', textangle=0)

    polars_barchart.update_yaxes(type='category', title='Airport Pair (Both Directions)', linewidth=2.5, showgrid=False, 
                              linecolor='rgb(180, 180, 180)', ticksuffix="  ", categoryorder='array', categoryarray=polars_carrier_category_order, tickfont={'size': 10})
    
    polars_barchart.update_layout(margin={'l':10, 'r': 10, 't': 10, 'b': 8},
                               plot_bgcolor='#f9f9f9', paper_bgcolor="#f9f9f9",
                               legend={'font': {'size': 10}, 'orientation':'h'})
    
    polars_barchart.update_xaxes(title='Passenger Utilization (%)',
                              showgrid=True, zeroline=False, showline=False, 
                              showticklabels=True, tickwidth=2, gridcolor="rgba(60, 60, 60, 0.15)")

    return polars_barchart




def passengerCountsCarrierTopTenRoutes(toggle_status, selected_carrier, sqlite_path):

    sqlite_carrier_routes_query = f"""

    with main_grouping as (
    select UNIQUE_CARRIER_NAME as "UNIQUE_CARRIER_NAME",
    DEST_AIRPORT_NAME as "DEST_AIRPORT_NAME",
    CONCAT(DEST, ': ', DEST_CITY_NAME) as "DEST_CODE_CITY",
    ORIGIN_AIRPORT_NAME as "ORIGIN_AIRPORT_NAME",
    CONCAT(ORIGIN, ': ', ORIGIN_CITY_NAME) as "ORIGIN_CODE_CITY",
    SUM(CAST(PASSENGERS AS real)) as "TOTAL_PASSENGERS",
    SUM(CAST(SEATS AS real)) as "TOTAL_SEATS"

    from T100_SEGMENT_ALL_CARRIER_2023_AIRPORTS_LOOKUP

    where DEST_AIRPORT_NAME != ORIGIN_AIRPORT_NAME
    and CAST(PASSENGERS as real) > 0
    and CAST(DEPARTURES_PERFORMED as real) > 0

    group by
    UNIQUE_CARRIER_NAME,
    DEST_AIRPORT_NAME,
    CONCAT(DEST, ': ', DEST_CITY_NAME),
    ORIGIN_AIRPORT_NAME,
    CONCAT(ORIGIN, ': ', ORIGIN_CITY_NAME) 
    ),
    
    sorting as (
    select b.*,
    CASE 
        when b."DEST_CODE_CITY" > b."ORIGIN_CODE_CITY" then CONCAT(b."DEST_CODE_CITY", ' & ', b."ORIGIN_CODE_CITY")
        when b."ORIGIN_CODE_CITY" > b."DEST_CODE_CITY" then CONCAT(b."ORIGIN_CODE_CITY", ' & ', b."DEST_CODE_CITY")
        else '3' end as "AIRPORT_PAIR"
    from main_grouping b
    )
    
    select "UNIQUE_CARRIER_NAME",
    "AIRPORT_PAIR",
    SUM(CAST("TOTAL_PASSENGERS" as real)) as "Total Passengers",
    SUM(CAST("TOTAL_SEATS" as real)) as "Total Seats",

    (SUM(CAST("TOTAL_PASSENGERS" as double precision)) / SUM(CAST("TOTAL_SEATS" as double precision))) as "PASSENGER UTIL PCT",

    ROW_NUMBER() OVER (PARTITION BY "UNIQUE_CARRIER_NAME" order by SUM(CAST("TOTAL_PASSENGERS" as real)) desc) as "PASSENGER RANKING"

    from sorting

    where "UNIQUE_CARRIER_NAME" = '{selected_carrier}'

    group by "UNIQUE_CARRIER_NAME",
    "AIRPORT_PAIR"

    order by "UNIQUE_CARRIER_NAME", SUM(CAST("TOTAL_PASSENGERS" as real)) desc

    """

    polars_carrier_routes= pl.read_database_uri(uri=sqlite_path, query=sqlite_carrier_routes_query, engine='adbc')

    polars_carrier_routes = polars_carrier_routes.filter(pl.col('PASSENGER RANKING') <= 10)

    polars_barchart = px.bar(polars_carrier_routes, x=["Total Seats", "Total Passengers"], y="AIRPORT_PAIR", orientation='h',
                            barmode='overlay', text_auto='0.3s', opacity=0.75)
    
    polars_barchart.update_traces(textfont_size=10, marker={"cornerradius":4},
                                  hovertemplate='<b>%{y}</b><br><br>%{data.name}: %{x:.3s}<extra></extra>')
    
    polars_barchart.update_layout(yaxis={'tickfont': {'size': 10}, 'categoryorder': 'total ascending'}, 
                                  margin={'l':10, 'r': 10, 't': 10, 'b': 8},
                               plot_bgcolor='#f9f9f9', paper_bgcolor="#f9f9f9",
                               legend={'font': {'size': 10}, 'orientation':'h'})
    
    polars_barchart.update_legends(yanchor="bottom", y=1.02, xanchor= 'right', x= 0.5, title=None)

    polars_barchart.update_yaxes(type='category', title='Airport Pair (Both Directions)', linewidth=2.5, showgrid=False, 
                              linecolor='rgb(180, 180, 180)', ticksuffix="  ")
    
    polars_barchart.update_xaxes(title='Total Passengers & Seats',
                              showgrid=True, zeroline=False, showline=False, 
                              showticklabels=True, tickwidth=2, gridcolor="rgba(60, 60, 60, 0.15)")

    polars_barchart.update_traces(marker_color="#E89C31", selector={"name": "Total Seats"}, textposition='outside', textangle=0)

    polars_barchart.update_traces(marker_color="#023E8A", selector={"name": "Total Passengers"}, textposition="inside", textangle=0)

    return polars_barchart
