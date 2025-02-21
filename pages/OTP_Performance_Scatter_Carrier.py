import polars as pl

from dash import dcc, html
import dash_bootstrap_components as dbc
import plotly_express as px


## Initial Function for loading first stage for All Carriers / visual; not used for toggling with mini select ##
## Mini select will use a different function which will only replace the dcc.Graph component, not the entire Div ##
def otpPerformanceCarrierScatter(selected_carrier, sqlite_path, selected_viz):

    if (selected_carrier == 'All Carriers' or selected_carrier is None or selected_carrier.strip() == '') and selected_viz == 'Arrival Delay By Route & Carrier':

        return '', '', ''
    

    ## Else section for when Carrier is selected ##
    else: 

        otp_carriers_summary = f"""

        select * from public.otp_carrier_average_delay
        where "Carrier Name" = '{selected_carrier}'

        """

        otp_carriers_summary_df = pl.read_database_uri(query=otp_carriers_summary, uri=sqlite_path, engine='adbc')

        otp_carriers_summary_df = otp_carriers_summary_df.with_columns(
            pl.when((pl.col('Average Arrival Delay Performance') >= 10.00)).then(pl.lit('Late > 10 Mins'))
            .when((pl.col('Average Arrival Delay Performance') < 10.00) & (pl.col('Average Arrival Delay Performance') >= 0.00)).then(pl.lit('Late < 10 Mins'))
            .when((pl.col('Average Arrival Delay Performance') < 0.00) & (pl.col('Average Arrival Delay Performance') >= -10.00)).then(pl.lit('Early < 10 Mins'))
            .when((pl.col('Average Arrival Delay Performance') < -10.00)).then(pl.lit('Early > 10 Mins')).alias('OTP Arrival Category'))

        otp_carriers_delay_scatter = px.scatter(data_frame=otp_carriers_summary_df, x = 'Number of Flights OTP', y = 'Average Arrival Delay Performance',
                                                log_x = False, log_y= False, color="OTP Arrival Category",
                                                custom_data=['Carrier Name', 'Route Description Short', 'Total Delays', 'Total Arrival Performance'],
                                                opacity=0.75,
                                                color_discrete_map={
                                                    'Late > 10 Mins': "#f03a3a",
                                                    'Late < 10 Mins': "#f4a582",
                                                    'Early < 10 Mins': "#92c5de",
                                                    'Early > 10 Mins': "#0571b0"
                                                },
                                                category_orders={'OTP Arrival Category': ['Early > 10 Mins', 'Early < 10 Mins', 'Late < 10 Mins', 'Late > 10 Mins']})
        
        otp_carriers_delay_scatter.update_traces(marker={"line": {'width': 0.75}, 'size': 7.5,
                                             'opacity': 0.75}, mode='markers', 
                                             hovertemplate = '''<b>%{customdata[1]}</b><br><br><b>Average Arrival Delay:</b> %{y:.2f} Mins<br><b>Total Flights:</b> %{x:.3s}<br><b>Total Delayed Flights:</b> %{customdata[2]:.3s}<br><b>Total Minutes Delayed:</b> %{customdata[3]:.3s}<br>''',
                                    )
        
        otp_carriers_delay_scatter.update_layout(yaxis={'tickfont': {'size': 10}}, margin={'l':10, 'r': 10, 't': 10, 'b': 8},
                               plot_bgcolor='#f9f9f9', paper_bgcolor="#f9f9f9",
                               showlegend=True, hoverlabel={'align': 'left'},
                               legend={
                                   'orientation':'h',
                                   'yanchor':"bottom",
                                   'y':1.02,
                                   'xanchor': 'center',
                                   'x': 0.5}, 
                                legend_title_text = '<b>Arrival Delay Category</b>')
        
        otp_carriers_delay_scatter.update_yaxes(title='Average Arrival Time Delay', showline=False, showgrid=True, showticklabels=True, tickwidth=2,
                              gridcolor='rgba(60, 60, 60, 0.15)', griddash='dot', zeroline=True, zerolinewidth=1, zerolinecolor='rgba(33, 37, 41, 0.5)')
    
        otp_carriers_delay_scatter.update_xaxes(title='Total Flights',
                              showgrid=True, showline=False, linewidth=2.5, linecolor='rgba(33, 37, 41, 0.5)',
                              showticklabels=True, tickwidth=2, gridcolor="rgba(60, 60, 60, 0.15)", griddash="dot")
        

        return_children = [

            html.H2(f'{selected_viz}', id='otp-graph-header', style={'marginBottom': '0.1em'}),
            html.P(f'{selected_carrier}', id='otp-graph-subheader', className='text-muted', style={'marginBottom': '0.1em'}),
            html.Hr(style={'margin': '0.5rem 0'}),
            html.P('''Displays the Average Arrival Delay by Carrier on a route by route basis. The Scatter plot displays average delay time against
                   the nuber of flights, which helps to highlight the worst performing flights a Carrier offers by Volume. 
                   Additionally, tooltips also provide additional context by showing Total Delay in minutes (Across the whole year), and number of flights that arrived late.''',
                   style={'fontSize': '0.85em'}, className='mb-2 text-muted',
                   id='otp-graph-description-2'),

            dcc.Graph(id='otp-graph-option-2', style={'display': 'block', 'height': '50vh'}, figure=otp_carriers_delay_scatter)


        ]


        return return_children