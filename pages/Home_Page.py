from dash import html, dcc, Input, Output, State, callback, no_update, register_page
import dash_bootstrap_components as dbc

register_page(__name__, path='/Home')

layout = html.Div([

    dbc.Container([

        dbc.Row(className='home-page-row-banner', children=[

            dbc.Col([

                html.H1('HOLY MOLY THIS IS SOME BIG TEXT')

            ], width=12)

        ])

    ], fluid=True)

], style={'margin': 0})