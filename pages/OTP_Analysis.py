import polars as pl
from dash import html, dcc, Input, Output, State, callback, no_update
import dash_bootstrap_components as dbc
import plotly_express as px
import os

import dash

from .OTPAnalyticsText import otp_text



dash.register_page(__name__, 
                   path='/OnTimePerformance', 
                   title="US Flight Analysis - On Time Performance Analytics", 
                   description='A deeper dive of On Time Performance for American Passenger Aviation.',
                   image="RoutesAnalysisMetaImage.png")

sqlite_path = os.environ['POSTGRES_URI_LOCATION']

otp_visual_list = ['Average Arrival Delay By Carrier']

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
                                html.Div([dcc.Dropdown(value='', options=[], multi=False, searchable=True, clearable=True, 
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


## Callback for the Routes Description Accordion ##
@callback(

    Output(component_id='otp-viz-accordion', component_property='active_item'),
    Input(component_id='otp-viz-selection', component_property='value')

)
def accordionActiveItemCallback(selected_viz):

    if selected_viz == otp_visual_list[0]:

        return 'otp-item-1'