from dash import html, dcc, Input, Output, State, callback, no_update, register_page
import dash_bootstrap_components as dbc

from .Home_Page_Pills import pills_array

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
                                   See below for an example on the type of information you can explore: ''', className='mb-3', id='airports-graph-desc',
                                   style={'color': 'rgb(199, 199, 200)'}),

                            html.H6('Top 5 Busiest Trips By Passengers in US (By Passenger Count)', style={'color': '#E89C31'}, className='mt-4 mb-3 text-center'),

                            ## First Row will have 3 pills
                            ## pills_array brought in from external module
                            dbc.Container(pills_array, className='mt-2 d-flex flex-row justify-content-center flex-wrap align-items-center')
                            

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