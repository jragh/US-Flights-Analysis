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

    polars_carrier_category_order = polars_carrier_routes.sort(pl.col('TOTAL SEATS'), descending=False).select(pl.col('AIRPORT_PAIR')).to_series().to_list()

    polars_barchart = px.bar(data_frame=polars_carrier_routes, x='PASSENGER UTIL PCT', y="AIRPORT_PAIR", text_auto='0.2%', orientation='h',
                             custom_data=["TOTAL SEATS", "TOTAL PASSENGERS"])

    polars_barchart.update_traces(textfont_size=10, marker={"cornerradius":4},
                                  hovertemplate='''<b>%{y}</b><br><br>
                                  <i>Passenger Util</i>: %{x:.2%}<br>
                                  <i>Total Passengers</i>: %{customdata[1]:.3s}<br>
                                  <i>Total Seats</i>: %{customdata[0]:.3s}''',
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

    polars_barchart = px.bar(polars_carrier_routes, x=["TOTAL SEATS", "TOTAL PASSENGERS"], y="AIRPORT_PAIR", orientation='h',
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

    polars_barchart.update_traces(marker_color="#E89C31", selector={"name": "TOTAL SEATS"}, textposition='outside', textangle=0)

    polars_barchart.update_traces(marker_color="#023E8A", selector={"name": "TOTAL PASSENGERS"}, textposition="inside", textangle=0)

    return polars_barchart
