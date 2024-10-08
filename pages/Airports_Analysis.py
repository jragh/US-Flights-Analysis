import polars as pl
from dash import html, dcc, Input, Output, State, callback, no_update
import dash_bootstrap_components as dbc
import plotly_express as px
import os

import dash

from .AirportAnalyticsText import airport_text
from .Airports_Analysis_Cards import generateSummaryCard

from .Generate_Top_Airports import generateAirportsTopTen

dash.register_page(__name__, path='/AirportAnalytics')

textResults = airport_text()

sqlite_path = os.environ['POSTGRES_URI_LOCATION']

airports_df = pl.read_database_uri(engine='adbc', uri=sqlite_path, query = """
                                select b.DESCRIPTION as "CITY AIRPORT NAME", 
                                count(*) as "NUMBER OF RECORDS"
                                from public.T100_SEGMENT_ALL_CARRIER_2023 a
                                left join public.T100_AIRPORT_CODE_LOOKUP_2023 b
                                on a.ORIGIN_AIRPORT_ID = b.CODE
                                where CAST(a.PASSENGERS AS numeric) > 0
                                and CAST(a.SEATS AS numeric) > 0
                                AND CAST(a.DEPARTURES_PERFORMED as numeric) > 0
                                and b.DESCRIPTION is not null
                                and a.ORIGIN_COUNTRY_NAME LIKE 'United States'
                                group by b.DESCRIPTION
                                ORDER BY b.DESCRIPTION ASC;""")

airport_filter_list = sorted([val['CITY AIRPORT NAME'] for val in airports_df.select(['CITY AIRPORT NAME']).unique().to_dicts()])

airports_visual_list = ["Routes vs Flights (Scatter)", 'Airport Summary Treemap', 'Airport Monthly Passengers & Flights', 'Top 10 Connected Airports By Passengers']


layout = html.Div([dbc.Container([
    
    dbc.Row([

        dbc.Col(children = textResults,
                 id='sidebar', className = 'textSidebar',width = 12, lg = 4, md =12, xl = 4, xxl = 4, sm = 12, align='start'),

        dbc.Col(children=[

            dbc.Row([dbc.Col([

                dbc.Row([
                    dbc.Col([
                        
                        dbc.Card(
                            dbc.CardBody(
                                [
                                    dbc.Label('Visual Selection: '),
                                    html.Div([dcc.Dropdown(value=airports_visual_list[1], options=airports_visual_list, multi=False, searchable=True, clearable=False, 
                                                           placeholder='Select a visual here...', id='airport-viz-selection',
                                                           style={'fontSize': '12px'})], className='dbc mb-2')
                                ], className='pt-3 pb-2'
                            ), className='bg-light text-dark border rounded-3'
                        )

                    ], width=12, md=4, id='carrier-selection-col', className='mb-2'),

                    dbc.Col([

                        dbc.Card(
                            dbc.CardBody([
                                dbc.Label('Airport Selection:  '),
                                html.Div([dcc.Dropdown(value='', options=airport_filter_list, multi=False, searchable=True, clearable=True, 
                                                           placeholder='Select an Airport from here...', id='airport-ap-selection',
                                                           style={'fontSize': '12px'})], className='dbc mb-2')
                            ], className='pt-3 pb-2'
                            ), className='bg-light text-dark border rounded-3'
                        )

                    ], width=12, md=8, id='visual-selection-col', className='mb-2')
                ]),

                

                
                

                ## Creating Graph Component for quick analytics ##
                dbc.Spinner([
                    html.Div([
                        html.H2('', id='airports-graph-header'),
                        html.Hr(className='my-2'),
                        html.P('', className='mb-2', id='airports-graph-desc'),

                        dcc.Graph(id='airports-graph', style={'display': 'block'})
                    ], className='p-4 bg-light text-dark border rounded-3', id='airports-visual-div')
                ], show_initially=True, spinner_style={'height': '3rem', 'width': '3rem'})


                

            ])], align="center")
            
            

        ], id='airports-graph_section', width = 12, lg = 8, md = 12, xl = 8, xxl = 8, sm=12, class_name='px-2')

    ])
], fluid=True, className='mr-4 ml-4')], style={'margin': 0})


@callback(
    Output(component_id='airports-visual-div', component_property='children'),
    [Input(component_id='airport-viz-selection', component_property='value'),
     Input(component_id='airport-ap-selection', component_property='value')
     ]
)
def select_airport_visual(selected_viz, selected_airport):

    if selected_viz == airports_visual_list[0]:

        airport_visual_desc = "Highlights the number of passengers transported by a given carrier vs. the amount of cities that are reachable using that carrier. If no airport is selected, then the analysis is for the entire United States. Size of bubble shows number of flights that departed from the given airport."

        ## If Statement for scatterplot when there is no airport selected ##
        if selected_airport is None or selected_airport.strip() == '':

            airports_query = """
            select a.UNIQUE_CARRIER_NAME as "UNIQUE CARRIER NAME",
            SUM(CAST(a.PASSENGERS AS real)) AS "TOTAL PASSENGERS",
            SUM(CAST(a.DEPARTURES_PERFORMED as real)) AS "TOTAL DEPARTED FLIGHTS",
            CAST(COUNT(DISTINCT a.DEST_AIRPORT_ID) as real) as "TOTAL DESTINATION AIRPORTS"
            from T100_SEGMENT_ALL_CARRIER_2023 a
            left join T100_AIRPORT_CODE_LOOKUP_2023 b
            on a.ORIGIN_AIRPORT_ID = b.CODE
            where CAST(a.PASSENGERS AS numeric) > 0
            and CAST(a.SEATS AS numeric) > 0
            AND CAST(a.DEPARTURES_PERFORMED as numeric) > 0
            and b.DESCRIPTION IS NOT NULL
            AND a.ORIGIN_COUNTRY_NAME = 'United States'
            GROUP BY a.UNIQUE_CARRIER_NAME
            order by a.UNIQUE_CARRIER_NAME
            """

            airports_polars = pl.read_database_uri(engine='adbc', query=airports_query, uri=sqlite_path)

            scatter_figure = px.scatter(
                airports_polars.select(['UNIQUE CARRIER NAME', 'TOTAL PASSENGERS', 'TOTAL DEPARTED FLIGHTS', 'TOTAL DESTINATION AIRPORTS']),
                x='TOTAL DESTINATION AIRPORTS',
                y='TOTAL DEPARTED FLIGHTS',
                size='TOTAL PASSENGERS',
                custom_data=['UNIQUE CARRIER NAME', 'TOTAL PASSENGERS'],
                size_max=50,
                opacity=0.7
            )

            scatter_figure.update_layout(margin={'r': 20, 't': 30, 'b':40}, 
                                         hoverlabel={'font': {'color': '#0B2838'},'bgcolor':'#E89C31'}, 
                                         plot_bgcolor='white',
                                        yaxis={'tickfont': {'size': 10}},
                                        xaxis={'tickfont': {'size': 10}})  

            scatter_figure.update_traces(hovertemplate="<b>%{customdata[0]}</b><br><br><b>Destination Airports: </b>%{x}<br><b>Departed Flights: </b>%{y:,.0f}<br><br><b><i>Passengers: %{customdata[1]:,.0f}</i></b>")

            scatter_figure.update_traces(marker={'color': '#0B2838'}, line={'width': 1, "color": '#E89C31'})

            scatter_figure.update_xaxes(linewidth=2.5, showgrid=False, linecolor='rgb(204, 204, 204)')
            
            scatter_figure.update_yaxes(showgrid=True, zeroline=False, showline=False, showticklabels=True, tickwidth=2, gridcolor="rgba(30, 63, 102, 0.15)")

            return_children = [

                html.H2(f"{selected_viz}: All Airports", id='airports-graph-header', style={'marginBottom': '0.1em'}),
                html.P('(All Airports in US)', id='airports-graph-subheader', className='text-muted', style={'marginBottom': '0.2em'}),
                html.Hr(className='my-2'),
                html.P(airport_visual_desc, className='mb-2 text-muted', id='airports-graph-desc', style={'fontSize': '0.85em'}),

                dcc.Graph(id='airports-graph', style={'height': '50vh'}, figure=scatter_figure)

            ]

            return return_children

        
        else:

            airports_query = f"""
                SELECT "ORIGIN AIRPORT NAME", 
                "UNIQUE CARRIER NAME", 
                CAST("TOTAL PASSENGERS" as real) as "TOTAL PASSENGERS", 
                CAST("TOTAL DEPARTED FLIGHTS" AS real) as "TOTAL DEPARTED FLIGHTS", 
                CAST("TOTAL DESTINATION AIRPORTS" AS real) as "TOTAL DESTINATION AIRPORTS"
                FROM t100_origin_airports_aggregate
                where "ORIGIN AIRPORT NAME" = '{selected_airport.replace("'", "''")}'
            """

            airports_polars = pl.read_database_uri(engine='adbc', query=airports_query, uri=sqlite_path)

            scatter_figure = px.scatter(airports_polars.select(["ORIGIN AIRPORT NAME", "UNIQUE CARRIER NAME", "TOTAL PASSENGERS", "TOTAL DEPARTED FLIGHTS", "TOTAL DESTINATION AIRPORTS"]),
                                        x='TOTAL DESTINATION AIRPORTS',
                                        y='TOTAL DEPARTED FLIGHTS',
                                        size="TOTAL PASSENGERS",
                                        custom_data=['UNIQUE CARRIER NAME', 'TOTAL PASSENGERS'],
                                        size_max=50,
                                        opacity=0.7)
            
            scatter_figure.update_layout(margin={'r': 20, 't': 30, 'b':40}, 
                                         hoverlabel={'font': {'color': '#0B2838'},'bgcolor':'#E89C31'}, 
                                         plot_bgcolor='#f9f9f9', paper_bgcolor="#f9f9f9",
                                        yaxis={'tickfont': {'size': 10}},
                                        xaxis={'tickfont': {'size': 10}})  

            scatter_figure.update_traces(hovertemplate="<b>%{customdata[0]}</b><br><br><b>Destination Airports: </b>%{x}<br><b>Departed Flights: </b>%{y:,.0f}<br><br><b><i>Passengers: %{customdata[1]:,.0f}</i></b>")

            scatter_figure.update_traces(marker={'color': '#0B2838'}, line={'width': 1, "color": '#E89C31'})

            scatter_figure.update_xaxes(linewidth=2.5, showgrid=False, linecolor='rgb(180, 180, 180)', zeroline=False)
            
            scatter_figure.update_yaxes(showgrid=True, zeroline=False, showline=False, showticklabels=True, tickwidth=2, gridcolor="rgba(60, 60, 60, 0.15)")

            return_children = [

                html.H2(f"{selected_viz}", id='airports-graph-header', style={'marginBottom': '0.1em'}),
                html.P(f"({selected_airport})", id='airports-graph-subheader', className='text-muted', style={'marginBottom': '0.2em'}),
                html.Hr(className='my-2'),
                html.P(airport_visual_desc, className='mb-2 text-muted', id='airports-graph-desc', style={'fontSize': '0.85em'}),

                dcc.Graph(id='airports-graph', style={'height': '50vh'}, figure=scatter_figure)

            ]

            return return_children
        
    
    elif selected_viz == airports_visual_list[1]:

        airport_visual_desc = 'Treemap displaying airline carriers operating at the given airport based on the number of departing passengers from that airport.'

        if selected_airport is None or selected_airport.strip() == '' or selected_airport == '':

            airports_query = """
            select a.UNIQUE_CARRIER_NAME as "UNIQUE CARRIER NAME",
            SUM(CAST(a.PASSENGERS AS real)) AS "TOTAL PASSENGERS",
            SUM(CAST(a.DEPARTURES_PERFORMED AS real)) AS "TOTAL DEPARTED FLIGHTS",
            CAST(COUNT(DISTINCT a.DEST_AIRPORT_ID) as real) as "TOTAL DESTINATION AIRPORTS"
            from T100_SEGMENT_ALL_CARRIER_2023 a
            left join T100_AIRPORT_CODE_LOOKUP_2023 b
            on a.ORIGIN_AIRPORT_ID = b.CODE
            where CAST(a.PASSENGERS AS real) > 0
            and CAST(a.SEATS AS real) > 0
            AND CAST(a.DEPARTURES_PERFORMED as real) > 0
            and b.DESCRIPTION IS NOT NULL
            AND a.ORIGIN_COUNTRY_NAME = 'United States'
            GROUP BY a.UNIQUE_CARRIER_NAME
            order by a.UNIQUE_CARRIER_NAME
            """

            airports_unique_destination_query = """
            select COUNT(distinct c.DESCRIPTION) as "TOTAL DESTINATION AIRPORTS"
            FROM T100_SEGMENT_ALL_CARRIER_2023 a
            left join T100_AIRPORT_CODE_LOOKUP_2023 b
            on a.ORIGIN_AIRPORT_ID = b.CODE
            left join T100_AIRPORT_CODE_LOOKUP_2023 c
            on a.DEST_AIRPORT_ID = c.CODE
            WHERE CAST(a.PASSENGERS AS real) > 0 
            AND CAST(DEPARTURES_PERFORMED AS real) > 0
            AND b.DESCRIPTION is not null
            AND a.ORIGIN_COUNTRY_NAME = 'United States'
            and c.DESCRIPTION IS NOT NULL
            """

            airports_polars = pl.read_database_uri(engine='adbc', query=airports_query, uri=sqlite_path)

            airports_unique_destinations_polars = pl.read_database_uri(engine='adbc', query=airports_unique_destination_query, uri=sqlite_path)

            ## TODO: Remap from Polars to SQL backend, update query to pull what is needed.
            airports_passenger_max = airports_polars.select(pl.sum('TOTAL PASSENGERS')).item()

            airports_departed_max = airports_polars.select(pl.sum('TOTAL DEPARTED FLIGHTS')).item()

            airports_carriers_unique = airports_polars.n_unique(subset=["UNIQUE CARRIER NAME"])

            airports_unique_destinations = airports_unique_destinations_polars.select('TOTAL DESTINATION AIRPORTS').row(0)[0]

            airports_polars = airports_polars.with_columns(pl.when(pl.col("TOTAL PASSENGERS") < (airports_passenger_max / 100))
                                         .then(pl.lit('Other Carriers')).otherwise(pl.col("UNIQUE CARRIER NAME")).alias('UNIQUE CARRIER SIMPLIFIED'))

            tree_figure=px.treemap(airports_polars, path=[px.Constant('All Carriers'), 'UNIQUE CARRIER SIMPLIFIED'], values='TOTAL PASSENGERS',
                                   custom_data=['UNIQUE CARRIER SIMPLIFIED', 'TOTAL PASSENGERS', 'TOTAL DEPARTED FLIGHTS', 'TOTAL DESTINATION AIRPORTS'],
                                   color='TOTAL PASSENGERS', color_continuous_scale=['#7CC6FE', '#0B2838'])
            
            tree_figure.update_traces(texttemplate="<b>%{customdata[0]}</b><br><br>Passengers: %{customdata[1]:,.0f} <br>Departed Flights: %{customdata[2]:,.0f}<br>Destinations: %{customdata[3]:,.0f}",
                                      root_color='#f9f9f9', marker={'cornerradius': 5})

            tree_figure.update_layout(margin={'t':0, 'b':0, 'l': 0, 'r': 0}, showlegend=False)

            tree_figure.update_coloraxes(showscale=False)


            return_children = [

                html.H3(f"{selected_viz}: All Airports", id='airports-graph-header'),
                html.Hr(className='my-2'),
                html.P(airport_visual_desc, className='mb-2 text-muted', id='airports-graph-desc'),

                dbc.Row([

                    dbc.Col([

                        dbc.CardGroup([

                            generateSummaryCard('Total Passengers', '#E89C31', "{:,.0f}".format(airports_passenger_max)),

                            generateSummaryCard('Total Departed Flights', '#E89C31', "{:,.0f}".format(airports_departed_max)),

                            generateSummaryCard('Total Carriers', '#E89C31', "{:,.0f}".format(airports_carriers_unique)),

                            generateSummaryCard('Total Flight Destinations', '#E89C31', "{:,.0f}".format(airports_unique_destinations))

                        ], style={"columnGap": "1em"})

                    ])

                ], style={'marginBottom': '1em'}),

                dbc.Row([

                    dcc.Graph(figure=tree_figure, style={'minHeight': '42vh'})

                ])

            ]

            return return_children
        
        else:

            ## SQL Queries to pull airports information ##
            airports_query = f"""
            select "ORIGIN AIRPORT NAME",
            "UNIQUE CARRIER NAME",
            CAST("TOTAL PASSENGERS" AS real) as "TOTAL PASSENGERS",
            CAST("TOTAL DEPARTED FLIGHTS" as real) as "TOTAL DEPARTED FLIGHTS",
            CAST("TOTAL DESTINATION AIRPORTS" as real) as "TOTAL DESTINATION AIRPORTS"
            from T100_ORIGIN_AIRPORTS_AGGREGATE
            where "ORIGIN AIRPORT NAME" like '{selected_airport.replace("'", "''")}'
            """

            airports_unique_destination_query = f"""
            select COUNT(distinct c.DESCRIPTION) as "TOTAL DESTINATION AIRPORTS"
            FROM T100_SEGMENT_ALL_CARRIER_2023 a
            left join T100_AIRPORT_CODE_LOOKUP_2023 b
            on a.ORIGIN_AIRPORT_ID = b.CODE
            left join T100_AIRPORT_CODE_LOOKUP_2023 c
            on a.DEST_AIRPORT_ID = c.CODE
            WHERE CAST(a.PASSENGERS AS real) > 0 
            AND CAST(DEPARTURES_PERFORMED AS real) > 0
            AND b.DESCRIPTION is not null
            AND a.ORIGIN_COUNTRY_NAME = 'United States'
            and c.DESCRIPTION IS NOT NULL
            and b.DESCRIPTION like '{selected_airport.replace("'", "''")}'
            """

            ## Polars Queries to pull data from SQL database with queries defined above ##
            airports_polars = pl.read_database_uri(engine='adbc', query=airports_query, uri=sqlite_path)

            airports_unique_destinations_polars = pl.read_database_uri(engine='adbc', query=airports_unique_destination_query, uri=sqlite_path)

            ## Set up of Summary stats for Airport based on passengers, departed flights, unique carriers, destination airports ##
            airports_passenger_max = airports_polars.select(pl.sum('TOTAL PASSENGERS')).item()

            airports_departed_max = airports_polars.select(pl.sum('TOTAL DEPARTED FLIGHTS')).item()

            airports_carriers_unique = airports_polars.n_unique(subset=["UNIQUE CARRIER NAME"])

            airports_unique_destinations = airports_unique_destinations_polars.select('TOTAL DESTINATION AIRPORTS').row(0)[0]

            ## Add in Simplified Unique Carrier Column as 'Other Carriers' if carried less than 1 percent of passengers ##
            airports_polars = airports_polars.with_columns(pl.when(pl.col("TOTAL PASSENGERS") < (airports_passenger_max / 100))
                                         .then(pl.lit('Other Carriers')).otherwise(pl.col("UNIQUE CARRIER NAME")).alias('UNIQUE CARRIER SIMPLIFIED'))

            ## Tree figure definition ##
            tree_figure=px.treemap(airports_polars, path=[px.Constant('All Carriers'), 'UNIQUE CARRIER SIMPLIFIED'], values='TOTAL PASSENGERS',
                                   custom_data=['UNIQUE CARRIER SIMPLIFIED', 'TOTAL PASSENGERS', 'TOTAL DEPARTED FLIGHTS', 'TOTAL DESTINATION AIRPORTS'],
                                   color='TOTAL PASSENGERS', color_continuous_scale=['#7CC6FE', '#0B2838'])
            
            tree_figure.update_traces(texttemplate="<b>%{customdata[0]}</b><br><br>Passengers: %{customdata[1]:,.0f} <br>Departed Flights: %{customdata[2]:,.0f}<br>Destinations: %{customdata[3]:,.0f}",
                                      root_color='#f9f9f9', marker={'cornerradius': 5})

            tree_figure.update_layout(margin={'t':0, 'b':0, 'l': 0, 'r': 0}, showlegend=False)

            tree_figure.update_coloraxes(showscale=False)

            ## Final Return to display Tree Map Graph with headers ##
            return_children = [

                html.H2(f"{selected_viz}", id='airports-graph-header', style={'marginBottom': '0.1em'}),
                html.P(f'({selected_airport})', id='airports-graph-subheader', style={'marginBottom': '0.2em'}, className='text-muted'),
                html.Hr(className='my-2'),
                html.P(airport_visual_desc, className='mb-2 text-muted', id='airports-graph-desc', style={'fontSize': '0.85em'}),

                dbc.Row([

                    dbc.Col([

                        dbc.CardGroup([

                            generateSummaryCard('Total Passengers', '#E89C31', "{:,.0f}".format(airports_passenger_max)),

                            generateSummaryCard('Total Departed Flights', '#E89C31', "{:,.0f}".format(airports_departed_max)),

                            generateSummaryCard('Total Carriers', '#E89C31', "{:,.0f}".format(airports_carriers_unique)),

                            generateSummaryCard('Total Flight Destinations', '#E89C31', "{:,.0f}".format(airports_unique_destinations))

                        ], style={"columnGap": "1em"})

                    ])

                ], style={'marginBottom': '1em'}),

                dbc.Row([

                    dcc.Graph(figure=tree_figure, style={'minHeight': '40vh'})

                    

                ])

            ]

            return return_children
        
    elif selected_viz == 'Airport Monthly Passengers & Flights':

        months_text = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

        airport_visual_desc = '2 Stacked Barcharts which display the amount of passenger traffic (Passengers and Flights carrying passengers) an airport handles throughout the year. Split on a monthly basis.'

        if selected_airport is None or selected_airport.strip() == '':

            airports_passenger_flights_query = """
            select b.MONTH_NAME_SHORT as "MONTH", a.MONTH as "MONTH NUM", a.YEAR, 
            SUM(CAST(a.PASSENGERS AS real)) as "TOTAL PASSENGERS",
            SUM(CAST(a.DEPARTURES_PERFORMED AS real)) as "TOTAL FLIGHTS" 
            from T100_SEGMENT_ALL_CARRIER_2023 a
            left join MONTHS_LOOKUP b
            on a.MONTH = b.MONTH::text
            WHERE CAST(a.PASSENGERS AS real) > 0 
            AND CAST(a.DEPARTURES_PERFORMED AS real) > 0
            GROUP BY b.MONTH_NAME_SHORT, a.MONTH, a.YEAR
            order by CAST(a.MONTH as real) asc
            """

            airports_polars = pl.read_database_uri(query=airports_passenger_flights_query, uri=sqlite_path, engine='adbc')

            line_figure_passengers = px.line(airports_polars, x='MONTH', y='TOTAL PASSENGERS',
                                                 markers=True, line_shape='spline',
                                                 category_orders={'MONTH': months_text},
                                                 color_discrete_sequence=['#0B2838'])
            
            line_figure_flights = px.line(airports_polars, x='MONTH', y='TOTAL FLIGHTS',
                                          markers=True, line_shape='spline',
                                          category_orders={'MONTH': months_text},
                                          color_discrete_sequence=['#E89C31'])
            
            line_figure_flights.update_xaxes(type='category')

            line_figure_flights.update_traces(yaxis ="y2", showlegend=True, name='Total Flights')

            line_figure_passengers.update_yaxes(showgrid=True, zeroline=False, showline=False, showticklabels=True, tickwidth=2, gridcolor="rgba(30, 63, 102, 0.15)")

            line_figure_passengers.update_traces(showlegend=True, name='Total Passengers')
            
            line_figure_passengers.add_traces(list(line_figure_flights.select_traces())).update_layout(yaxis2={"overlaying":"y", "side":"right", 'rangemode': "normal", "title": "Total Flights"},
                                                                                                       yaxis1={'rangemode': 'normal', 'title': 'Total Passengers'})
            
            line_figure_passengers.update_xaxes(type='category', categoryorder='array', categoryarray=months_text, linewidth=2.5, showgrid=False, linecolor='rgb(180, 180, 180)')

            line_figure_passengers.update_layout(legend={
                'orientation':'h',
                'yanchor':"bottom",
                'y':1.02,
                'xanchor': 'center',
                'x': 0.5}, 
                legend_title_text = '<b>US Passenger & Flight Traffic</b>',
                xaxis_title=None,
                yaxis_tickfont={'size': 10},
                margin={'l':10, 'r': 10, 't': 10, 'b': 10},
                plot_bgcolor='#f9f9f9', paper_bgcolor="#f9f9f9",
                hovermode='closest')
            
            ## Update secondary y axis ticks ##
            line_figure_passengers.update_layout(yaxis2={"tickmode": 'sync', 'tickfont': {'size': 10}}, hovermode='x unified')

            ## Update Traces for hover template ##
            line_figure_passengers.update_traces(hovertemplate="%{y:.3s}")


            return_children = [

                html.H2(f"{selected_viz}", id='airports-graph-header', style={'marginBottom': '0.1em'}),
                html.P(f'(All Airports in United States)', id='airports-graph-subheader', className='text-muted', style={'marginBottom': '0.2em'}),
                html.Hr(className='my-2'),
                html.P(airport_visual_desc, className='mb-2 text-muted', id='airports-graph-desc', style={'fontSize': '0.85em'}),

                dcc.Graph(id='airports-graph', style={'height':'52vh'}, figure=line_figure_passengers)

            ]

            return return_children
        
        else:

            airports_passenger_flights_query = f"""
            SELECT "AIRPORT NAME", 
            "AIRPORT ID",
            "month" as "MONTH",
            "year" as "YEAR",
            "ARRIVING PASSENGERS"::real,
            "ARRIVING FLIGHTS"::real,
            "DEPARTING PASSENGERS"::real,
            "DEPARTING FLIGHTS"::real
            FROM t100_airport_arrivals_departures
            where "AIRPORT NAME" = '{selected_airport.replace("'", "''")}'"""

            airports_polars = pl.read_database_uri(query=airports_passenger_flights_query, uri=sqlite_path, engine='adbc')

            ## Bar Figure Setup for Passengers ##
            bar_figure_passengers = px.bar(airports_polars, x='MONTH', y=['ARRIVING PASSENGERS', 'DEPARTING PASSENGERS'],
                                           color_discrete_map={'ARRIVING PASSENGERS': '#0B2838', 'DEPARTING PASSENGERS': '#62B3E0'},
                                           text_auto='0.3s')
            
            bar_figure_passengers.update_yaxes(showgrid=True, zeroline=False, showline=False, showticklabels=True, tickwidth=2, gridcolor="rgba(30, 63, 102, 0.15)")

            bar_figure_passengers.update_layout(legend={
                'orientation':'h',
                'yanchor':"bottom",
                'y':1.02,
                'xanchor': 'center',
                'x': 0.5}, 
                legend_title_text = '<b>Total Passenger Traffic</b>',
                xaxis_title=None,
                yaxis_title="Total Passengers",
                yaxis_tickfont={'size': 10},
                margin={'l':10, 'r': 10, 't': 10, 'b': 10},
                plot_bgcolor='#f9f9f9', paper_bgcolor="#f9f9f9",
                hovermode='closest')
            
            ## Using <extra></extra> to get rid of secondary hovertemplate window ##
            bar_figure_passengers.update_traces(textfont_size=10, marker={'cornerradius': 5}, hovertemplate="""<b>%{x}</b><br><br><b>%{data.name}</b>: %{y:.3s}<br><extra></extra>""")

            bar_figure_passengers.update_xaxes(categoryarray=months_text, linewidth=2.5, showgrid=False, linecolor='rgb(180, 180, 180)')

            ## Bar Figure Setup for Flights ##

            bar_figure_flights = px.bar(airports_polars, x='MONTH', y=['ARRIVING FLIGHTS', 'DEPARTING FLIGHTS'],
                                           color_discrete_map={'ARRIVING FLIGHTS': '#E89C31', 'DEPARTING FLIGHTS': '#F2C689'},
                                           text_auto='0.3s')
            
            bar_figure_flights.update_yaxes(showgrid=True, zeroline=False, showline=False, showticklabels=True, tickwidth=2, gridcolor="rgba(30, 63, 102, 0.15)")

            bar_figure_flights.update_layout(legend={
                'orientation':'h',
                'yanchor':"bottom",
                'y':1.02,
                'xanchor': 'center',
                'x': 0.5}, 
                legend_title_text = '<b>Total Flight Traffic</b>',
                xaxis_title=None,
                yaxis_title="Total Flights",
                yaxis_tickfont={'size': 10},
                
                margin={'l':10, 'r': 10, 't': 10, 'b': 10},
                plot_bgcolor='#f9f9f9', paper_bgcolor="#f9f9f9",
                hovermode='closest')
            
            bar_figure_flights.update_traces(textfont_size=10, marker={"cornerradius":5}, hovertemplate="""<b>%{x}</b><br><br><b>%{data.name}</b>: %{y:.3s}<br><extra></extra>""")

            bar_figure_flights.update_xaxes(categoryarray=months_text, linewidth=2.5, showgrid=False, linecolor='rgb(180, 180, 180)')


            ## Return div contents for the callback ##
            return_children = [

                html.H2(f"{selected_viz}", id='airports-graph-header', style={'marginBottom': '0.1em'}),
                html.P(f'({selected_airport})', id='airports-graph-subheader', className='text-muted', style={'marginBottom': '0.2em'}),
                html.Hr(className='my-2'),
                html.P(airport_visual_desc, className='mb-2 text-muted', id='airports-graph-desc', style={'fontSize': '0.85em'}),

                dcc.Graph(id='airports-graph', style={'height':'26vh'}, figure=bar_figure_passengers),

                dcc.Graph(id='airports-graph-2', style={'height': '26vh'}, figure=bar_figure_flights)

            ]

            return return_children
        
    elif selected_viz == 'Top 10 Connected Airports By Passengers':

        return generateAirportsTopTen(selected_viz=selected_viz, selected_airport=selected_airport, sqlite_path=sqlite_path)



@callback(
    Output(component_id='airport-ap-selection', component_property='clearable'),
    Output(component_id='airport-ap-selection', component_property='value'),
    [Input(component_id='airport-viz-selection', component_property='value')],
    State(component_id='airport-ap-selection', component_property='value')
)
def handleClearableAirportSelection(selected_viz, selected_airport):

    if (selected_airport is None or selected_airport.strip() == '') and selected_viz == 'Top 10 Connected Airports By Passengers':

        return False, 'New York, NY: John F. Kennedy International'
    
    elif selected_viz == 'Top 10 Connected Airports By Passengers' and (selected_airport is not None and selected_airport.strip() != ''):

        return False, no_update
    
    else:

        return True, no_update
    

@callback(
    Output(component_id='airport-viz-accordion', component_property='active_item'),
    [Input(component_id='airport-viz-selection', component_property='value')]
)
def accordionActiveItemCallback(selected_viz):

    if selected_viz == airports_visual_list[0]:

        return 'airports-item-1'
    
    elif selected_viz == airports_visual_list[1]:

        return 'airports-item-2'
    
    elif selected_viz == airports_visual_list[2]:

        return 'airports-item-3'
    
    elif selected_viz == airports_visual_list[3]:

        return 'airports-item-4'