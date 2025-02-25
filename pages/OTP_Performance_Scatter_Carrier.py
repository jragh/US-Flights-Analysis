import polars as pl

from dash import dcc, html
import dash_bootstrap_components as dbc
import plotly_express as px


## Initial Function for loading first stage for All Carriers / visual; not used for toggling with mini select ##
## Mini select will use a different function which will only replace the dcc.Graph component, not the entire Div ##
def otpPerformanceCarrierScatter(selected_carrier, sqlite_path, selected_viz):

    if (selected_carrier == 'All Carriers' or selected_carrier is None or selected_carrier.strip() == '') and selected_viz == 'Arrival Delay By Route & Carrier':

        otp_carriers_summary = '''
        
        with a as (

        select "Carrier Name", 
        'Total Routes Operated' as "Calculation Category",
        count(distinct "Route Description") "Value"
        from public.otp_carrier_average_delay
        group by "Carrier Name", 2
        order by count(distinct "Route Description") desc

        ),

        b as (

        select "Carrier Name",
        'Routes Arriving Late On Average' as "Calculation Category",
        SUM(case when "Average Arrival Delay Performance" > 10.00 then 1 else 0 end) "Value"
        from public.otp_carrier_average_delay
        group by "Carrier Name", 2

        ),

        c as (

        select "Carrier Name", 
        SUM("Number of Flights OTP") "Number of Flights", 
        SUM("Total Delays") "Delayed Flights",
        SUM("Carrier Delays") "Carrier Delays",
        SUM("Weather Delays") "Weather Delays",
        SUM("NAS Delays") "NAS Delays",
        SUM("Security Delays") "Security Delays",
        SUM("Late Aircraft Delays") "Late Aircraft Delays"

        from public.otp_carrier_average_delay

        group by "Carrier Name"


        )

        select a.*, 
        CAST(c."Number of Flights" as real) "Number of Flights", 
        CAST(c."Delayed Flights" as real) "Delayed Flights", 
        CAST(c."Carrier Delays" as real) "Carrier Delays", 
        CAST(c."Weather Delays" as real) "Weather Delays", 
        CAST(c."NAS Delays" as real) "NAS Delays", 
        CAST(c."Security Delays" as real) "Security Delays", 
        CAST(c."Late Aircraft Delays" as real) "Late Aircraft Delays"
        from a
        left join c
        on a."Carrier Name" = c."Carrier Name"

        union 

        select b.*, 
        CAST(c."Number of Flights" as real) "Number of Flights", 
        CAST(c."Delayed Flights" as real) "Delayed Flights", 
        CAST(c."Carrier Delays" as real) "Carrier Delays", 
        CAST(c."Weather Delays" as real) "Weather Delays", 
        CAST(c."NAS Delays" as real) "NAS Delays", 
        CAST(c."Security Delays" as real) "Security Delays", 
        CAST(c."Late Aircraft Delays" as real) "Late Aircraft Delays"
        from b
        left join c
        on b."Carrier Name" = c."Carrier Name"

        order by "Carrier Name"
        
        
        '''

        otp_carriers_summary_df = pl.read_database_uri(query=otp_carriers_summary, uri=sqlite_path, engine='adbc')

        otp_carriers_delay_scatter = px.scatter(data_frame=otp_carriers_summary_df, x="Value", y="Carrier Name", color="Calculation Category",
        custom_data=["Number of Flights", "Delayed Flights", "Carrier Delays", "Weather Delays", "NAS Delays", "Security Delays", "Late Aircraft Delays", "Calculation Category"],
        color_discrete_map={
            'Total Routes Operated': 'rgba(33, 37, 41, 1)',
            'Routes Arriving Late On Average': '#E89C31'
        })

        otp_carriers_delay_scatter.update_layout(yaxis={'tickfont': {'size': 10}}, margin={'l':10, 'r': 10, 't': 10, 'b': 8},
                               plot_bgcolor='#f9f9f9', paper_bgcolor="#f9f9f9",
                               showlegend=True, hoverlabel={'align': 'left'},
                               legend={
                                   'orientation':'h',
                                   'yanchor':"bottom",
                                   'y':1.02,
                                   'xanchor': 'center',
                                   'x': 0.5}, 
                                legend_title_text = '<b>Routes Breakdown</b>')

        ## Sorting the Categories
        sort_carrier = otp_carriers_summary_df.sort(pl.col("Value")).filter(pl.col("Calculation Category") == 'Total Routes Operated').get_column("Carrier Name").to_list()

        otp_carriers_delay_scatter.update_yaxes(title=None, showline=True, linewidth=2.5, linecolor='rgba(33, 37, 41, 0.5)',
                                showgrid=False, showticklabels=True, tickwidth=2,
                                gridcolor='rgba(60, 60, 60, 0.15)', griddash='dot', zeroline=True, zerolinewidth=1, zerolinecolor='rgba(33, 37, 41, 0.5)',
                                categoryorder="array", categoryarray=sort_carrier)

        otp_carriers_delay_scatter.update_xaxes(title='Number of Routes Operated',
                              showgrid=True, showline=True, linewidth=2.5, linecolor='rgba(33, 37, 41, 0.5)',
                              showticklabels=True, tickwidth=2, gridcolor="rgba(60, 60, 60, 0.15)", griddash="dot",
                              zeroline=False)

        otp_carriers_delay_scatter.update_traces(marker={'size': 9}, mode='markers',
        hovertemplate='''<b>%{y}</b><br><b>%{customdata[7]}: %{x:,}</b><br><br><b>Total Flights: </b>%{customdata[0]:,i}<br><b>Delayed Flights: </b>%{customdata[1]:,i}<br><b>Carrier Related Delayed Flights: </b>%{customdata[2]:,i}<br><b>Weather Related Delayed Flights: </b>%{customdata[3]:,i}<br><b>NAS Related Delayed Flights: </b>%{customdata[4]:,i}<br><b>Security Related Delayed Flights: </b>%{customdata[5]:,i}<br><b>Late Aircraft Delayed Flights: </b>%{customdata[6]:,i}<br><extra></extra>''')

        return_children = [

            html.H2(f'{selected_viz}', id='otp-graph-header', style={'marginBottom': '0.1em'}),
            html.P(f'{selected_carrier}: Routes With Delays Over 10 Mins', id='otp-graph-subheader', className='text-muted', style={'marginBottom': '0.1em'}),
            html.Hr(style={'margin': '0.5rem 0'}),
            html.P('''Displays the Total Number of Routes (Both Directions) and the Number of Routes where on Average there is an Arrival Delay.
            This helps to highlight which how many routes an airline operates where they are experiencing delays, without overwhelming the end user.
            Additionally, hover tooltips also provice additional context by showing Total Flights, Total Average Delay for the Carrier, and Number of Flights that arrived late.''',
                   style={'fontSize': '0.85em'}, className='mb-2 text-muted',
                   id='otp-graph-description-2'),

            
            
            dcc.Graph(id='otp-graph-option-2', style={'display': 'block', 'height': '50vh'}, figure=otp_carriers_delay_scatter)

        ]

        return return_children
    

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