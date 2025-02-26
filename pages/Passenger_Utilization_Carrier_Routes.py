import polars as pl

from dash import dcc, html
import dash_bootstrap_components as dbc
import plotly_express as px


## Currently deciding that there will be no option for total USA ##
## Default is Porter airlines (Clean looking visual) ##

## TODO July 29: Implement DCC Store to capture state of carrier whenever it's last changed ##
def passengerUtilizationCarrierRoutes(selected_carrier, sqlite_path):

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

    (SUM(CAST("TOTAL_PASSENGERS" as double precision)) / SUM(CAST("TOTAL_SEATS" as double precision))) * 100.00 as "PASSENGER UTIL PCT",

    ROW_NUMBER() OVER (PARTITION BY "UNIQUE_CARRIER_NAME" order by SUM(CAST("TOTAL_PASSENGERS" as real)) desc) as "PASSENGER RANKING"

    from sorting

    where "UNIQUE_CARRIER_NAME" = '{selected_carrier}'

    group by "UNIQUE_CARRIER_NAME",
    "AIRPORT_PAIR"

    order by "UNIQUE_CARRIER_NAME", SUM(CAST("TOTAL_PASSENGERS" as real)) desc

    """

    passengers_visual_desc = """Highlights the top 10 Airport Pairs (Both directions of travel) by Passenger Traffic for a given airline carrier.
    Allows the user to also see the usage of available seats by passengers for the a given airline route.
    The Passenger Util. % Option shows the Passenger to Seat Ratio directly in percent form."""
    
    polars_carrier_routes = pl.read_database_uri(uri=sqlite_path, query=sqlite_carrier_routes_query, engine="adbc")

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



    return_children = [

        html.H2('Top 10 Passenger Routes By Carrier w/ Passenger Util %', id='passenger-graph-header', style={'marginBottom': '0.1em'}),
        html.P(f'{selected_carrier}', id='passengers-graph-subheader', className='text-muted', style={'marginBottom': '0.2em'}),
        html.Hr(className='my-2'),
        html.P(passengers_visual_desc, className='mb-0 text-muted', id='passengers-graph-desc', style={'fontSize': '0.85em'}),

        html.Span(children=[

            ## Switching to Radio Items as a test for the callback ##
            dbc.RadioItems(inline=True, value=1, id='passengers-graph-mini-select', options=[
                {'label': 'Passenger & Seat Counts', 'value': 1},
                {'label': 'Passenger Utilization Pct (%)', 'value': 2}
            ], className='mb-0 text-muted', style={'fontSize': '0.8em'})

        ], className='passengers-graph-util-span mb-0'),

            ##html.Small('Passenger & Seat Counts', className='mb-0 text-muted mx-2', style={'fontSize': '0.75em'}),
            
            ##dbc.Select(id='passengers-graph-mini-select', size='sm', options=['Passenger & Seat Counts', 'Passenger Utilization Pct (%)'], class_name='routes-graph-util-select'),
           ## html.Small('Passenger Utilization Pct (%)', className='mb-0 text-muted', style={'fontSize': '0.75em'})

        dcc.Store(id='passengers-carrier-routes-store', data={'carrier-name': selected_carrier}),

        dcc.Graph(id='passengers-graph', style={'height': '48vh'}, figure=polars_barchart)

    ]

    return return_children



## "rgba(255, 183, 3, 0.6)"

# routes_bar_figure.update_traces(marker_color="#023E8A", selector={"name": "Total Seats"}, marker={"cornerradius":4})

# routes_bar_figure.update_traces(marker_color="#A2D2FF", selector={"name": "Total Passengers"}, marker={"cornerradius":4})


# html.H2(f"{selected_viz}", id='routes-graph-header', style={'marginBottom': '0.1em'}),
#         html.P(f'{selected_airport_1} & {selected_airport_2}', id='routes-graph-subheader', className='text-muted', style={'marginBottom': '0.2em'}),
#         html.Hr(className='my-2'),
#         html.P(routes_visual_desc, className='mb-2 text-muted', id='routes-graph-desc', style={'fontSize': '0.85em'}), 
#         html.Span(children=[
            
#             html.Small('Carrier Selection: ', className='text-muted mx-2 mt-1 mb-2'),
#             dbc.Select(id='routes-graph-mini-select', size='sm', options=routes_polars_carrier_list, class_name='routes-graph-util-select')
        
#         ], className='routes-graph-util-span mb-2'),
#         dcc.Graph(id='routes-graph', style={'height':'48vh'}, figure=routes_bar_figure)