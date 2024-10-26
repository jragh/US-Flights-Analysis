import polars as pl
import os

import dash_bootstrap_components as dbc
from dash import html


pills_array = [
 

    ## Pill Number 1
    html.Span(html.Small('1: LHR & JFK'), className='mx-1 my-1 px-2 py-1 flex-grow-0 rounded-pill btn-home-page', id='home-pill-1',
              style={'backgroundColor': '#62B3E0', 'color': '#0B2838'}),
              
    dbc.Popover(
        [
            dbc.PopoverHeader([html.Strong('LONDON, UK (LHR) AND NEW YORK, NY (JFK)')], style={'fontWeight': 'bold', 'fontSize': '90%'}),
            dbc.PopoverBody(children=[
            
            html.Span([
                html.Strong('Passengers Flown: ', style={'fontSize': '90%'}),
                html.P('2,987,159', className='mb-1', style={'fontSize': '90%'})
                ]),
            
            html.Span([
                html.Strong('Flights Flown: '),
                html.P('14,634', className='mb-1')
            ]),

            html.Span([
                html.Strong('Servicing Carriers: '),
                html.P('6', className='mb-1')
            ])
            ], className='px-3 py-2')
        ],
        body=True,
        target='home-pill-1',
        trigger='legacy',
        flip=True,
        placement='auto'
    ),


    ## Pill Number 2
    html.Span(html.Small('2: ATL & MCO'), className='mx-1 my-1 px-2 py-1 flex-grow-0 rounded-pill btn-home-page', id='home-pill-2',
              style={'backgroundColor': '#E89C31', 'color': '#0B2838'}),

    dbc.Popover([
            dbc.PopoverHeader([html.Strong('ATLANTA, GA (ATL) AND ORLANDO, FL (MCO)')], style={'fontWeight': 'bold', 'fontSize': '90%'}),
            dbc.PopoverBody(children=[

                html.Span([
                    html.Strong('Passengers Flown: ', style={'fontSize': '90%'}),
                    html.P('2,952,159', className='mb-1', style={'fontSize': '90%'})
                ]),

                html.Span([
                    html.Strong('Flights Flown: ', style={'fontSize': '90%'}),
                    html.P('18,124', className='mb-1', style={'fontSize': '90%'})
                ]),

                html.Span([
                    html.Strong('Servicing Carriers: ', style={'fontSize': '90%'}),
                    html.P('15', className='mb-1', style={'fontSize': '90%'})
                ])
            ], className='px-3 py-2')
        ],
        body=True,
        target='home-pill-2',
        trigger='legacy',
        flip=True,
        placement='auto'
    ),


    ## Pill Number 3
    html.Span(html.Small('3: LAX & JFK'), className='mx-1 my-1 px-2 py-1 flex-grow-0 rounded-pill btn-home-page', id='home-pill-3',
              style={'backgroundColor': '#A1123D', 'color': '#E89C31'}),

    dbc.Popover([

        dbc.PopoverHeader([html.Strong('LOS ANGELES, CA (LAX) AND NEW YORK, NY (JFK)')], style={'fontWeight': 'bold', 'fontSize': '90%'}),
        dbc.PopoverBody(children=[

            html.Span([
                html.Strong('Passengers Flown: ', style={'fontSize': '90%'}),
                html.P('2,812,807', className='mb-1', style={'fontSize': '90%'})
            ]),
            html.Span([
                html.Strong('Flights Flown: ', style={'fontSize': '90%'}),
                html.P('19,958', className='mb-1', style={'fontSize': '90%'})
            ]),
            html.Span([
                html.Strong('Servicing Carriers: ', style={'fontSize': '90%'}),
                html.P('13', className='mb-1', style={'fontSize': '90%'})
            ])
        ], className='px-3 py-2')

    ],
        body=True,
        target='home-pill-3',
        trigger='legacy',
        flip=True,
        placement='auto'),


    ## Pill Number 4
    html.Span(html.Small('4: LAS & LAX'), className='mx-1 my-1 px-2 py-1 flex-grow-0 rounded-pill btn-home-page', id='home-pill-4',
              style={'backgroundColor': '#62B3E0', 'color': '#0B2838'}),

    dbc.Popover([

        dbc.PopoverHeader([html.Strong('LAS VEGAS, NV (LAS) AND LOS ANGELES, CA (LAX)')], style={'fontWeight': 'bold', 'fontSize': '90%'}),
        dbc.PopoverBody(children=[

            html.Span([
                html.Strong('Passengers Flown: ', style={'fontSize': '90%'}),
                html.P('2,727,943', className='mb-1', style={'fontSize': '90%'})
            ]),
            html.Span([
                html.Strong('Flights Flown: ', style={'fontSize': '90%'}),
                html.P('22,474', className='mb-1', style={'fontSize': '90%'})
            ]),
            html.Span([
                html.Strong('Servicing Carriers: ', style={'fontSize': '90%'}),
                html.P('25', className='mb-1', style={'fontSize': '90%'})
            ])
        ], className='px-3 py-2')

    ],
        body=True,
        target='home-pill-4',
        trigger='legacy',
        flip=True,
        placement='auto'),


    ## Pill Number 5
    html.Span(html.Small('5: LAX & SFO'), className='mx-1 my-1 px-2 py-1 flex-grow-0 rounded-pill btn-home-page', id='home-pill-5',
              style={'backgroundColor': '#E89C31', 'color': '#0B2838'}),

    dbc.Popover([

        dbc.PopoverHeader([html.Strong('LOS ANGELES, CA (LAX) AND SAN FRANCISCO, CA (SFO)')], style={'fontWeight': 'bold', 'fontSize': '90%'}),
        dbc.PopoverBody(children=[

            html.Span([
                html.Strong('Passengers Flown: ', style={'fontSize': '90%'}),
                html.P('2,709,771', className='mb-1', style={'fontSize': '90%'})
            ]),
            html.Span([
                html.Strong('Flights Flown: ', style={'fontSize': '90%'}),
                html.P('25,442', className='mb-1', style={'fontSize': '90%'})
            ]),
            html.Span([
                html.Strong('Servicing Carriers: ', style={'fontSize': '90%'}),
                html.P('22', className='mb-1', style={'fontSize': '90%'})
            ])
        ], className='px-3 py-2')

    ],
        body=True,
        target='home-pill-5',
        trigger='legacy',
        flip=True,
        placement='auto'),

    
    ## Pill Number 6
    html.Span(html.Small('6: ATL & FLL'), className='mx-1 my-1 px-2 py-1 flex-grow-0 rounded-pill btn-home-page', id='home-pill-6',
              style={'backgroundColor': '#A1123D', 'color': '#E89C31'}),

    dbc.Popover([

        dbc.PopoverHeader([html.Strong('ATLANTA, GA (ATL) AND FORT LAUDERDALE, FL (FLL)')], style={'fontWeight': 'bold', 'fontSize': '90%'}),
        dbc.PopoverBody(children=[

            html.Span([
                html.Strong('Passengers Flown: ', style={'fontSize': '90%'}),
                html.P('2,591,317', className='mb-1', style={'fontSize': '90%'})
            ]),
            html.Span([
                html.Strong('Flights Flown: ', style={'fontSize': '90%'}),
                html.P('15,897', className='mb-1', style={'fontSize': '90%'})
            ]),
            html.Span([
                html.Strong('Servicing Carriers: ', style={'fontSize': '90%'}),
                html.P('12', className='mb-1', style={'fontSize': '90%'})
            ])
        ], className='px-3 py-2')

    ],
        body=True,
        target='home-pill-6',
        trigger='legacy',
        flip=True,
        placement='auto'),


    ## Pill Number 7
    html.Span(html.Small('7: LAS & DEN'), className='mx-1 my-1 px-2 py-1 flex-grow-0 rounded-pill btn-home-page', id='home-pill-7',
              style={'backgroundColor': '#62B3E0', 'color': '#0B2838'}),

    dbc.Popover([

        dbc.PopoverHeader([html.Strong('LAS VEGAS, NV (LAS) AND DENVER, CO (DEN)')], style={'fontWeight': 'bold', 'fontSize': '90%'}),
        dbc.PopoverBody(children=[

            html.Span([
                html.Strong('Passengers Flown: ', style={'fontSize': '90%'}),
                html.P('2,418,520', className='mb-1', style={'fontSize': '90%'})
            ]),
            html.Span([
                html.Strong('Flights Flown: ', style={'fontSize': '90%'}),
                html.P('18,391', className='mb-1', style={'fontSize': '90%'})
            ]),
            html.Span([
                html.Strong('Servicing Carriers: ', style={'fontSize': '90%'}),
                html.P('15', className='mb-1', style={'fontSize': '90%'})
            ])
        ], className='px-3 py-2')

    ],
        body=True,
        target='home-pill-7',
        trigger='legacy',
        flip=True,
        placement='auto'),


    ## Pill Number 8
    html.Span(html.Small('8: PHX & DEN'), className='mx-1 my-1 px-2 py-1 flex-grow-0 rounded-pill btn-home-page', id='home-pill-8',
              style={'backgroundColor': '#E89C31', 'color': '#0B2838'}),

    dbc.Popover([

        dbc.PopoverHeader([html.Strong('PHOENIX, AZ (PHX) AND DENVER, CO (DEN)')], style={'fontWeight': 'bold', 'fontSize': '90%'}),
        dbc.PopoverBody(children=[

            html.Span([
                html.Strong('Passengers Flown: ', style={'fontSize': '90%'}),
                html.P('2,418,388', className='mb-1', style={'fontSize': '90%'})
            ]),
            html.Span([
                html.Strong('Flights Flown: ', style={'fontSize': '90%'}),
                html.P('18,656', className='mb-1', style={'fontSize': '90%'})
            ]),
            html.Span([
                html.Strong('Servicing Carriers: ', style={'fontSize': '90%'}),
                html.P('20', className='mb-1', style={'fontSize': '90%'})
            ])
        ], className='px-3 py-2')

    ],
        body=True,
        target='home-pill-8',
        trigger='legacy',
        flip=True,
        placement='auto'),


    ## Pill Number 9
    html.Span(html.Small('9: LAX & HNL'), className='mx-1 my-1 px-2 py-1 flex-grow-0 rounded-pill btn-home-page', id='home-pill-9',
              style={'backgroundColor': '#A1123D', 'color': '#E89C31'}),

    dbc.Popover([

        dbc.PopoverHeader([html.Strong('LOS ANGELES, CA (LAX) AND HONOLULU, HI (HNL)')], style={'fontWeight': 'bold', 'fontSize': '90%'}),
        dbc.PopoverBody(children=[

            html.Span([
                html.Strong('Passengers Flown: ', style={'fontSize': '90%'}),
                html.P('2,337,121', className='mb-1', style={'fontSize': '90%'})
            ]),
            html.Span([
                html.Strong('Flights Flown: ', style={'fontSize': '90%'}),
                html.P('12,466', className='mb-1', style={'fontSize': '90%'})
            ]),
            html.Span([
                html.Strong('Servicing Carriers: ', style={'fontSize': '90%'}),
                html.P('19', className='mb-1', style={'fontSize': '90%'})
            ])
        ], className='px-3 py-2')

    ],
        body=True,
        target='home-pill-9',
        trigger='legacy',
        flip=True,
        placement='auto'),

    
    ## Pill Number 10
    html.Span(html.Small('10: LAX & ORD'), className='mx-1 my-1 px-2 py-1 flex-grow-0 rounded-pill btn-home-page', id='home-pill-10',
              style={'backgroundColor': '#62B3E0', 'color': '#0B2838'}),

    dbc.Popover([

        dbc.PopoverHeader([html.Strong('LOS ANGELES, CA (LAX) AND CHICAGO, IL (ORD)')], style={'fontWeight': 'bold', 'fontSize': '90%'}),
        dbc.PopoverBody(children=[

            html.Span([
                html.Strong('Passengers Flown: ', style={'fontSize': '90%'}),
                html.P('2,324,504', className='mb-1', style={'fontSize': '90%'})
            ]),
            html.Span([
                html.Strong('Flights Flown: ', style={'fontSize': '90%'}),
                html.P('13,558', className='mb-1', style={'fontSize': '90%'})
            ]),
            html.Span([
                html.Strong('Servicing Carriers: ', style={'fontSize': '90%'}),
                html.P('20', className='mb-1', style={'fontSize': '90%'})
            ])
        ], className='px-3 py-2')

    ],
        body=True,
        target='home-pill-10',
        trigger='legacy',
        flip=True,
        placement='auto')
                              

]