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
            ], gap=1, style={'textAlign': '-webkit-center'}, className="my-4 align-items-center"
        ),

        html.Div([

            html.Span([html.I(className='bi bi-buildings-fill', style={'color': '#0B2838', 'fontSize': '4em'})], style={'display': 'inline-block'}),
            html.H6('Explore data and stats about Airports across the United States.', style={'fontWeight': 100})

        ], style={'margin': 'auto', 'textAlign': 'center', 'justify': 'center'})

        ], className='title-animate'),

        html.Div([

            dbc.Accordion([

                dbc.AccordionItem([

                    html.Small("""Compare Carriers by the number of Departed Flights vs Number of distinct destinations for a given airport. 
                               Bubble sizes are based on the number of passengers transported.""", className="text-muted")

                ], title="Routes vs Flights (Scatter)", style={'width': "100%"}, item_id='airports-item-1'),

                dbc.AccordionItem([

                    html.Small("""Provides Cards with Summary Statisitcs, along with a Treemap based on Carriers and Passengers Transported.
                               Includes Passengers Transported, Departed Flights, Total Carriers, and Total Destinations.""", className='text-muted')

                ], title="Airport Summary Treemap", style={'width': "100%"}, item_id='airports-item-2')

            ], class_name='d-flex flex-column w-100 flex-grow-1', id='airport-viz-accordion', active_item='airports-item-2')

        ], className='mt-3 w-100 d-flex flex-column justify-content-center overflow-y-scroll') 

    ]

    return return_array