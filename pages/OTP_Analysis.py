import polars as pl
from dash import html, dcc, Input, Output, State, callback, no_update
import dash_bootstrap_components as dbc
import plotly_express as px
import os

import plotly.graph_objects as go

import dash

from .OTPAnalyticsText import otp_text



dash.register_page(__name__, 
                   path='/OnTimePerformance', 
                   title="US Flight Analysis - On Time Performance Analytics", 
                   description='A deeper dive of On Time Performance for American Passenger Aviation.',
                   image="RoutesAnalysisMetaImage.png")

sqlite_path = os.environ['POSTGRES_URI_LOCATION']

otp_visual_list = ['Average Arrival Delay By Carrier']

carrier_selection_query = """ select distinct "Unique Carrier Name" from public.otp_daily_average oda order by "Unique Carrier Name" """

carrier_selection_options = pl.Series(pl.read_database_uri(uri=sqlite_path, engine='adbc', query = carrier_selection_query).select(pl.col("Unique Carrier Name"))).to_list()


months_text = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

carrier_selection_options.insert(0, 'All Carriers')

textResults = otp_text()

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
                                    html.Div([dcc.Dropdown(value=otp_visual_list[0], options=otp_visual_list, multi=False, searchable=True, clearable=False, 
                                                           placeholder='Select a visual here...', id='otp-viz-selection',
                                                           style={'fontSize': '12px'})], className='dbc mb-2')
                                ], className='pt-2 pb-2'
                            ), className='bg-light text-dark border rounded-3'
                        )

                    ], width=12, md=6, id='visual-selection-col', className='mb-2'),

                    dbc.Col([

                        dbc.Card(
                            dbc.CardBody([
                                dbc.Label('Carrier Selection'),
                                html.Div([dcc.Dropdown(value=carrier_selection_options[0], options=carrier_selection_options, multi=False, searchable=True, clearable=True, 
                                                           placeholder='Select a Carrier for Analysis', id='otp-carrier-selection',
                                                           style={'fontSize': '12px'})], className='dbc mb-2')
                            ], className='pt-2 pb-2'
                            ), className='bg-light text-dark border rounded-3'
                        )

                    ], width=12, md=6, id='otp-carrier-selection-col-1', className='mb-2')

                ], justify='even'),

                

                
                

                ## Creating Graph Component for quick analytics ##
                dbc.Spinner([
                    html.Div([
                        html.H2('', id='otp-graph-header'),
                        html.Hr(className='my-2'),
                        html.P('', className='mb-2', id='otp-graph-desc'),

                        dcc.Graph(id='otp-graph', style={'display': 'block'})
                    ], className='p-4 bg-light text-dark border rounded-3', id='otp-visual-div')
                ], show_initially=True, spinner_style={'height': '3rem', 'width': '3rem'})


                

            ])], align="center")
            
            

        ], id='otp_graph_section', width = 12, lg = 8, md = 12, xl = 8, xxl = 8, sm=12, class_name='px-2')

    ])
], fluid=True, className='mr-4 ml-4')], style={'margin': 0})


## Callback for selected Graph ##
@callback(
    Output(component_id='otp-visual-div', component_property='children'),
    [Input(component_id='otp-viz-selection', component_property='value'),
     Input(component_id='otp-carrier-selection', component_property='value')
    ]
)
def otpGraphUpdateCallback(selected_viz, selected_carrier):

    if selected_viz == 'Average Arrival Delay By Carrier':

        if selected_carrier == 'All Carriers':

            all_carriers_query = """ 
            
            SELECT 
            "Unique Carrier Code", 
            "Unique Carrier Name",
            "Month Number", 
            "Month Name", 
            "Average Delay", 
            "Total Flights", 
            "Total Late > 10 Mins", 
            "Total Late < 10 Mins", 
            "Total Early < 10 Mins", 
            "Total Early > 10 Mins"
            FROM public.otp_carrier_by_month_summary_delay

            """

            otp_carriers_summary = pl.read_database_uri(uri = sqlite_path, engine = 'adbc', query = all_carriers_query)

            otp_all_carriers_summary_fig = px.bar(data_frame=otp_carriers_summary, x="Month Name", barmode='stack',
                                                  y=["Total Early > 10 Mins", "Total Early < 10 Mins", "Total Late < 10 Mins", "Total Late > 10 Mins"],
                                                  facet_row="Unique Carrier Name")
            
            otp_all_carriers_summary_fig.update_xaxes(categoryorder='array', categoryarray=months_text)



            return_list = [

                html.H2(f'{selected_viz}', id='otp-graph-header', style={'marginBottom': '0.1em'}),
                html.P('All Carriers: Average Arrival Delay By Month', id='otp-graph-subheader', className='text-muted', style={'marginBottom': '0.1em'}),
                html.Hr(),
                html.P('Empty Graph goes here for now...', style={'fontSize': '0.85em'}, className='mb-2 text-muted'),
                dcc.Graph(id='otp-graph-option-1', style={'display': 'block', 'height':'26vh'}, figure=otp_all_carriers_summary_fig),
                dcc.Graph(id='otp-graph-option-2', style={'display': 'block', 'height':'26vh'})

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
                                           color_discrete_map={'Early > 10 Mins': '#2c7bb6', 'Early < 10 Mins': '#abd9e9', 'Late < 10 Mins': '#fdae61', 'Late > 10 Mins': '#A1123D'},
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
            CAST("Average Delay" as decimal(20,2)) as "Average Delay", 
            CAST("Total Flights" as real) as "Total Flights", 
            CAST("Delay Standard Deviation" as decimal(20,2)) as "Delay Standard Deviation", 
            CAST("CI Upper" as decimal(20, 2)) as "CI Upper", 
            CAST("CI Lower" as decimal(20, 2)) as "CI Lower"
            FROM public.otp_carrier_monthly_average_ci

            where "Unique Carrier Name" = '{selected_carrier}'

            order by CAST("Month Number" as real) asc

            """

            carrier_delay_avg = pl.read_database_uri(query = selected_carrier_query_2, engine='adbc', uri=sqlite_path)

            carrier_delay_avg = carrier_delay_avg.with_columns(pl.col("Average Delay").cast(pl.Float64, strict=True).alias('Average Delay Float'))

            carrier_delay_avg_fig = px.line(carrier_delay_avg, 
                                            x="Month Name", 
                                            y="Average Delay Float", 
                                            markers=True, 
                                            text="Average Delay Float", 
                                            color_discrete_sequence=['#A1123D'])

            carrier_delay_avg_fig.update_yaxes(showgrid=True, zeroline=True, showline=False, showticklabels=True, tickwidth=2, gridcolor="rgba(30, 63, 102, 0.15)", type="-")

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
            
            carrier_delay_avg_fig.update_xaxes(categoryarray=months_text, linewidth=2.5, showgrid=False, linecolor='rgb(180, 180, 180)')

            carrier_delay_avg_fig.for_each_trace(lambda t: t.update(name = 'Average Arrival Delay in Mins'))

            carrier_delay_avg_fig.update_traces(textposition="bottom center", textfont={'size': 10.5}, line={'width': 3}, marker={'size': 10}, showlegend=True)


            return_array = [

                html.H2(f'Average Arrivak Delay & Arrival Delay Breakdown', id='otp-graph-header', style={'marginBottom': '0.1em'}),
                html.P(f'{selected_carrier}', id='routes-graph-subheader', className='text-muted', style={'marginBottom': '0.2em'}),
                html.Hr(style={'margin': '0.5rem 0'}),
                html.P('Displays the Average Arrival Delay on a monthly basis for each Airline Carrier. Additionally shows the breakdown of flight arrivals by severity of early / late arrival.', style={'fontSize': '0.85em'}, className='mb-2 text-muted'),

                dcc.Graph(id='otp-graph-option-1', style={'display': 'block', 'height': '26vh'}, figure=carrier_delay_brreakdown_fig),

                dcc.Graph(id='otp-graph-option-2', style={'display': 'block', 'height': '26vh'}, figure=carrier_delay_avg_fig)

            ]

            return return_array

## Callback for the Routes Description Accordion ##
@callback(

    Output(component_id='otp-viz-accordion', component_property='active_item'),
    Input(component_id='otp-viz-selection', component_property='value')

)
def accordionActiveItemCallback(selected_viz):

    if selected_viz == otp_visual_list[0]:

        return 'otp-item-1'