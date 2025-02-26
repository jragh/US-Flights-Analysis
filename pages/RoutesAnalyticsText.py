import dash_bootstrap_components as dbc
from dash import html

def routes_text():

    return_array = [

        html.Div([

            dbc.Stack(
            [
                html.Span(
                    html.H1('ROUTE'), className= 'header-span'
                ),
                html.Span(
                    html.H1('ANALYTICS'), className = 'header-span'
                )
            ], gap=1, style={'textAlign': '-webkit-center'}, className="my-4 align-items-center"
        ),

        html.Div([
            
                html.Span([html.I(className='bi bi-signpost-split-fill', style={'color': '#0B2838', 'fontSize': '4em'})], style={'display': 'inline-block'}),
                html.H6('A deeper dive on Market Pairs and Air Travel Routes across the United States.', style={'fontWeight': 100})
    
        ], style={'margin': 'auto', 'textAlign': 'center', 'justify': 'center'})


        ], className='title-animate'),

        html.Div([

            dbc.Accordion([

                dbc.AccordionItem([

                    html.Small("""Compare Carriers by the estimated revenue generated between 2 city market pairs (both directions). 
                               Revenue estimate is based on the Number of Passengers travelling between the selected airports,
                               multiplied by the Average Fare for the market pair. 
                               (Revenue data only includes the Top 1000 Market Pairs in the contiguous United States)""", className="text-muted")

                ], title="Market Pairs: Revenue By Carrier", style={'width': "100%"}, item_id='routes-item-1'),

                dbc.AccordionItem([

                    html.Small("""A deeper look at passenger travel between 2 airports (both ways), 
                               comparing Passenger Counts, Available Seats, and Passenger Utilizaiton Rates by Airline Carrier.
                               Viewing All Carriers will give total counts, while viewing a specific Airline Carrier will give a monthly breakdown.
                               Small Airline Carriers grouped as 'Other Carriers'.""", className='text-muted')

                ], title='Airport Pairs: Passenger Util % By Carrier', style={'width': '100%'}, item_id='routes-item-2'),

                dbc.AccordionItem([

                    html.Small("""Scatter view allows you to assess load factors (Percentage of available seating capacity that is filled with passengers) for each route an airline carrier operates. 
                               When viewing All Carriers, the scatter points show the airlines overall load factor vs. how many flights they operate (minimum 200 departures performed). 
                               Individual airline carrier view allows the user to see the load factor for each route vs. the number of flights (minimum 20 departures performed for the route).""", className='text-muted')

                ], title='Scatter Analysis: Load Factor By Carrier', item_id='routes-item-3', style={'width': '100%'})

            ], class_name='d-flex flex-column w-100 flex-grow-1', id='route-viz-accordion', active_item='routes-item-1')

        ], className='mt-3 mb-2 w-100 d-flex flex-column justify-content-center overflow-y-scroll') 

    ]

    return return_array