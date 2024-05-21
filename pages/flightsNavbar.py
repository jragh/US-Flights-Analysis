import polars as pl
from dash import html, dcc, Input, Output, State
import dash_bootstrap_components as dbc
import plotly_express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

import dash


def navbar_named(page_name):

    named_navbar = page_name

    navbar = dbc.Navbar(
    dbc.Container([

        dbc.Row([

            dbc.Col(html.Span(html.I(className='bi bi-airplane-fill', style={'fontSize': '2em', 'color': '#E89C31'})), style={'display':'inline-block'}),
            dbc.Col(html.Span([html.H5('FLYLYTICS')],className='nav-header-span-class'))

        ], class_name='g-2', align='center'),

        dbc.Row([

            dbc.Nav([

                dbc.NavItem(dbc.NavLink(f"{named_navbar}", active=True, style={'font-size': 'x-small'},class_name='nav-header-desc-pill')),
                dbc.DropdownMenu([

                    dbc.DropdownMenuItem("Person Analytics", href='/PassengerAnalytics'),
                    dbc.DropdownMenuItem('Airport Analytics', href='/AirportAnalytics'),
                    dbc.DropdownMenuItem('Route Analytics'),
                    dbc.DropdownMenuItem('Flight Delay Analytics')
                ], nav=True, label='Page Navigation', color="secondary", menu_variant="dark")
                
            ], navbar=True, style={'alignItems': 'center'}, horizontal='end', class_name='navbar-top')

        ])

        

    ], class_name='m-0 mw-100', fluid="md"),dark=True, color='dark', class_name='p-2 w-95vw'
)

    return navbar