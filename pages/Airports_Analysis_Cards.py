from dash import html, dcc, Input, Output, State, callback
import dash_bootstrap_components as dbc

def generateSummaryCard(title_value: str, background_color: str, card_value_text):

    return dbc.Card([
                                dbc.CardHeader(title_value, style={'color': '#0B2838', 'textAlign': 'center'}, class_name='p-2'),
                                dbc.CardBody([
                                    html.H4(card_value_text, style={'marginBottom': 0, 'color': '#0B2838'})
                                ], style={'textAlign': 'center'}, class_name="px-2 py-3")
                            ], color=background_color, style={'borderRadius': "5px"})


## '#E89C31'