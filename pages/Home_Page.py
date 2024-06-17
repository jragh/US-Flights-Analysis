from dash import html, dcc, Input, Output, State, callback, no_update, register_page
import dash_bootstrap_components as dbc

register_page(__name__, path='/Home')

layout = html.Div([

    dbc.Container([

        dbc.Row(className='home-page-row-banner', children=[

            dbc.Col([

                dbc.Row([

                    dbc.Col([

                        html.Span(
                            
                            [html.H1('HOLY MOLY THIS IS SOME BIG TEXT', className='home-banner-title-text'),
                            html.P('This is some Smaller Example text')]
                            
                        , style={'display': 'inline-block'}, className='home-page-title-text-box')

                    ],lg=4, md=6, sm=12, xs=12, width=3, className='d-flex align-items-center'),


                    dbc.Col([

                        html.Div([

                            html.H2('Check out some ', id='home-page-header'),
                            html.Hr(className='my-2'),
                            html.P('Test 1', className='mb-2', id='airports-graph-desc')

                    ], className='p-4 rounded-3 home-page-example-animate-box flex-fill', id='home-visual-div')

                    ],lg=6, md=6, sm=12, xs=12, width=8, className='d-flex align-items-center')


                ], style={'height': '100%'}, justify='around')

            ], width=12, className='home-banner-main-column')

        ])

    ], fluid=True)

], style={'margin': 0})