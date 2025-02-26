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
            ], gap=1, style={'textAlign': '-webkit-center'}, className="my-4 align-items-center"
            ),

            html.Div([

                html.Span(
                    html.I(className='bi bi-people-fill me-2', style={'color': '#0B2838', 'fontSize': '4em'}), style={'display': 'inline-block'}
                ),

                html.H6('Discover insights on Passenger Airline travel throughout the United States using Passenger and Available Seat counts!', style={'fontWeight': 100})

                ], style={'margin': 'auto 0 auto 0', 'justifyContent': 'center', 'textAlign': 'center'})

        ], className='title-animate'),

        html.Div([

            dbc.Accordion([

                dbc.AccordionItem([

                    html.Small("""Select to see how many passengers flew on flights throughout the entire year.
                               Can filter by Airline Carrier.""", className="text-muted")

                ], title="Passengers By Carrier", style={'width': "100%"}, item_id='passengers-item-1'),

                dbc.AccordionItem([

                    html.Small("""Select to see % of seats filled by Passengers on flights. Can filter by Airline Carrier.""", className='text-muted')

                ], title='Passenger Utilization By Carrier (%)', style={'width': "100%"}, item_id='passengers-item-2'),

                dbc.AccordionItem([

                    html.Small("""Select to see a detailed table on Passenger Utilization. Passengers! Seats! Aircraft! Routes! Departures! 
                               Filters in column headers.""", className='text-muted')

                ], title='Passenger Utilization Details', style={'width': "100%"}, item_id='passengers-item-3'),

                dbc.AccordionItem([

                    html.Small("""Visualizes Top 10 Carrier Routes Load Factor using either the Passenger & Seat overlay chart or the Passenger Utilization % chart.
                               A specific airport must be selected (when switching to visual without any airport filter, an airport will automatically be selected).""",
                               className='text-muted')

                ], title='Top 10 Passenger Routes By Carrier', style={'width': "100%"}, item_id='passengers-item-4')

            ], class_name='d-flex flex-column w-100 flex-grow-1', id='passenger-viz-accordion', active_item='passengers-item-1')

        ], className='mt-3 mb-2 w-100 d-flex flex-column justify-content-center overflow-y-scroll')
        
    ]

    return returnArray