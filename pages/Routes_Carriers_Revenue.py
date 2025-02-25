import polars as pl
import dash_bootstrap_components as dbc
from dash import html, dcc
import plotly_express as px

def generateRouteCarrierRevenue(selected_viz, selected_airport_1, selected_airport_2, sqlite_path):

    routes_visual_desc = """Displays the Estimated Revenue for the Airport Pair by associated carriers. 
    Larger carriers shown individually, smaller carriers with estimated revenue less than 1% will be lumped into 'Other Carriers'.
    Estimated Revenue based on Average Fare for the given markets."""


    ## This is the SQL query to pull the estimated revenue information for 2 airports ##
    ## This query is also saved in the associated .sql file ##
    routes_carriers_revenue_query = f"""

        with cte as (
 
        select * from T100_SEGMENT_ALL_CARRIER_2023_FARES
        where ORIGIN_AIRPORT_NAME = '{selected_airport_1.replace("'", "''")}'
        AND DEST_AIRPORT_NAME = '{selected_airport_2.replace("'", "''")}'
        and CAST(PASSENGERS AS real) > 0 and CAST(DEPARTURES_PERFORMED AS real) > 0

        UNION

        select * from T100_SEGMENT_ALL_CARRIER_2023_FARES
        where ORIGIN_AIRPORT_NAME = '{selected_airport_2.replace("'", "''")}'
        AND DEST_AIRPORT_NAME = '{selected_airport_1.replace("'", "''")}'
        and CAST(PASSENGERS AS real) > 0 and CAST(DEPARTURES_PERFORMED AS real) > 0

        )
        ,

        split_rank as (

        select UNIQUE_CARRIER_NAME, 
        SUM(CAST(PASSENGERS AS real) * CAST(AVERAGE_FARE AS double precision)) as "Aggregate Revenue",
        CASE WHEN SUM(CAST(PASSENGERS AS real) * CAST(AVERAGE_FARE AS double precision)) < ((select SUM(CAST(PASSENGERS AS real) * CAST(AVERAGE_FARE AS double precision)) from cte) / 100.00)
        then 'Other Carriers' else UNIQUE_CARRIER_NAME end as "UNIQUE_CARRIER_SIMPLIFIED"
        from cte
        group by UNIQUE_CARRIER_NAME

        )

        select cte.UNIQUE_CARRIER_NAME, 
        sr."UNIQUE_CARRIER_SIMPLIFIED" as "Carrier Name",
        aclu.description as "AIRCRAFT_TYPE",
        AVG(cast(cte.AVERAGE_FARE as double precision)) AS "Average Fare", 
        SUM(CAST(cte.PASSENGERS AS real) * CAST(cte.AVERAGE_FARE AS double precision)) as "Total Revenue",
        SUM(CAST(cte.PASSENGERS AS real)) as "Total Passengers",
        SUM(CAST(cte.DEPARTURES_PERFORMED AS real)) AS "Total Flights"
        from cte
        
        left join split_rank sr
        on cte.UNIQUE_CARRIER_NAME = sr.UNIQUE_CARRIER_NAME

        left join T100_SEGMENT_AIRCRAFT_TYPE_LOOKUP_2023 aclu
        on cte.AIRCRAFT_TYPE = aclu.code

        GROUP BY cte.UNIQUE_CARRIER_NAME,
        sr."Aggregate Revenue",
        sr."UNIQUE_CARRIER_SIMPLIFIED",
        aclu.description
        
        ORDER BY CAST(sr."Aggregate Revenue" as double precision) asc
        
    """

    routes_polars = pl.read_database_uri(query=routes_carriers_revenue_query, engine='adbc', uri=sqlite_path)

    h_bar_figure = px.bar(routes_polars, x='Total Revenue', y='Carrier Name',color='AIRCRAFT_TYPE', text_auto='0.3s',
                          orientation='h', barmode='stack', color_discrete_sequence=px.colors.sequential.Cividis,
                          custom_data=['Total Passengers', 'Total Flights', 'Average Fare'])
    
    h_bar_figure.update_traces(textfont_size=10, marker={"cornerradius":4}, textposition='inside', textangle=0,
                               hovertemplate='''<b>%{y}</b><br><br>Aircraft Type: %{data.name}<br>Total Revenue: %{x:$.3s}<extra></extra><br>Total Passengers: %{customdata[0]:,.3s}<br>Total Flights: %{customdata[1]:,.0f}<br>Average Fare Cost: %{customdata[2]:$.3s}''', cliponaxis=False,
                               texttemplate='%{x:$.3s}')
    
    h_bar_figure.update_layout(yaxis={'tickfont': {'size': 10}}, margin={'l':10, 'r': 10, 't': 10, 'b': 8},
                               plot_bgcolor='#f9f9f9', paper_bgcolor="#f9f9f9",
                               showlegend=False)
    
    h_bar_figure.update_yaxes(type='category', title=None, linewidth=2.5, showgrid=False, 
                              linecolor='rgb(180, 180, 180)', ticksuffix="  ", categoryorder='total ascending')
    
    h_bar_figure.update_xaxes(title='Total Pair Revenue',
                              showgrid=True, zeroline=False, showline=False, 
                              showticklabels=True, tickwidth=2, gridcolor="rgba(60, 60, 60, 0.15)")
    
    return_children = [

        html.H2(f"{selected_viz}", id='routes-graph-header', style={'marginBottom': '0.1em'}),
        html.P(f'{selected_airport_1} & {selected_airport_2}', id='routes-graph-subheader', className='text-muted', style={'marginBottom': '0.2em'}),
        html.Hr(className='my-2'),
        html.P(routes_visual_desc, className='mb-2 text-muted', id='routes-graph-desc', style={'fontSize': '0.85em'}), 
        dcc.Graph(id='routes-graph', style={'height':'54vh'}, figure=h_bar_figure)

    ]

    return return_children