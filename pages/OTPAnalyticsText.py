import dash_bootstrap_components as dbc
from dash import html

import dash_bootstrap_components as dbc
from dash import html

def otp_text():

    return_array = [

        html.Div([

            dbc.Stack(
            [
                html.Span(
                    html.H1('ON TIME'), className= 'header-span'
                ),

                html.Span(
                    html.H1('PERFORMANCE'), className= 'header-span'
                ),

                html.Span(
                    html.H1('ANALYTICS'), className = 'header-span'
                )
            ], gap=1, style={'textAlign': '-webkit-center'}, className="my-4 align-items-center"
        ),

        html.Div([
            
                html.Span([html.I(className='bi bi-hourglass-split', style={'color': '#0B2838', 'fontSize': '4em'})], style={'display': 'inline-block'}),
                html.H6('A deeper dive on Passenger On-Time Performance across the United States.', style={'fontWeight': 100})
    
        ], style={'margin': 'auto', 'textAlign': 'center', 'justify': 'center'})


        ], className='title-animate'),

        html.Div([

            dbc.Accordion([

                dbc.AccordionItem([

                    html.Small("""View average Arrival Delay times in minutes on a daily basis for each available American Carrier.
                               Toggle switch allows choice between Late Arrivals only or All Arrivals (Early, On Time, Late).
                               Includes 95% Confidence Intervals. """, className="text-muted")

                ], title="Average Arrival Delay By Carrier (Daily)", style={'width': "100%"}, item_id='otp-item-1')

            ], class_name='d-flex flex-column w-100 flex-grow-1', id='otp-viz-accordion', active_item='otp-item-1')

        ], className='mt-3 mb-2 w-100 d-flex flex-column justify-content-center overflow-y-scroll', style={'height': '45vh'}) 

    ]

    return return_array