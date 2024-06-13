import polars as pl
import dash_bootstrap_components as dbc
from dash import html, dcc
import plotly_express as px
import dash

import plotly.subplots as sp




def generateAirportsTopTen(selected_viz, selected_airport, sqlite_path):

    airport_visual_desc = 'Displays the Top 10 Connected Airports to the selected airport based on the total incoming and outgoing passengers.'

    airports_passenger_flights_query = f"""

        with origins as (

        select [ORIGIN_AIRPORT_NAME],
        SUM(CAST([PASSENGERS] AS INT)) as [TOTAL ORIGIN PASSENGERS]
        from T100_SEGMENT_ALL_CARRIER_2023_AIRPORTS_LOOKUP
        where CAST([PASSENGERS] as int) > 0 
        and CAST([DEPARTURES_PERFORMED] as int) > 0
        and [DEST_AIRPORT_NAME] = '{selected_airport}'
        group by [ORIGIN_AIRPORT_NAME]),

        destinations as (
        
        select [DEST_AIRPORT_NAME],
        SUM(CAST([PASSENGERS] AS INT)) as [TOTAL DEST PASSENGERS]
        from T100_SEGMENT_ALL_CARRIER_2023_AIRPORTS_LOOKUP
        where CAST([PASSENGERS] as int) > 0 
        and CAST([DEPARTURES_PERFORMED] as int) > 0
        and [ORIGIN_AIRPORT_NAME] = '{selected_airport}'
        group by [DEST_AIRPORT_NAME]

        ),

        window as (
        
        select COALESCE(o.[ORIGIN_AIRPORT_NAME], d.[DEST_AIRPORT_NAME]) as [AIRPORT NAME],
        COALESCE(cast(o.[TOTAL ORIGIN PASSENGERS] as int), 0) as [ARRIVING PASSENGERS],
        COALESCE(cast(d.[TOTAL DEST PASSENGERS] as int), 0) as [DEPARTING PASSENGERS],
        (COALESCE(cast(o.[TOTAL ORIGIN PASSENGERS] as int), 0) + COALESCE(cast(d.[TOTAL DEST PASSENGERS] as int), 0)) as [TOTAL PASSENGERS],

        ROW_NUMBER() OVER (order by (COALESCE(cast(o.[TOTAL ORIGIN PASSENGERS] as int), 0) + COALESCE(cast(d.[TOTAL DEST PASSENGERS] as int), 0)) desc) as [PASSENGER RANKING]


        from origins o
        FULL OUTER JOIN destinations d
        on o.[ORIGIN_AIRPORT_NAME] = d.[DEST_AIRPORT_NAME])

        select * from window
        where [PASSENGER RANKING] <= 10
        order by CAST([TOTAL PASSENGERS] as int) asc;

    """

    
    airports_polars = pl.read_database_uri(query=airports_passenger_flights_query, engine='adbc', uri=sqlite_path)

    airports_polars = airports_polars.with_columns(pl.col('AIRPORT NAME').str.replace(r'\: ', '<br>').alias('AIRPORT NAME SPLIT'))

    h_bar_figure = px.bar(airports_polars, x=['ARRIVING PASSENGERS', 'DEPARTING PASSENGERS'], y='AIRPORT NAME SPLIT',text_auto='0.3s',
                          orientation='h', barmode='stack')

    h_bar_figure.update_traces(textfont_size=10, marker={"cornerradius":4}, textposition='inside', textangle=0,
                               hovertemplate='<b>%{y}</b><br><br>%{data.name}: %{x:.3s}<extra></extra>')
    
    h_bar_figure.update_layout(yaxis={'tickfont': {'size': 10}}, margin={'l':10, 'r': 10, 't': 10, 'b': 8},
                               plot_bgcolor='#f9f9f9', paper_bgcolor="#f9f9f9",
                               legend={'font': {'size': 10}, 'orientation':'h'})

    h_bar_figure.update_legends(yanchor="bottom", y=1.02, xanchor= 'right', x= 0.5, title=None)

    h_bar_figure.update_yaxes(type='category', title=None, linewidth=2.5, showgrid=False, 
                              linecolor='rgb(180, 180, 180)', ticksuffix="  ")
    
    h_bar_figure.update_xaxes(title='Total Passengers',
                              showgrid=True, zeroline=False, showline=False, 
                              showticklabels=True, tickwidth=2, gridcolor="rgba(60, 60, 60, 0.15)")

    h_bar_figure.update_traces(marker_color="#0B2838", selector={"name": "ARRIVING PASSENGERS"})

    h_bar_figure.update_traces(marker_color="#62B3E0", selector={"name": "DEPARTING PASSENGERS"})            


    return_children = [

        html.H2(f"{selected_viz}", id='airports-graph-header', style={'marginBottom': '0.1em'}),
        html.P(f'({selected_airport})', id='airports-graph-subheader', className='text-muted', style={'marginBottom': '0.2em'}),
        html.Hr(className='my-2'),
        html.P(airport_visual_desc, className='mb-2 text-muted', id='airports-graph-desc', style={'fontSize': '0.85em'}), 
        dcc.Graph(id='airports-graph', style={'height':'54vh'}, figure=h_bar_figure)

    ]

    return return_children