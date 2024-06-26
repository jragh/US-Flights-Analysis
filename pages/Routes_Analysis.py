import polars as pl
from dash import html, dcc, Input, Output, State, callback, no_update
import dash_bootstrap_components as dbc
import plotly_express as px

import dash

dash.register_page(__name__, path='/RouteAnalytics')

sqlite_path = 'sqlite:///US_Flights_Analytics.db'

routes_visual_list = ['Market Pairs: Revenue By Carrier']

layout = html.Div([dbc.Container([
    
    dbc.Row([

        dbc.Col(children = [],
                 id='sidebar', className = 'textSidebar',width = 12, lg = 4, md =12, xl = 4, xxl = 4, sm = 12, align='start'),

        dbc.Col(children=[

            dbc.Row([dbc.Col([

                dbc.Row([
                    dbc.Col([
                        
                        dbc.Card(
                            dbc.CardBody(
                                [
                                    dbc.Label('Visual Selection: '),
                                    html.Div([dcc.Dropdown(value=routes_visual_list[0], options=routes_visual_list, multi=False, searchable=True, clearable=False, 
                                                           placeholder='Select a visual here...', id='routes-viz-selection',
                                                           style={'fontSize': '12px'})], className='dbc mb-2')
                                ], className='pt-3 pb-2'
                            ), className='bg-light text-dark border rounded-3'
                        )

                    ], width=12, md=4, id='visual-selection-col', className='mb-2'),

                    dbc.Col([

                        dbc.Card(
                            dbc.CardBody([
                                dbc.Label(''),
                                html.Div([dcc.Dropdown(value='', options=[], multi=False, searchable=True, clearable=True, 
                                                           placeholder='Select an Airport from here...', id='airport-ap-selection',
                                                           style={'fontSize': '12px'})], className='dbc mb-2')
                            ], className='pt-3 pb-2'
                            ), className='bg-light text-dark border rounded-3'
                        )

                    ], width=12, md=4, id='visual-selection-col', className='mb-2')
                ], justify='around'),

                

                
                

                ## Creating Graph Component for quick analytics ##
                dbc.Spinner([
                    html.Div([
                        html.H2('', id='routes-graph-header'),
                        html.Hr(className='my-2'),
                        html.P('', className='mb-2', id='routes-graph-desc'),

                        dcc.Graph(id='routes-graph', style={'display': 'block'})
                    ], className='p-4 bg-light text-dark border rounded-3', id='routes-visual-div')
                ], show_initially=True, spinner_style={'height': '3rem', 'width': '3rem'})


                

            ])], align="center")
            
            

        ], id='routes_graph_section', width = 12, lg = 8, md = 12, xl = 8, xxl = 8, sm=12, class_name='px-2')

    ])
], fluid=True, className='mr-4 ml-4')], style={'margin': 0})