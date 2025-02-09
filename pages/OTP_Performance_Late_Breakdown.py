import polars as pl

from dash import dcc, html
import dash_bootstrap_components as dbc
import plotly_express as px

## Initial Function for loading forst stage for new carrier / visual; not used for toggling with mini select ##
## Mini select will use a different function which will only replace the dcc.Graph component, not the entire Div ##
def otpPerformanceLateBreakdown(selected_carrier, sqlite_path, selected_viz):

    months_text = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

    if selected_carrier == 'All Carriers' or selected_carrier is None or selected_carrier.strip() == '':

        ## All Carriers Delay Breakdown By Counts ##
        all_carriers_query = """ 
        
        SELECT 
        "Month Number", 
        "Month Name", 
        "Arrival Delay Classification", 
        cast("Total Flights" as real) as "Total Flights"
        FROM public.otp_total_monthly_delay_class
        """

        otp_carriers_summary = pl.read_database_uri(uri = sqlite_path, engine = 'adbc', query = all_carriers_query)

        otp_all_carriers_delay_breakdown_fig = px.bar(data_frame=otp_carriers_summary, x="Month Name", barmode='stack', color='Arrival Delay Classification',
                                                  color_discrete_map={'Early > 10 Mins': '#0571b0', 'Early < 10 Mins': '#92c5de', 'Late < 10 Mins': '#f4a582', 'Late > 10 Mins': '#ca0020'},
                                                  text_auto='0.3s', 
                                                  y="Total Flights",
                                                  category_orders={'Arrival Delay Classification': ['Early > 10 Mins', 'Early < 10 Mins', 'Late < 10 Mins', 'Late > 10 Mins']})
            
        otp_all_carriers_delay_breakdown_fig.update_yaxes(showgrid=True, zeroline=False, showline=False, showticklabels=True, tickwidth=2, gridcolor="rgba(30, 63, 102, 0.15)", type="-")

        otp_all_carriers_delay_breakdown_fig.update_layout(legend={
            'orientation':'h',
            'yanchor':"bottom",
            'y':1.02,
            'xanchor': 'center',
            'x': 0.5}, 
            legend_title_text = '<b>Arrival Delay Category</b>',
            xaxis_title=None,
            yaxis_title="Total Flights",
            yaxis_tickfont={'size': 10},
            
            margin={'l':10, 'r': 10, 't': 10, 'b': 10},
            plot_bgcolor='#f9f9f9', paper_bgcolor="#f9f9f9",
            hovermode='closest')
        
        otp_all_carriers_delay_breakdown_fig.update_traces(textfont_size=10, marker={"cornerradius":5}, hovertemplate="""<b>%{x}</b><br><br><b>%{data.name}</b>: %{y:.3s}<br><extra></extra>""")

        otp_all_carriers_delay_breakdown_fig.update_xaxes(categoryarray=months_text, linewidth=2.5, showgrid=False, linecolor='rgb(180, 180, 180)')
        
        ## All Carriers Average Delay Summary with other Stats ##
        otp_all_carrier_average_summary_query = """
        
        SELECT 
        cast("Month Number" as integer) as "Month Number", 
        "Month Name", 
        CAST("Average Delay" as real) as "Average Delay", 
        CAST("Total Flights" as integer) as "Total Flights", 
        CAST("Delay Standard Deviation" as real) as "Delay Standard Deviation", 
        CAST("CI Upper" as real) as "CI Upper", 
        CAST("CI Lower" as real) as "CI Lower"
        FROM public.otp_total_monthly_average_ci
        
        """

        otp_all_carriers_summary_2 = pl.read_database_uri(engine='adbc', uri=sqlite_path, query=otp_all_carrier_average_summary_query)

        otp_all_carriers_summary_2 = otp_all_carriers_summary_2.with_columns(pl.col("Average Delay").cast(pl.Float64, strict=True).alias('Average Delay Float'))

        otp_all_carriers_summary_2 = otp_all_carriers_summary_2.with_columns(

            pl.col('Average Delay Float').round(2).alias('Average Delay Float'),
            pl.col('CI Upper').cast(pl.Float64, strict=True).round(2).alias('CI Upper'),
            pl.col('CI Lower').cast(pl.Float64, strict=True).round(2).alias('CI Lower'),

        )

        otp_all_carriers_summary_fig = px.line(otp_all_carriers_summary_2, 
                                            x="Month Name", 
                                            y="Average Delay Float", 
                                            markers=True, 
                                            text="Average Delay Float", 
                                            color_discrete_sequence=['#ca0020'],
                                            custom_data=["CI Upper", "CI Lower", "Total Flights"])
            
        otp_all_carriers_summary_fig.update_yaxes(showgrid=False, zeroline=True, showline=False, showticklabels=True, tickwidth=2, gridcolor="rgba(30, 63, 102, 0.15)", type="-")

        ## Additional Section for Zero Line on Average Mins of Delay ##
        otp_all_carriers_summary_fig.update_yaxes(zerolinewidth=2, zerolinecolor='rgba(0, 0, 0, 0.4)')
    
        otp_all_carriers_summary_fig.update_layout(legend={
            'orientation':'h',
            'yanchor':"bottom",
            'y':1.02,
            'xanchor': 'center',
            'x': 0.5}, 
            legend_title_text = '<b>Average Arrival Delay</b>',
            xaxis_title=None,
            yaxis_title="Avg Arrival Delay (Mins)",
            yaxis_tickfont={'size': 10},
            margin={'l':10, 'r': 10, 't': 10, 'b': 10},
            plot_bgcolor='#f9f9f9', paper_bgcolor="#f9f9f9",
            hovermode='closest')
            
        otp_all_carriers_summary_fig.update_xaxes(categoryarray=months_text, linewidth=2.5, showgrid=False, linecolor='rgb(180, 180, 180)')

        otp_all_carriers_summary_fig.for_each_trace(lambda t: t.update(name = 'Average Arrival Delay in Mins'))

        otp_all_carriers_summary_fig.update_traces(textposition="bottom center", textfont={'size': 10.5}, line={'width': 3}, marker={'size': 10}, showlegend=True,
                                            hovertemplate="""<b>All Carriers - %{x}</b><br><br>
                                            <b>Average Arrival Delay: </b> %{y:.3} Mins<br>
                                            <b>Total Flights: </b> %{customdata[2]:,}<br>
                                            <b>CI 95% Upper: </b> %{customdata[0]} Mins<br>
                                            <b>CI 95% Lower: </b> %{customdata[1]} Mins<br>""")



        return_list = [

            html.H2(f'{selected_viz}', id='otp-graph-header', style={'marginBottom': '0.1em'}),
            html.P('All Carriers', id='otp-graph-subheader', className='text-muted', style={'marginBottom': '0.1em'}),
            html.Hr(style={'margin': '0.5rem 0'}),
            html.P('''Displays the Average Arrival Delay on a monthly basis for all Airline Carriers Combined. 
                    Additionally shows the breakdown of flight arrivals by severity of early / late arrival.''', style={'fontSize': '0.85em'}, className='mb-2 text-muted',
                    id='otp-graph-description-1'),

            html.Span(children = [

                ## Radio Items Select for changing graph without changing the visual selection dropdown at top ##
                dbc.RadioItems(inline=True, value=1, id='otp-graph-mini-select-1', options=[
                        
                    {'label': 'On-Time Counts & Arrival Delay Average', 'value': 1},
                    {'label': 'Flights Delayed (%)', 'value': 2}
                ], className='mb-0 text-muted', style={'fontSize': '0.8em'})

            ], className='otp-graph-util-span mb-0'),
                
            dcc.Graph(id='otp-graph-option-1-a', style={'display': 'block', 'height':'26vh'}, figure=otp_all_carriers_delay_breakdown_fig),
                
            dcc.Graph(id='otp-graph-option-1-b', style={'display': 'block', 'height':'24vh'}, figure=otp_all_carriers_summary_fig)

        ]



        return return_list
    
    else:

        selected_carrier_query = f"""

            SELECT 
            "Unique Carrier Code", 
            "Unique Carrier Name", 
            "Month Number", 
            "Month Name", 
            "Arrival Delay Classification", 
            CAST("Total Flights" as real) as "Total Flights"
            FROM public.otp_carrier_monthly_delay_class

            where "Unique Carrier Name" = '{selected_carrier}'

        """

        carrier_delay_breakdown = pl.read_database_uri(query=selected_carrier_query, engine='adbc', uri=sqlite_path)

        carrier_delay_brreakdown_fig = px.bar(carrier_delay_breakdown, x='Month Name', y='Total Flights', color='Arrival Delay Classification', barmode='stack',
                                        color_discrete_map={'Early > 10 Mins': '#0571b0', 'Early < 10 Mins': '#92c5de', 'Late < 10 Mins': '#f4a582', 'Late > 10 Mins': '#ca0020'},
                                        text_auto='0.3s',
                                        category_orders={'Arrival Delay Classification': ['Early > 10 Mins', 'Early < 10 Mins', 'Late < 10 Mins', 'Late > 10 Mins']})
            
        carrier_delay_brreakdown_fig.update_yaxes(showgrid=True, zeroline=False, showline=False, showticklabels=True, tickwidth=2, gridcolor="rgba(30, 63, 102, 0.15)", type="-")

        carrier_delay_brreakdown_fig.update_layout(legend={
            'orientation':'h',
            'yanchor':"bottom",
            'y':1.02,
            'xanchor': 'center',
            'x': 0.5}, 
            legend_title_text = '<b>Arrival Delay Category</b>',
            xaxis_title=None,
            yaxis_title="Total Flights",
            yaxis_tickfont={'size': 10},
            
            margin={'l':10, 'r': 10, 't': 10, 'b': 10},
            plot_bgcolor='#f9f9f9', paper_bgcolor="#f9f9f9",
            hovermode='closest')
        
        carrier_delay_brreakdown_fig.update_traces(textfont_size=10, marker={"cornerradius":5}, hovertemplate="""<b>%{x}</b><br><br><b>%{data.name}</b>: %{y:.3s}<br><extra></extra>""")

        carrier_delay_brreakdown_fig.update_xaxes(categoryarray=months_text, linewidth=2.5, showgrid=False, linecolor='rgb(180, 180, 180)')

        selected_carrier_query_2 = f"""

            SELECT 
            "Unique Carrier Code", 
            "Unique Carrier Name", 
            "Month Number",
            "Month Name", 
            CAST("Average Delay" as real) as "Average Delay", 
            CAST("Total Flights" as real) as "Total Flights", 
            CAST("Delay Standard Deviation" as double precision) as "Delay Standard Deviation", 
            CAST("CI Upper" as real) as "CI Upper", 
            CAST("CI Lower" as real) as "CI Lower"
            FROM public.otp_carrier_monthly_average_ci

            where "Unique Carrier Name" = '{selected_carrier}'

            order by CAST("Month Number" as real) asc

        """

        carrier_delay_avg = pl.read_database_uri(query = selected_carrier_query_2, engine='adbc', uri=sqlite_path)

        carrier_delay_avg = carrier_delay_avg.with_columns(pl.col("Average Delay").cast(pl.Float64, strict=True).alias('Average Delay Float'))

        carrier_delay_avg = carrier_delay_avg.with_columns(

            pl.col('Average Delay Float').round(2).alias('Average Delay Float'),
            pl.col('CI Upper').cast(pl.Float64, strict=True).round(2).alias('CI Upper'),
            pl.col('CI Lower').cast(pl.Float64, strict=True).round(2).alias('CI Lower')

        )

        carrier_delay_avg_fig = px.line(carrier_delay_avg, 
                                        x="Month Name", 
                                        y="Average Delay Float", 
                                        markers=True, 
                                        text="Average Delay Float", 
                                        color_discrete_sequence=['#ca0020'],
                                        custom_data=["CI Upper", "CI Lower", "Unique Carrier Name", "Total Flights"])
        
        carrier_delay_avg_fig.update_yaxes(showgrid=False, zeroline=True, showline=False, showticklabels=True, tickwidth=2, gridcolor="rgba(30, 63, 102, 0.15)", type="-")

        ## Additional Section for Zero Line on Average Mins of Delay ##
        carrier_delay_avg_fig.update_yaxes(zerolinewidth=2, zerolinecolor='rgba(0, 0, 0, 0.4)')

        carrier_delay_avg_fig.update_layout(legend={
            'orientation':'h',
            'yanchor':"bottom",
            'y':1.02,
            'xanchor': 'center',
            'x': 0.5}, 
            legend_title_text = '<b>Average Arrival Delay</b>',
            xaxis_title=None,
            yaxis_title="Avg Arrival Delay (Mins)",
            yaxis_tickfont={'size': 10},
                
            margin={'l':10, 'r': 10, 't': 10, 'b': 10},
            plot_bgcolor='#f9f9f9', paper_bgcolor="#f9f9f9",
            hovermode='closest')
        

        carrier_delay_avg_fig.update_xaxes(categoryarray=months_text, linewidth=1.5, showgrid=False, linecolor='rgb(180, 180, 180)')

        carrier_delay_avg_fig.for_each_trace(lambda t: t.update(name = 'Average Arrival Delay in Mins'))

        carrier_delay_avg_fig.update_traces(textposition="bottom center", textfont={'size': 10.5}, line={'width': 3}, marker={'size': 10}, showlegend=True,
                                            hovertemplate="""<b>%{customdata[2]} - %{x}</b><br><br>
                                            <b>Average Arrival Delay: </b> %{y:.3} Mins<br>
                                            <b>Total Flights: </b> %{customdata[3]:,}<br>
                                            <b>CI 95% Upper: </b> %{customdata[0]} Mins<br>
                                            <b>CI 95% Lower: </b> %{customdata[1]} Mins<br>""")
        

        return_array = [

            html.H2(f'Average Arrival Delay & Arrival Delay Breakdown', id='otp-graph-header', style={'marginBottom': '0.1em'}),
            html.P(f'{selected_carrier}', id='routes-graph-subheader', className='text-muted', style={'marginBottom': '0.2em'}),
            html.Hr(style={'margin': '0.5rem 0'}),
            html.P('''Displays the Average Arrival Delay on a monthly basis for each Airline Carrier. 
                    Additionally shows the breakdown of flight arrivals by severity of early / late arrival.''', style={'fontSize': '0.85em'}, className='mb-2 text-muted',
                    id='otp-graph-description-1'),

            html.Span(children = [

                ## Radio Items Select for changing graph without changing the visual selection dropdown at top ##
                dbc.RadioItems(inline=True, value=1, id='otp-graph-mini-select-1', options=[
                        
                    {'label': 'On-Time Counts & Arrival Delay Average', 'value': 1},
                    {'label': 'Flights Delayed (%)', 'value': 2}
                ], className='mb-0 text-muted', style={'fontSize': '0.8em'})

            ], className='otp-graph-util-span mb-0'),

            dcc.Graph(id='otp-graph-option-1-a', style={'display': 'block', 'height': '26vh'}, figure=carrier_delay_brreakdown_fig),

            dcc.Graph(id='otp-graph-option-1-b', style={'display': 'block', 'height': '24vh'}, figure=carrier_delay_avg_fig)

        ]

        return return_array
        

        










