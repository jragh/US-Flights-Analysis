from dash import html, dcc, Input, Output, State, callback
import dash_bootstrap_components as dbc

def generateSummaryCard(title_value: str, background_color: str, card_value_text):

    return dbc.Card([
                                dbc.CardBody([
                                    html.P(title_value, style={'color': '#0B2838', 'fontSize': '0.85em', 'marginBottom': '1.5em', "fontWeight": "bold"}),
                                    html.H3(card_value_text, style={'marginBottom': 0, 'color': '#0B2838'})
                                ], style={'textAlign': 'left'}, class_name="px-4 py-3")
                            ], color=background_color, style={'borderRadius': "5px"})


## '#E89C31'