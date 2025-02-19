import polars as pl
from dash import html, dcc, Input, Output, State, callback, no_update, ctx
import dash_bootstrap_components as dbc
import plotly_express as px
import os

import plotly.graph_objects as go

import dash

from .OTPAnalyticsText import otp_text

from .OTP_Performance_Pct_Late import otpPerformancePctLate, otpPerformanceLateBreakdownFigOnly

from .OTP_Performance_Late_Breakdown import otpPerformanceLateBreakdown

from .OTP_Performance_Scatter_Carrier import otpPerformanceCarrierScatter



dash.register_page(__name__, 
                   path='/OnTimePerformance', 
                   title="US Flight Analysis - On Time Performance Analytics", 
                   description='A deeper dive of On Time Performance for American Passenger Aviation.',
                   image="RoutesAnalysisMetaImage.png")

sqlite_path = os.environ['POSTGRES_URI_LOCATION']

otp_visual_list = ['Average Arrival Delay By Carrier', 'Arrival Delay By Route & Carrier']

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
                                html.Div([dcc.Dropdown(value=carrier_selection_options[0], options=carrier_selection_options, multi=False, searchable=True, clearable=False, 
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


## Callback for selected Graph using imported library as opposed to written out code ##
@callback(
    Output(component_id='otp-visual-div', component_property='children'),
    [Input(component_id='otp-viz-selection', component_property='value'),
     Input(component_id='otp-carrier-selection', component_property='value')
    ]
)
def otpGraphUpdateCallback(selected_viz, selected_carrier):

    if selected_viz == 'Average Arrival Delay By Carrier':

        print(ctx.triggered_id)

        if ctx.triggered_id == 'otp-carrier-selection':

            if selected_carrier is None or selected_carrier.strip() == '':

                return no_update
            
            else:

                return otpPerformanceLateBreakdown(selected_carrier=selected_carrier, sqlite_path=sqlite_path, selected_viz=selected_viz)
            
        elif ctx.triggered_id == 'otp-viz-selection':

            if selected_carrier is None or selected_carrier.strip() == '' or selected_carrier == 'All Carriers':

                return otpPerformanceLateBreakdown(selected_carrier='All Carriers', sqlite_path=sqlite_path, selected_viz=selected_viz)
            
            else:

                return otpPerformanceLateBreakdown(selected_carrier=selected_carrier, sqlite_path=sqlite_path, selected_viz=selected_viz)
            
        ## Need this line if it is a fresh load of the page, or else our graph will not load because there is no ctx trigger being fired ##
        elif ctx.triggered_id is None:

            return otpPerformanceLateBreakdown(selected_carrier='All Carriers', sqlite_path=sqlite_path, selected_viz=selected_viz)
        
    ## Selection and return for Graph #2
    elif selected_viz == 'Arrival Delay By Route & Carrier':

        if ctx.triggered_id == 'otp-carrier-selection':

            if selected_carrier is None or selected_carrier.strip() == '':

                return no_update
            
            else: 

                return otpPerformanceCarrierScatter(selected_carrier=selected_carrier, sqlite_path=sqlite_path, selected_viz=selected_viz)
            
        elif ctx.triggered_id == 'otp-viz-selection':

            if selected_carrier is None or selected_carrier.strip() == '' or selected_carrier == 'All Carriers':

                return otpPerformanceCarrierScatter(selected_carrier = 'All Carriers', sqlite_path=sqlite_path, selected_viz=selected_viz)
            
            else:

                return otpPerformanceCarrierScatter(selected_carrier=selected_carrier, sqlite_path=sqlite_path, selected_viz=selected_viz)
            
        elif ctx.triggered_id is None:

            return otpPerformanceCarrierScatter(selected_carrier = 'All Carriers', sqlite_path=sqlite_path, selected_viz=selected_viz)

## Callback for the Routes Description Accordion ##
@callback(

    Output(component_id='otp-viz-accordion', component_property='active_item'),
    Input(component_id='otp-viz-selection', component_property='value')

)
def accordionActiveItemCallback(selected_viz):

    if selected_viz == otp_visual_list[0]:

        return 'otp-item-1'
    
    elif selected_viz == otp_visual_list[1]:

        return 'otp-item-2'
    

@callback(

    Output(component_id='otp-graph-option-1-a', component_property='figure'),
    Output(component_id='otp-graph-description-1', component_property='children'),
    [Input(component_id='otp-graph-mini-select-1', component_property='value')],
    State(component_id='otp-carrier-selection', component_property='value'),
    prevent_initial_call=True

)
def otpToggleFigureOne(toggle_selection, selected_carrier):

    if toggle_selection == 2:

        ## Currently using global for sqlite path, will need to change this ##
        return otpPerformancePctLate(selected_carrier=selected_carrier, sqlite_path=sqlite_path)
    
    elif toggle_selection == 1:

        return otpPerformanceLateBreakdownFigOnly(selected_carrier, sqlite_path)