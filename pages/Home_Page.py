from dash import html, dcc, Input, Output, State, callback, no_update, register_page
import dash_bootstrap_components as dbc

register_page(__name__, path='/Home')

layout = html.Div([

    dbc.Container([

        dbc.Row(className='home-page-row-banner', children=[

            dbc.Col([

                dbc.Row([

                    dbc.Col([

                        html.Div(
                            
                            [html.H1('Welcome To', className='home-banner-title-text'),
                             html.Span(html.H1('FLYLYTICS'), className='home-banner-title-italics'),
                            html.P('An Analytics Dashboard containing information on flights throughout the USA!', style={'color': 'rgb(199, 199, 200)', 'fontWeight': 100})]
                            
                        , style={'display': 'inline-block'}, className='home-page-title-text-box')

                    ],lg=4, md=6, sm=12, xs=12, width=12, className='d-flex align-items-start justify-content-sm-center justify-content-md-start justify-content-center title-animate'),


                    dbc.Col([

                        html.Div([

                            html.H2('An Analytics App on USA Flights Data', id='home-page-header', style={'color': 'rgb(199, 199, 200)'}),
                            html.Hr(className='my-2'),
                            html.Small('''Explore this Web app to discover key data relating to US passenger flights.
                                   Available themes in the app include Passenger, Airport, Carrier, Flight Route, and Flight Delay Data.
                                   See below for an example on the type of information you can explore: ''', className='mb-2', id='airports-graph-desc',
                                   style={'color': 'rgb(199, 199, 200)'}),

                            html.H6('Top 5 Busiest Trips By Passengers in US (By Passenger Count)', style={'color': '#E89C31'}, className='my-3'),

                            html.Span([

                                html.H6([
                                    html.Span('#1: LONDON, UK (LHR) AND NEW YORK, NY (JFK)', className='example_head_1'),

                                    html.Span('#2: ATLANTA, GA (ATL) AND ORLANDO, FL (MCO)', className='example_head_2'),

                                    html.Span('#3: LOS ANGELES, CA (LAX) AND NEW YORK, NY (JFK)', className='example_head_3'),

                                    html.Span('#4: LAS VEGAS, NV (LAS) AND LOS ANGELES, CA (LAX)', className='example_head_4'),

                                    html.Span('#5: LOS ANGELES, CA (LAX) AND SAN FRANCISCO, CA (SFO)', className='example_head_5')
                            ], className='m-0')

                            ], className='busy-trips-header-home-page'),

                            html.Div(style={'height': '1.5em'}),


                            html.Span([

                                html.H6([

                                    html.Span('Passengers: 2 987 159, Flights: 14 634, Servicing Carriers: 5', className='example_head_stats_1'),

                                    html.Span('#2: ATLANTA, GA (ATL) AND ORLANDO, FL (MCO)', className='example_head_stats_2'),

                                    html.Span('#3: LOS ANGELES, CA (LAX) AND NEW YORK, NY (JFK)', className='example_head_stats_3'),

                                    html.Span('#4: LAS VEGAS, NV (LAS) AND LOS ANGELES, CA (LAX)', className='example_head_stats_4'),

                                    html.Span('#5: LOS ANGELES, CA (LAX) AND SAN FRANCISCO, CA (SFO)', className='example_head_stats_5')

                                ])

                            ], className='busy-trips-header-home-page-stats')
                            

                    ], className='p-4 rounded-3 home-page-example-animate-box flex-fill', id='home-visual-div')

                    ],lg=6, md=6, sm=12, xs=12, width=8, className='d-flex align-items-start title-animate')


                ], style={'height': '100%'}, justify='around')

            ], width=12, className='home-banner-main-column')

        ])

    ], fluid=True)

], style={'margin': 0})