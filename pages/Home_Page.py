from dash import html, dcc, Input, Output, State, callback, no_update, register_page
import dash_bootstrap_components as dbc

from .Home_Page_AG_Grid import home_page_grid

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

                            html.H2('An Analytics App on USA Flights Data', id='home-page-header', style={'color': '#E89C31'}),
                            html.Hr(className='my-2'),
                            html.Small('''Explore this Web app to discover key data relating to US passenger flights.
                                   Available themes in the app include Passenger, Airport, Carrier, Flight Route, and Flight Delay Data.
                                   See below for an example on the type of information you can explore: ''', className='mb-2', id='airports-graph-desc',
                                   style={'color': 'rgb(199, 199, 200)'}),

                            html.H6('Top 5 Busiest Trips By Passengers in US (By Passenger Count)', style={'color': '#E89C31'}, className='my-3'),

                            ## First Row will have 3 pills
                            dbc.Row([
                                
                                ## Col for Home Page Pills ##
                                ## TODO: Create separate component for home page pills to work ##
                                dbc.Col([

                                    html.Span(html.Small('1: LHR & JFK'), className='mx-1 px-2 py-1', id='home-pill-1',
                                              style={'backgroundColor': '#62B3E0', 'color': '#0B2838', 'borderRadius': '20px'}),

                                    ## Popover for Home Page Pill ##
                                    dbc.Popover(
                                        [
                                            dbc.PopoverHeader('LONDON, UK (LHR) AND NEW YORK, NY (JFK)', style={'fontSize': '80%', 'fontWeight': 'bold'}),
                                            dbc.PopoverBody(children=[
                                            html.Span([
                                                html.Strong('Passengers Flown: '),
                                                html.P('2,987,159')
                                                ])
                                            ], className='px-3 py-2')
                                        ],
                                        body=True,
                                        target='home-pill-1',
                                        trigger='legacy',
                                        flip=True
                                    )

                                ], xl = 3, lg = 4, md = 6, sm = 6, xs = 6, style={'textAlign': 'center'})


                            ], justify='center', className='mt-2 mb-4'),

                            dbc.Row([]),

                            dbc.Row([]),

                            home_page_grid

                            # html.Span([

                            #     html.H6([
                            #         html.Span('#1: LONDON, UK (LHR) AND NEW YORK, NY (JFK)', className='example_head_1'),

                            #         html.Span('#2: ATLANTA, GA (ATL) AND ORLANDO, FL (MCO)', className='example_head_2'),

                            #         html.Span('#3: LOS ANGELES, CA (LAX) AND NEW YORK, NY (JFK)', className='example_head_3'),

                            #         html.Span('#4: LAS VEGAS, NV (LAS) AND LOS ANGELES, CA (LAX)', className='example_head_4'),

                            #         html.Span('#5: LOS ANGELES, CA (LAX) AND SAN FRANCISCO, CA (SFO)', className='example_head_5')
                            # ], className='m-0')

                            # ], className='busy-trips-header-home-page'),

                            # html.Div(style={'height': '1.5em'}),


                            # html.Span([

                            #     html.H6([

                            #         html.Span('Passengers: 2 987 159, Flights: 14 634, Servicing Carriers: 5', className='example_head_stats_1'),

                            #         html.Span('Passengers: 2 952 159, Flights: 18 009, Servicing Carriers: 7', className='example_head_stats_2'),

                            #         html.Span('Passengers: 2 812 807, Flights: 19 935, Servicing Carriers: 5', className='example_head_stats_3'),

                            #         html.Span('Passengers: 2 727 943, Flights: 22 440, Servicing Carriers: 20', className='example_head_stats_4'),

                            #         html.Span('Passengers: 2 709 771, Flights: 23 368, Servicing Carriers: 13', className='example_head_stats_5')

                            #     ])

                            # ], className='busy-trips-header-home-page-stats')
                            

                    ], className='p-4 rounded-3 home-page-example-animate-box flex-fill', id='home-visual-div')

                    ],lg=6, md=6, sm=12, xs=12, width=8, className='d-flex align-items-start title-animate')


                ], style={'height': '100%'}, justify='around')

            ], width=12, className='home-banner-main-column')

        ]),

        dbc.Row([

            dbc.Col([

                html.A(html.Span([html.I(className='bi bi-people-fill home-page-info-img')], className='mb-3'), href='/PassengerAnalytics'),
                html.H5('Passengers'),
                html.Small('Highlights trends in passenger airline travel across the USA. Analyze by Carrier, Seat utilization, and other metrics!')

            ], width=12, xs=12, sm=6, md=3, lg=2, xl=2, xxl=2, className='home-page-info-col mt-3'),

            dbc.Col([

                html.A(html.Span([html.I(className='bi bi-buildings-fill home-page-info-img')], className='mb-3'), href='/AirportAnalytics'),
                html.H5('Airports'),
                html.Small('Discover key highlights in airline travel at the airport level. Analyze by Carriers, Passengers, Flights and Destinations!')

            ], width=12, xs=12, sm=6, md=3, lg=2, xl=2, xxl=2, className='home-page-info-col mt-3'),

            dbc.Col([

                html.A(html.Span([html.I(className='bi bi-geo-alt-fill home-page-info-img')], className='mb-3'), href='/RouteAnalytics'),
                html.H5('Routes'),
                html.Small('Analyze Origin-Destination pairings with associated attributes such as Ticket Pricing, Passenger Counts, Carrier information, and more!')

            ], width=12, xs=12, sm=6, md=3, lg=2, xl=2, xxl=2, className='home-page-info-col mt-3'),

            dbc.Col([

                html.Span([html.I(className='bi bi-hourglass-split home-page-info-img')], className='mb-3'),
                html.H5('Flight Delays'),
                html.Small('Investigate Flight Delay dynamics among a variety of dimensions including Carriers, Airports, Aircraft, and Routes!')

            ], width=12, xs=12, sm=6, md=3, lg=2, xl=2, xxl=2, className='home-page-info-col mt-3')

        ], justify='evenly', className='my-4')

    ], fluid=True)

], style={'margin': 0})