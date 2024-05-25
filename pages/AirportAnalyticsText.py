import dash_bootstrap_components as dbc
from dash import html

def airport_text():

    return_array = [

        html.Div([

            dbc.Stack(
            [
                html.Span(
                    html.H1('AIRPORT'), className= 'header-span'
                ),
                html.Span(
                    html.H1('ANALYTICS'), className = 'header-span'
                )
            ], gap=1, style={'textAlign': '-webkit-center'}, className="my-4"
        ),

        html.Div([

            html.Span([html.I(className='bi bi-buildings-fill', style={'color': '#0B2838', 'fontSize': '4em'})], style={'display': 'inline-block'}),
            html.H6('Explore data and stats about Airports across the United States.', style={'fontWeight': 100})

        ], style={'margin': 'auto', 'textAlign': 'center', 'justify': 'center'})

        ], className='title-animate') 

    ]

    return return_array