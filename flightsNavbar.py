import polars as pl
from dash import html, dcc, Input, Output, State
import dash_bootstrap_components as dbc
import plotly_express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

import dash



navbar = dbc.Navbar(
    dbc.Container([

        dbc.Row([

            dbc.Col(html.Span(html.I(className='bi bi-airplane-fill', style={'fontSize': '2em', 'color': '#E89C31'})), style={'display':'inline-block'}),
            dbc.Col(html.Span([html.H5('FLYLYTICS', style={'margin': '0'})],className='nav-header-span-class'))

        ], class_name='g-2', align='center'),

        dbc.NavbarToggler(id="navbar-toggler", n_clicks=0)

    ], class_name='m-0'),dark=True, color='dark', class_name='p-2'
)