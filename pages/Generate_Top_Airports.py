import polars as pl
import dash_bootstrap_components as dbc
from dash import html, dcc
import plotly_express as px
import dash

import plotly.subplots as sp




def generateAirportsTopTen(selected_viz, selected_airport, sqlite_path):

    airport_visual_desc = 'This is a test statement for the Airports Top 10 Destinations and Sources.'

    airports_passenger_flights_query = f"""

        with a as(
        select DEST_AIRPORT_ID,
        DEST_AIRPORT_NAME,
        ORIGIN_AIRPORT_ID, 
        ORIGIN_AIRPORT_NAME,
        SUM(CAST([PASSENGERS] as int)) as [ARRIVING PASSENGERS]
        from [T100_SEGMENT_ALL_CARRIER_2023_AIRPORTS_LOOKUP]
        where CAST([Passengers] as INT) > 0 
        and CAST([DEPARTURES_PERFORMED] AS int) > 0
        and [DEST_AIRPORT_NAME] = '{selected_airport}'
        group by DEST_AIRPORT_ID, DEST_AIRPORT_NAME, ORIGIN_AIRPORT_ID, ORIGIN_AIRPORT_NAME
        ),

        totals as (
        select a.[DEST_AIRPORT_ID], 
        a.[DEST_AIRPORT_NAME], 
        a.[ORIGIN_AIRPORT_ID], 
        a.[ORIGIN_AIRPORT_NAME],
        a.[ARRIVING PASSENGERS],
        ROW_NUMBER () over (partition by a.[DEST_AIRPORT_ID] order by a.[ARRIVING PASSENGERS] DESC) as [ORIGIN AIRPORT RANKING]
        from a),

        carrier_dump as (
        
        select DEST_AIRPORT_ID, 
        ORIGIN_AIRPORT_ID,
        UNIQUE_CARRIER_NAME, 
        SUM(CAST([PASSENGERS] AS INT)) as [CARRIER TOTAL PASSENGERS]
        from [T100_SEGMENT_ALL_CARRIER_2023_AIRPORTS_LOOKUP] x

        where CAST([Passengers] as INT) > 0 
        and CAST([DEPARTURES_PERFORMED] AS int) > 0
        and [DEST_AIRPORT_NAME] = '{selected_airport}'
        group by DEST_AIRPORT_ID, ORIGIN_AIRPORT_ID, UNIQUE_CARRIER_NAME

        )


        select t.[DEST_AIRPORT_NAME], 
        t.[ORIGIN_AIRPORT_NAME], 
        SUM(CAST(c.[CARRIER TOTAL PASSENGERS] AS INT)) as [TOTAL_PASSENGERS]
        from totals t
        inner join carrier_dump c
        on t.DEST_AIRPORT_ID = c.DEST_AIRPORT_ID and t.ORIGIN_AIRPORT_ID = c.ORIGIN_AIRPORT_ID
        where CAST(t.[ORIGIN AIRPORT RANKING] as INT) <= 10

        GROUP BY t.[DEST_AIRPORT_NAME], 
        t.[ORIGIN_AIRPORT_NAME]

        order by SUM(CAST(c.[CARRIER TOTAL PASSENGERS] AS INT)) desc
        ;

    """

    
    airports_polars = pl.read_database_uri(query=airports_passenger_flights_query, engine='adbc', uri=sqlite_path)

    h_bar_figure = px.bar(airports_polars, x='TOTAL_PASSENGERS', y='ORIGIN_AIRPORT_NAME',text_auto='0.3s')

    h_bar_figure.update_traces(textfont_size=10, marker={"cornerradius":5})
    
    h_bar_figure.update_layout(showlegend=False, yaxis={'tickfont': {'size': 10}}, margin={'l':10, 'r': 10, 't': 10, 'b': 10})

    return_children = [

        html.H2(f"{selected_viz}", id='airports-graph-header', style={'marginBottom': '0.1em'}),
        html.P(f'({selected_airport})', id='airports-graph-subheader', className='text-muted', style={'marginBottom': '0.2em'}),
        html.Hr(className='my-2'),
        html.P(airport_visual_desc, className='mb-2 text-muted', id='airports-graph-desc', style={'fontSize': '0.85em'}), 
        dcc.Graph(id='airports-graph', style={'height':'26vh'}, figure=h_bar_figure)

    ]

    return return_children