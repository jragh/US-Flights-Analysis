import polars as pl
from dash import html, dcc, Input, Output, State
import dash_bootstrap_components as dbc
import plotly_express as px

from flask import Flask, redirect

import dash

# from Passenger_Utilization_Summary import summary
# from PassengerAnalyticsText import passengerText
# from flightsNavbar import navbar_named

from pages import flightsNavbar

# sqlite_path = 'sqlite://US_Flights_Analytics.db'

dbc_css = "https://cdn.jsdelivr.net/gh/AnnMarieW/dash-bootstrap-templates/dbc.min.css"

# passenger_viz_list = ['Passengers By Carrier', 'Passenger Utilization By Carrier (%)', 'Passenger Utilization Details']

# analytics_df = pl.read_database_uri(query="SELECT * FROM T100_SEGMENT_ALL_CARRIER_2023 where CAST([PASSENGERS] as FLOAT) > 0 and CAST(SEATS as FLOAT) > 0 and CAST([DEPARTURES_PERFORMED] as FLOAT) > 0 ORDER BY [UNIQUE_CARRIER_NAME], ROUND(CAST([PASSENGERS] as FLOAT), 2) desc", uri=sqlite_path,engine='adbc')

# print(analytics_df.head(25))


# ## TODO: Idea for Carrier sorted list: Group by, then sort by Number of Passengers Flown descending, then select single column, to dicts, etc; 
# carrier_filter_list = sorted([val['UNIQUE_CARRIER_NAME'] for val in analytics_df.select(['UNIQUE_CARRIER_NAME']).unique().to_dicts()])

# ## TODO: Remove Global variable when we have the sheet selection ##
# textResults = passengerText()

server = Flask(__name__)

@server.route('/')
def index_redirect():
    return redirect('/Home')


app = dash.Dash(__name__, external_stylesheets=[dbc.themes.ZEPHYR, dbc_css, dbc.icons.BOOTSTRAP], use_pages=True, suppress_callback_exceptions=True, server=server)


## dash.register_page(__name__, path='/')

## Debugging for page registry ##
## print(dash.page_registry.values())

app.layout = dbc.Container([
    dcc.Location(id='app-location-id'),
    html.Div([

        dbc.Row(id='app-navbar-row-output')

    ], style={'margin': '0'}),
    dash.page_container
], class_name='m-0 g-0 w-100', id='PlsFix', fluid=True)


## Callback for Global Navbar; Will update the pill based on that ##
@app.callback(

    Output(component_id='app-navbar-row-output', component_property='children'),
    [Input(component_id='app-location-id', component_property='pathname')]
    
)
def pathnameCallback(path):

    pathname_pill_pair = {'/Home': 'Home', 
                          '/PassengerAnalytics': 'Passenger Analytics', 
                          '/AirportAnalytics' : 'Airport Analytics', 
                          '/RouteAnalytics': 'Route Analytics',
                          "/": 'Home',
                          "/OnTimePerformance": "On Time Performance"
                          }

    return_children = [
        dbc.Col([
            flightsNavbar.navbar_named(pathname_pill_pair[path]),

            ## Stores used by Routes Page ##
            dcc.Store(id='routes-airport-store-1', data={'airport-name-1': 'Los Angeles, CA: Los Angeles International'}, storage_type='memory'),
        
            dcc.Store(id='routes-airport-store-2', data={'airport-name-2': 'New York, NY: John F. Kennedy International'}, storage_type='memory')
        ], width=12)
        ]

    return return_children


# app.layout = dbc.Container([
#     dbc.Row([
#         dbc.Col([
#             navbar_named('Passenger Analytics')
#         ], width=12)
#     ]),
#     dbc.Row([

#         dbc.Col(children = textResults,
#                  id='sidebar', className = 'textSidebar',width = 12, lg = 4, md =12, xl = 4, xxl = 4, sm = 12, align='start'),

#         dbc.Col(children=[

#             dbc.Row([dbc.Col([

#                 ## Header for the Graph Section
#                 html.Hr(),

#                 dbc.Row([
#                     dbc.Col([
                        
#                         dbc.Card(
#                             dbc.CardBody(
#                                 [
#                                     dbc.Label('Airline Carrier Selection:  '),
#                                     html.Div([dcc.Dropdown(options=carrier_filter_list, multi=False, searchable=True, clearable=True, 
#                                                            placeholder='Select an Airline Carrier here...', id='passenger-carrier-selection',
#                                                            style={'fontSize': '12px'})], className='dbc mb-2')

#                                 ], className='pt-3 pb-2'
#                             ), className='bg-light text-dark border rounded-3'
#                         )

#                     ], width=12, md=8, id='carrier-selection-col', className='mb-2'),

#                     dbc.Col([

#                         dbc.Card(
#                             dbc.CardBody([
#                                 dbc.Label('Visual Selection: '),
#                                 html.Div([dcc.Dropdown(options=passenger_viz_list, value='Passengers By Carrier', multi=False, searchable=True, clearable=False, 
#                                                        placeholder='Select an Data Viz hre...', id='passenger-viz-selection',
#                                                        style={'fontSize': '12px'})], className='dbc mb-2')

#                             ], className='pt-3 pb-2'
#                             ), className='bg-light text-dark border rounded-3'
#                         )

#                     ], width=12, md=4, id='visual-selection-col', className='mb-2')
#                 ]),

                

                
                

#                 ## Creating Graph Component for quick analytics ##
#                 dbc.Spinner([
#                     html.Div([
#                         html.H2('All Carriers: Number of Passengers Transported', id='graph-header'),
#                         html.Hr(className='my-2'),
#                         html.P('', className='mb-2', id='passenger-graph-desc'),

#                         dcc.Graph(id='passengers-graph', style={'height': '50vh'})
#                     ], className='p-4 bg-light text-dark border rounded-3', id='pass_visual_div')
#                 ], show_initially=True, spinner_style={'height': '3rem', 'width': '3rem'})


                

#             ])], align="center")
            
            

#         ], id='graph_section', width = 12, lg = 8, md = 12, xl = 8, xxl = 8, sm=12, class_name='px-2')

#     ])
# ], fluid=True, className='mr-4 ml-4')

# @app.callback(
#     Output(component_id='pass_visual_div', component_property='children'),
#     [Input(component_id='passenger-carrier-selection', component_property='value'),
#      Input(component_id='passenger-viz-selection', component_property='value')
#     ]
# )
# def passengers_carrier_selection(selected_carrier, selected_pass_viz):

#     months_text = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

#     ## First Return is Passengers By Carrier ##
#     if selected_pass_viz == 'Passengers By Carrier':

#         pass_graph_desc = 'Provides the total number of passengers transported on flights throughout the entire year for the given carrier. (All Carriers shown if none provided)'
        
#         pass_carrier = pl.read_database_uri(query='SELECT * FROM T100_PASSENGERS_BY_CARRIER_2023', uri=sqlite_path,engine='adbc')

#         if selected_carrier is None or selected_carrier.strip() == '':

#             bar_figure = px.bar(pass_carrier.select(['MONTH', 'TOTAL PASSENGERS']).group_by(pl.col('MONTH')).sum(), x='MONTH', y='TOTAL PASSENGERS',
#                                 text_auto='.2s', title='Passengers Transported By Month: All Carriers')

#             bar_figure.update_traces(textposition='outside', textangle=0, marker_color="#0B2838", marker={"cornerradius":4})

#             bar_figure.update_xaxes(categoryorder='array', categoryarray=months_text, linewidth=2.5, showgrid=False, linecolor='rgb(204, 204, 204)')

#             bar_figure.update_yaxes( showgrid=True, zeroline=False, showline=False, showticklabels=True, tickwidth=2,gridcolor="rgba(30, 63, 102, 0.15)")

#             bar_figure.update_layout(plot_bgcolor='white')

#             return_children = [
#                 html.H2('All Carriers: Number of Passengers Transported', id='graph-header'),
#                 html.Hr(className='my-2'),
#                 html.P(pass_graph_desc, className='mb-2 text-muted', id='passenger-graph-desc'),
#                 dcc.Graph(figure=bar_figure, id='passengers-graph', style={'height': '52vh'})
#             ]

#             return return_children
        
#         else:

#             bar_figure = px.bar(pass_carrier.filter(pl.col('UNIQUE_CARRIER_NAME') == selected_carrier), x='MONTH', y='TOTAL PASSENGERS',
#                                 text_auto='.2s', title=f'Passengers Transported By Month: {selected_carrier}')

#             bar_figure.update_traces(textposition='outside', textangle=0, marker_color="#0B2838", marker={"cornerradius":4})

#             bar_figure.update_xaxes(categoryorder='array', categoryarray=months_text, linewidth=2.5, showgrid=False, linecolor='rgb(204, 204, 204)')
            
#             bar_figure.update_yaxes( showgrid=True, zeroline=False, showline=False, showticklabels=True, tickwidth=2, gridcolor="rgba(30, 63, 102, 0.15)")

#             bar_figure.update_layout(plot_bgcolor='white')

#             return_children = [
#                 html.H2(f'{selected_carrier}: Number of Passengers Transported', id='graph-header'),
#                 html.Hr(className='my-2'),
#                 html.P(pass_graph_desc, className='mb-2 text-muted', id='passenger-graph-desc'),
#                 dcc.Graph(figure=bar_figure, id='passengers-graph', style={'height': '52vh'})
#             ]
            

#             return return_children
        

#     ## Second Return is for showing seat usage utilization ## 
#     elif selected_pass_viz == 'Passenger Utilization By Carrier (%)':

#         pass_graph_desc = 'Provides the percentage of seats used by passnegers (Passengers Divided By Seats) for the given carrier throughout the year. (All Carriers shown if none provided)'

#         if selected_carrier is None or selected_carrier.strip() == '':

#             pass_util_carrier = pl.read_database_uri(query='select a.* from T100_PASSENGER_UTILIZATION_TOTAL_2023 a left join [MONTHS_LOOKUP] b on a.[MONTH] = b.[MONTH_NAME_SHORT] order by CAST(b.[MONTH] as int) asc', uri=sqlite_path,engine='adbc')

#             bar_figure = px.bar(pass_util_carrier.select(['MONTH', 'TOTAL SEATS', 'TOTAL PASSENGERS']).group_by(pl.col('MONTH')).sum(),
#                                 x='MONTH', y=['TOTAL SEATS', 'TOTAL PASSENGERS'], title='Passenger Seat Utilization: All Carriers',
#                                 barmode='group', text_auto='.3s')
            
#             bar_figure.update_traces(textposition='outside', textangle=0)

#             bar_figure.update_yaxes( showgrid=True, zeroline=False, showline=False, showticklabels=True, tickwidth=2, gridcolor="rgba(30, 63, 102, 0.15)")

#             ## Add in Line Figure
#             line_figure = px.line(pass_util_carrier.select(['MONTH', 'PASSENGER UTILIZATION PCT']), x='MONTH', y='PASSENGER UTILIZATION PCT',
#                                   category_orders={'MONTH': months_text}, markers=True)

#             line_figure.update_xaxes(type='category')

#             line_figure.update_traces(yaxis ="y2", line_color="rgba(255, 183, 3, 0.6)", name='PASSENGER UTILIZATION PCT', showlegend=True)

#             bar_figure.add_traces(list(line_figure.select_traces())).update_layout(yaxis2={"overlaying":"y", "side":"right", 'rangemode': "tozero", "tickformat":'.1%', "title": "Seats / Passengers (%)"},
#                                                                   yaxis1={"rangemode": "normal", "title" : "Total Seats or Passengers"})

#             bar_figure.update_xaxes(categoryorder='array', categoryarray=months_text, linewidth=2.5, showgrid=False, linecolor='rgb(204, 204, 204)')

#             bar_figure.update_layout(plot_bgcolor='white')

#             ## Adding in Horizontal Legend
#             bar_figure.update_layout(plot_bgcolor='white', legend_title=None, legend=dict(orientation="h", xanchor="center", x=0.5, yanchor='bottom', y=-0.32), hovermode="x unified", xaxis_title=None)

#             ## Set Bar Colors ##
#             bar_figure.update_traces(marker_color="#023E8A", selector={"name": "TOTAL SEATS"}, marker={"cornerradius":4})

#             bar_figure.update_traces(marker_color="#A2D2FF", selector={"name": "TOTAL PASSENGERS"}, marker={"cornerradius":4})

#             bar_figure.update_traces(hovertemplate="%{y}")

#             return_children = [
#                 html.H2('All Carriers: Passenger Util. (%)', id='graph-header'),
#                 html.Hr(className='my-2'),
#                 html.P(pass_graph_desc, className='mb-2 text-muted', id='passenger-graph-desc'),
#                 dcc.Graph(figure=bar_figure, id='passengers-graph', style={'height': '52vh'})
#             ]

#             return return_children
        
#         else:

#             pass_util_carrier = pl.read_database_uri(query='select a.* from T100_PASSENGER_UTILIZATION_BY_CARRIER_2023 a left join [MONTHS_LOOKUP] b on a.[MONTH] = b.[MONTH_NAME_SHORT] order by CAST(b.[MONTH] as int) asc', uri=sqlite_path,engine='adbc')

#             bar_figure = px.bar(pass_util_carrier.filter(pl.col('UNIQUE_CARRIER_NAME') == selected_carrier).select(['MONTH', 'TOTAL SEATS', 'TOTAL PASSENGERS']),
#                                 x='MONTH', y=['TOTAL SEATS', 'TOTAL PASSENGERS'], title=f'Passenger Seat Utilization Pct: {selected_carrier}',
#                                 barmode='group', text_auto='.3s')
            

            
#             bar_figure.update_traces(textposition='outside', textangle=0)

#             bar_figure.update_yaxes( showgrid=True, zeroline=False, showline=False, showticklabels=True, tickwidth=2, gridcolor="rgba(30, 63, 102, 0.15)")

#             ## Add in Line Figure
#             line_figure = px.line(pass_util_carrier.filter(pl.col('UNIQUE_CARRIER_NAME') == selected_carrier).select(['MONTH', 'PASSENGER UTILIZATION PCT']),
#                                   x='MONTH', y='PASSENGER UTILIZATION PCT', category_orders={'MONTH': months_text}, markers=True)
            
#             line_figure.update_xaxes(type='category')

#             line_figure.update_traces(yaxis ="y2", line_color="rgba(255, 183, 3, 0.6)", name='PASSENGER UTILIZATION PCT', showlegend=True)

#             bar_figure.add_traces(list(line_figure.select_traces())).update_layout(yaxis2={"overlaying":"y", "side":"right", 'rangemode': "tozero", "tickformat":'.1%', "title": "Seats / Passengers (%)"},
#                                                                   yaxis1={"rangemode": "normal", "title" : "Total Seats or Passengers"})

#             bar_figure.update_xaxes(categoryorder='array', categoryarray=months_text, linewidth=2.5, showgrid=False, linecolor='rgb(204, 204, 204)')

#             ## Adding in Horizontal Legend
#             bar_figure.update_layout(plot_bgcolor='white', legend_title=None, legend=dict(orientation="h", xanchor="center", x=0.5, yanchor='bottom', y=-0.32), hovermode="x unified", xaxis_title=None)

#             ## Set Bar Colors ##
#             bar_figure.update_traces(marker_color="#023E8A", selector={"name": "TOTAL SEATS"}, marker={"cornerradius":4})

#             bar_figure.update_traces(marker_color="#A2D2FF", selector={"name": "TOTAL PASSENGERS"}, marker={"cornerradius":4})

#             bar_figure.update_traces(hovertemplate="%{y}")

#             return_children = [
#                 html.H2(f'{selected_carrier}: Passenger Seat Utilization Pct', id='graph-header'),
#                 html.Hr(className='my-2'),
#                 html.P(pass_graph_desc, className='mb-2 text-muted', id='passenger-graph-desc'),
#                 dcc.Graph(figure=bar_figure, id='passengers-graph', style={'height': '52vh'})
#             ]

#             return return_children
        
    
#     ## Return Dash AG Grid for Summary Table on Passenger Utilization ##
#     elif selected_pass_viz == 'Passenger Utilization Details':

#         pass_graph_desc = 'Provides a summary table of Unique Routes, Passengers, Seats & Passenger Utilization Rate through the year for each carrier (Table is filterable)'

#         dag_table = summary

#         return_children = [
#                 html.H2('Passenger Utilization Details', id='graph-header'),
#                 html.Hr(className='my-2'),
#                 html.P(pass_graph_desc, className='mb-3 text-muted', id='passenger-graph-desc'),
#                 dag_table
#         ]

#         return return_children



# @app.callback(
#     Output(component_id='passenger-carrier-selection', component_property='disabled'),
#     Output(component_id='passenger-carrier-selection', component_property='value'),
#     [Input(component_id='passenger-viz-selection', component_property='value')],
#     State(component_id='passenger-carrier-selection', component_property='value')
# )
# def pass_details_disable_carrier(selected_pass_viz, carrier_state):

#     if selected_pass_viz == 'Passenger Utilization Details':

#         return True, None
    
#     return False, carrier_state


# ## This Callback is for the Passenger visualization components ##
# @app.callback(
#     Output(component_id='pass-1-desc', component_property='children'),
#     Output(component_id='pass-2-desc', component_property='children'),
#     Output(component_id='pass-3-desc', component_property='children'),
#     [Input(component_id='passenger-viz-selection', component_property='value')]
# )
# def highlight_active_pass_viz(selected_viz):

#     old_style = {'borderRadius': '50px', 'backgroundColor': 'white', 'display': 'inline-block'}

#     highlight_style = {'borderRadius': '50px', 'backgroundColor': '#0B2838', 'display': 'inline-block', 'padding': '0.09em 0.6em'}

#     if selected_viz == 'Passengers By Carrier':

#         child_1 = [
#             html.H6('Passengers By Carrier', className='my-0'),
#             html.Span(html.Small('1', style={'color': '#E89C31'}), style=highlight_style, id='pass-1-desc-span')
#                     ]
        
#         child_2 = [
#             html.H6('Passenger Utilization By Carrier (%)', className='my-0'),
#             html.Span(html.Small('2', style={'color': '#0B2838'}), style=old_style, id='pass-2-desc-span')
#                 ]
        
#         child_3 = [
#             html.H6('Passenger Utilization Details', className='my-0'),
#             html.Span(html.Small('3', style={'color': '#0B2838'}), style=old_style, id='pass-3-desc-span')
#                 ]
        
#         return child_1, child_2, child_3
    

#     elif selected_viz == 'Passenger Utilization By Carrier (%)':

#         child_1 = [
#             html.H6('Passengers By Carrier', className='my-0'),
#             html.Span(html.Small('1', style={'color': '#0B2838'}), style=old_style, id='pass-1-desc-span')
#                     ]
        
#         child_2 = [
#             html.H6('Passenger Utilization By Carrier (%)', className='my-0'),
#             html.Span(html.Small('2', style={'color': '#E89C31'}), style=highlight_style, id='pass-2-desc-span')
#                 ]
        
#         child_3 = [
#             html.H6('Passenger Utilization Details', className='my-0'),
#             html.Span(html.Small('3', style={'color': '#0B2838'}), style=old_style, id='pass-3-desc-span')
#                 ]
        
#         return child_1, child_2, child_3
    


#     elif selected_viz == 'Passenger Utilization Details':

#         child_1 = [
#             html.H6('Passengers By Carrier', className='my-0'),
#             html.Span(html.Small('1', style={'color': '#0B2838'}), style=old_style, id='pass-1-desc-span')
#                     ]
        
#         child_2 = [
#             html.H6('Passenger Utilization By Carrier (%)', className='my-0'),
#             html.Span(html.Small('2', style={'color': '#0B2838'}), style=old_style, id='pass-2-desc-span')
#                 ]
        
#         child_3 = [
#             html.H6('Passenger Utilization Details', className='my-0'),
#             html.Span(html.Small('3', style={'color': '#E89C31'}), style=highlight_style, id='pass-3-desc-span')
#                 ]
        
#         return child_1, child_2, child_3


if __name__ == "__main__":
    app.run_server(debug=True)