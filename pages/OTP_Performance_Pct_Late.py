import polars as pl

from dash import dcc, html
import dash_bootstrap_components as dbc
import plotly_express as px

def otpPerformancePctLate(selected_carrier, sqlite_path):

    months_text = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

    if selected_carrier == 'All Carriers':

        otp_pct_late_query = """

            with a as (

            select "Month Number", "Month Name", 
            SUM(case when "Arrival Delay Classification" like 'Late %' then cast("Total Flights" as real) else 0 end) as "Total Late Flights",
            SUM(cast("Total Flights" as real)) as "Total Flights"
            from public.otp_carrier_monthly_delay_class
            group by "Month Number", "Month Name")

            select 'All Carriers' as "Unique Carrier Name", a.*, (a."Total Late Flights" * 1.00) / (a."Total Flights" * 1.00) as "Late Flight Percentage"
            from a
            order by cast("Month Number" as real) asc

        """

    else:
        
        otp_pct_late_query = f"""

            with a as (

            select "Unique Carrier Code", "Unique Carrier Name", "Month Number", "Month Name", 
            SUM(case when "Arrival Delay Classification" like 'Late %' then cast("Total Flights" as real) else 0 end) as "Total Late Flights",
            SUM(cast("Total Flights" as real)) as "Total Flights"
            from public.otp_carrier_monthly_delay_class

            where "Unique Carrier Name" = '{selected_carrier}'

            group by "Unique Carrier Code", "Unique Carrier Name", "Month Number", "Month Name")

            select a.*, (a."Total Late Flights" * 1.00) / (a."Total Flights" * 1.00) as "Late Flight Percentage"
            from a
            order by "Unique Carrier Name", cast("Month Number" as real) asc
        
        """

    otp_pct_late_polars_df = pl.read_database_uri(query=otp_pct_late_query, engine="adbc", uri=sqlite_path)

    otp_pct_late_visual_description = """Highlights the percentage of flights that arrived after their scheduled arrival time.
    Covers both major US Passenger Carriers as well as a total for 'All Carriers' on a monthly basis (Use the toggle below to switch between views)."""

    polars_barchart = px.bar(data_frame=otp_pct_late_polars_df, y='Late Flight Percentage', x='Month Name', orientation='v', text_auto='0.2%',
                             custom_data=['Total Flights', 'Total Late Flights'])
    
    polars_barchart.update_xaxes(categoryarray=months_text, linewidth=2.5, showgrid=False, linecolor='rgb(180, 180, 180)')

    polars_barchart.update_yaxes(showgrid=True, zeroline=False, showline=False, showticklabels=True, tickwidth=2, gridcolor="rgba(30, 63, 102, 0.15)", type="-", tickformat='0.0%')

    polars_barchart.update_traces(textfont_size=10, marker={"cornerradius":4, "color": 'rgb(232, 156, 49)'}, hovertemplate='''<b>%{x}</b><br /><br /><b>Percent of Flights Late: </b>%{y:.2%}<br><b>Total Late Flights: </b>%{customdata[1]:,}<br /><b>Total Flights: </b>%{customdata[0]:,}''')
    
    polars_barchart.update_layout(legend={
                'orientation':'h',
                'yanchor':"bottom",
                'y':1.02,
                'xanchor': 'center',
                'x': 0.5}, 
                legend_title_text = '<b>Percent of Flights w/ Delayed Arrivals</b>',
                xaxis_title=None,
                yaxis_title="Pct of Total Flights",
                yaxis_tickfont={'size': 10},
                
                margin={'l':10, 'r': 10, 't': 10, 'b': 10},
                plot_bgcolor='#f9f9f9', paper_bgcolor="#f9f9f9",
                hovermode='closest')
    
    return polars_barchart, otp_pct_late_visual_description
    


def otpPerformanceLateBreakdownFigOnly(selected_carrier, sqlite_path):

    months_text = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

    otp_breakdown_description = '''Displays the Average Arrival Delay on a monthly basis for each Airline Carrier. 
                    Additionally shows the breakdown of flight arrivals by severity of early / late arrival.'''

    if selected_carrier == 'All Carriers':

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

        return otp_all_carriers_delay_breakdown_fig, otp_breakdown_description

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

        return carrier_delay_brreakdown_fig, otp_breakdown_description





