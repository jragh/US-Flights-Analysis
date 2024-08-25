import polars as pl
import dash_bootstrap_components as dbc
from dash import html, dcc
import plotly_express as px


def generateScatterCarrierRouteLoadFactor(selected_viz, selected_carrier, sqlite_path, min_flights = 200):

    routes_visual_desc = """Displays the Load Factor for all routes for a given carrier based on the number of flights the carrier operates on the route.
    If no carrier is selected, than load factor for each carrier against the number of flights is presented for each carrier. 
    In Carrier specific view, only routes with at least 20 departures performed are shown. 
    Only carriers with at least 200 departures performed are shown."""

    min_flights_str = str(min_flights)

    ## This is where we pull the SQL query for the polars dataframe
    ## This section will include both queries for all carriers, and specific carrier

    ## All Carriers Query ##
    if (selected_carrier is None or selected_carrier.strip() == ''): 

        routes_carriers_load_factor_query = f"""
        
        select UNIQUE_CARRIER_NAME as [Carrier Name],
        sum(cast(passengers as int)) as [Total Passengers],
        sum(cast(seats as int)) as [Total Seats],
        sum(cast(departures_performed as int)) as [Total Flights],
        sum(cast(passengers as float)) / sum(cast(seats as float)) as [Load Factor Ratio]

        FROM T100_SEGMENT_ALL_CARRIER_2023_AIRPORTS_LOOKUP

        where CAST(DEPARTURES_PERFORMED AS INT) > 0
        and CAST(PASSENGERS AS INT) > 0
        and DEST_AIRPORT_NAME <> ORIGIN_AIRPORT_NAME
        AND CAST(SEATS AS INT) > 0

        group by UNIQUE_CARRIER_NAME
        having sum(cast(departures_performed as int)) >= {min_flights_str}
        ORDER BY sum(cast(departures_performed as int)) DESC;
        
        """

        routes_polars = pl.read_database_uri(query=routes_carriers_load_factor_query, engine='adbc', uri=sqlite_path)

        scatter_figure = px.scatter(routes_polars, x="Total Flights", y = "Load Factor Ratio", 
                                    custom_data=["Total Passengers", "Total Seats", "Carrier Name"], log_x=True, marginal_y="violin")
        


    ## Specific Carrier Query ##
    else:

        routes_carriers_load_factor_query = f"""select UNIQUE_CARRIER_NAME, 
        CASE 
            WHEN DEST || ': ' || DEST_CITY_NAME > ORIGIN || ': ' || ORIGIN_CITY_NAME then DEST || ': ' || DEST_CITY_NAME || ' & ' || ORIGIN || ': ' || ORIGIN_CITY_NAME
            WHEN ORIGIN || ': ' || ORIGIN_CITY_NAME > DEST || ': ' || DEST_CITY_NAME THEN ORIGIN || ': ' || ORIGIN_CITY_NAME || ' & ' || DEST || ': ' || DEST_CITY_NAME
            ELSE ORIGIN || ': ' || ORIGIN_CITY_NAME || ' & ' || DEST || ': ' || DEST_CITY_NAME 
        END AS [Route Airport Pair],
        SUM(CAST(SEATS as INT)) as [Total Seats],
        SUM(CAST(PASSENGERS as INT)) as [Total Passengers],
        SUM(CAST(DEPARTURES_PERFORMED AS INT)) AS [Total Flights],
        SUM(CAST(PASSENGERS as float)) / SUM(CAST(SEATS as float)) as [Load Factor Ratio]
        FROM T100_SEGMENT_ALL_CARRIER_2023_AIRPORTS_LOOKUP
        where CAST(DEPARTURES_PERFORMED AS INT) > 0
        and CAST(PASSENGERS AS INT) > 0
        and DEST_AIRPORT_NAME <> ORIGIN_AIRPORT_NAME
        AND CAST(SEATS AS INT) > 0
        AND UNIQUE_CARRIER_NAME = '{selected_carrier}'

        group by UNIQUE_CARRIER_NAME, 
        CASE 
            WHEN DEST || ': ' || DEST_CITY_NAME > ORIGIN || ': ' || ORIGIN_CITY_NAME then DEST || ': ' || DEST_CITY_NAME || ' & ' || ORIGIN || ': ' || ORIGIN_CITY_NAME
            WHEN ORIGIN || ': ' || ORIGIN_CITY_NAME > DEST || ': ' || DEST_CITY_NAME THEN ORIGIN || ': ' || ORIGIN_CITY_NAME || ' & ' || DEST || ': ' || DEST_CITY_NAME
            ELSE ORIGIN || ': ' || ORIGIN_CITY_NAME || ' & ' || DEST || ': ' || DEST_CITY_NAME 
        END

        having SUM(CAST(DEPARTURES_PERFORMED AS INT)) > 20

        ORDER BY SUM(CAST(DEPARTURES_PERFORMED AS INT)) DESC, SUM(CAST(SEATS AS INT)) DESC;
        """
        
        routes_polars = pl.read_database_uri(query=routes_carriers_load_factor_query, engine='adbc', uri=sqlite_path)

        scatter_figure = px.scatter(routes_polars, x="Total Flights", y = "Load Factor Ratio", 
                                    log_x= False, custom_data=["Total Passengers", "Total Seats", "Route Airport Pair"], marginal_y="violin",
                                    opacity=0.7)
        
        scatter_figure.update_traces(marker={"line": {'width': 0.75}, 'size': 10, 'color': '#E89C31'}, hovertemplate = '''
                                    <b>%{customdata[2]}</b><br><br>
                                    <b>Load Factor:</b> %{y:.2%}<br>
                                    <b>Total Passengers:</b> %{customdata[0]:,3s}<br>
                                    <b>Total Seats:</b> %{customdata[1]:,3s}<br>
                                    <b>Total Flights:</b> %{x:,3f}<br>''',
                                    )
        
        scatter_figure.update_layout(yaxis={'tickfont': {'size': 10}}, margin={'l':10, 'r': 10, 't': 10, 'b': 8},
                               plot_bgcolor='#f9f9f9', paper_bgcolor="#f9f9f9",
                               showlegend=False)
    
        scatter_figure.update_yaxes(title='Route Load Factor', showline=False, showgrid=True, showticklabels=True, tickwidth=2,
                              gridcolor='rgba(60, 60, 60, 0.15)', row=1, col=1)
    
        scatter_figure.update_xaxes(title='Total Departures Performed',
                              showgrid=True, showline=True, linewidth=2.5, linecolor='rgb(180, 180, 180)',
                              showticklabels=True, tickwidth=2, gridcolor="rgba(60, 60, 60, 0.15)", row=1, col=1)
        
        return_children = [

            html.H2(f"{selected_viz}", id='routes-graph-header', style={'marginBottom': '0.1em'}),
            html.P(f'Selected Airline Carrier: {selected_carrier}', id='routes-graph-subheader', className='text-muted', style={'marginBottom': '0.2em'}),
            html.Hr(className='my-2'),
            html.P(routes_visual_desc, className='mb-2 text-muted', id='routes-graph-desc', style={'fontSize': '0.85em'}), 
            dcc.Graph(id='routes-graph', style={'height':'54vh'}, figure=scatter_figure)

        ]

        return return_children


    




