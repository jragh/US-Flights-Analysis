from dash import html, dcc, Input, Output, State
import dash_bootstrap_components as dbc
import plotly_express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots


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

                dbc.DropdownMenu([

                    dbc.DropdownMenuItem(html.Span([html.I(className='bi bi-house-fill', style={'marginRight': '0.5em', 'fontSize': '1.25em'}),'Home']), href='/'),
                    dbc.DropdownMenuItem(html.Span([html.I(className='bi bi-people-fill', style={'marginRight': '0.5em', 'fontSize': '1.25em'}), "Person Analytics"]), href='/PassengerAnalytics'),
                    dbc.DropdownMenuItem(html.Span([html.I(className='bi bi-buildings-fill', style={'marginRight': '0.5em', 'fontSize': '1.25em'}), "Airport Analytics"]), href='/AirportAnalytics'),
                    dbc.DropdownMenuItem(html.Span([html.I(className='bi bi-geo-alt-fill', style={'marginRight': '0.5em', 'fontSize': '1.25em'}), "Route Analytics"])),
                    dbc.DropdownMenuItem(html.Span([html.I(className='bi bi-hourglass-split', style={'marginRight': '0.5em', 'fontSize': '1.25em'}), "Flight Delay Analytics"]))

                ], in_navbar=True, nav=True, label='Page Navigation', color="secondary", menu_variant="dark", align_end=True),
                dbc.NavItem(dbc.NavLink(f"{named_navbar}", active=True, style={'font-size': 'x-small'},class_name='nav-header-desc-pill'))
                
            ], navbar=True, style={'alignItems': 'center'}, horizontal='end', class_name='navbar-top')

        ])

        

    ], class_name='m-0 mw-100', fluid=False),dark=True, color='dark', class_name='p-2 w-95vw mb-2'
)

    return navbar