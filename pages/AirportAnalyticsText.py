import dash_bootstrap_components as dbc
from dash import html

def airport_text():

    return_array = [

        dbc.Stack(
            [
                html.Span(
                    html.H1('AIRPORT'), className= 'header-span'
                ),
                html.Span(
                    html.H1('ANALYTICS'), className = 'header-span'
                )
            ], gap=1, style={'textAlign': '-webkit-center'}, className="my-4"
        )

    ]

    return return_array