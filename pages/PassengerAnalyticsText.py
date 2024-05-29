from dash import html, dcc, Input, Output, State
import dash_bootstrap_components as dbc
import plotly_express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots



def passengerText():

    returnArray = [

        html.Div([

            dbc.Stack(
            [
                html.Span(
                    html.H1('PASSENGER'), className= 'header-span'
                ),
                html.Span(
                    html.H1('ANALYTICS'), className = 'header-span'
                )
            ], gap=1, style={'textAlign': '-webkit-center'}, className="my-4"
            ),

            html.Div([

                html.Span(
                    html.I(className='bi bi-people-fill me-2', style={'color': '#0B2838', 'fontSize': '4em'}), style={'display': 'inline-block'}
                ),

                html.H6('Here is some example text describing what the passenger analytics will be like', style={'fontWeight': 100})

                ], style={'margin': 'auto', 'justifyContent': 'center', 'textAlign': 'center'})

        ], className='title-animate'),

        html.Div([
            dbc.ListGroup([

                dbc.ListGroupItem([
                    html.Div([

                        html.H6('Passengers By Carrier', className='my-0'),
                        html.Span(html.Small('1', style={'color': '#0B2838'}), style={'borderRadius': '50px', 'backgroundColor': 'white', 'display': 'inline-block'}, id='pass-1-desc-span')

                    ], className='w-100 d-flex justify-content-between mb-2', id='pass-1-desc'),
                    html.Small("""Select to see how many passengers flew on flights throughout the entire year.
                               Can filter by Airline Carrier.""", className="text-muted")
                ]),

                dbc.ListGroupItem([
                    html.Div([

                        html.H6('Passenger Utilization By Carrier (%)', className='my-0'),
                        html.Span(html.Small('2', style={'color': '#0B2838'}), style={'borderRadius': '50px', 'backgroundColor': 'white', 'display': 'inline-block'}, id='pass-2-desc-span')

                    ], className='w-100 d-flex justify-content-between mb-2', id='pass-2-desc'),
                    html.Small("""Select to see % of seats filled by Passengers on flights.
                               Can filter by Airline Carrier.""", className="text-muted")
                ]),

                dbc.ListGroupItem([
                    html.Div([

                        html.H6('Passenger Utilization Details', className='my-0'),
                        html.Span(html.Small('3', style={'color': '#0B2838'}), style={'borderRadius': '50px', 'backgroundColor': 'white', 'display': 'inline-block'}, id='pass-3-desc-span')

                    ], className='w-100 d-flex justify-content-between mb-2', id='pass-3-desc'),
                    html.Small("""Select to see a detailed table on Passenger Utilization.
                               Passengers! Seats! Aircraft! Routes! Departures! 
                               Filters in column headers.""", className="text-muted")
                    
                ])



            ], className='w-100 d-flex')
        ], className='mt-3 w-100 d-flex justify-content-center')

        
        
    ]

    return returnArray