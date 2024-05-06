import polars as pl
from dash import html, dcc, Input, Output, State
import dash_bootstrap_components as dbc
import plotly_express as px

import dash

sqlite_path = 'sqlite://US_Flights_Analytics.db'

dbc_css = "https://cdn.jsdelivr.net/gh/AnnMarieW/dash-bootstrap-templates/dbc.min.css"

passenger_viz_list = ['Passengers By Carrier', 'Passenger Utilization By Carrier (%)', 'Passenger Utilization Monthly']

analytics_df = pl.read_database_uri(query='SELECT * FROM T100_SEGMENT_ALL_CARRIER_2023 ORDER BY ROUND(CAST([PASSENGERS] as FLOAT), 2) desc', uri=sqlite_path,engine='adbc')

print(analytics_df.head(25))


## TODO: Idea for Carrier sorted list: Group by, then sort by Number of Passengers Flown descending, then select single column, to dicts, etc; 
carrier_filter_list = sorted([val['UNIQUE_CARRIER_NAME'] for val in analytics_df.select(['UNIQUE_CARRIER_NAME']).unique().to_dicts()])

print(carrier_filter_list)

print(type(carrier_filter_list))

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.ZEPHYR, dbc_css])


app.layout = dbc.Container([
    dbc.Row([

        dbc.Col(children =[
            html.H1('Hello World')
        ], id='sidebar', width = 12, lg = 4, md = 6, xl = 4, xxl = 4, sm = 12, align="center"),

        dbc.Col(children=[

            dbc.Row([dbc.Col([

                ## Header for the Graph Section
                html.H2('Graphs will go here', style={'textAlign': 'center'}),
                html.Hr(),

                dbc.Row([
                    dbc.Col([
                        
                        dbc.Card(
                            dbc.CardBody(
                                [
                                    dbc.Label('Airline Carrier Selection:  '),
                                    html.Div([dcc.Dropdown(options=carrier_filter_list, multi=False, searchable=True, clearable=True, 
                                                           placeholder='Select an Airline Carrier here...', id='carrier-selection',
                                                           style={'fontSize': '12px'})], className='dbc mb-2')

                                ], className='pt-3 pb-2'
                            ), className='bg-light text-dark border rounded-3'
                        )

                    ], width=12, md=8, id='carrier-selection-col', className='mb-2'),

                    dbc.Col([

                        dbc.Card(
                            dbc.CardBody([
                                dbc.Label('Visual Selection: '),
                                html.Div([dcc.Dropdown(options=passenger_viz_list, value='Passengers By Carrier', multi=False, searchable=True, clearable=False, 
                                                       placeholder='Select an Data Viz hre...', id='passenger-viz-selection',
                                                       style={'fontSize': '12px'})], className='dbc mb-2')

                            ], className='pt-3 pb-2'
                            ), className='bg-light text-dark border rounded-3'
                        )

                    ], width=12, md=4, id='visual-selection-col', className='mb-2')
                ]),

                

                
                

                ## Creating Graph Component for quick analytics ##
                html.Div([
                    html.H2('All Carriers: Number of Passengers Transported', id='graph-header'),
                    html.Hr(className='my-2'),
                    html.P('Provivides the total number of passengers transported on flights throughout the entire year for the given carrier. (All Carriers shown if none provided)', className='mb-2'),

                    dcc.Graph(id='passengers-graph')
                ], className='p-4 bg-light text-dark border rounded-3')


                

            ])], align="center")
            
            

        ], id='graph_section', width = 12, lg = 8, md = 6, xl = 4, xxl = 8, sm=12, class_name='px-2')

    ])
])

@app.callback(
    Output(component_id='passengers-graph', component_property='figure'),
    Output(component_id='graph-header', component_property='children'),
    [Input(component_id='carrier-selection', component_property='value'),
     Input(component_id='passenger-viz-selection', component_property='value')
    ]
)
def passengers_carrier_selection(selected_carrier, selected_pass_viz):

    months_text = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

    ## First Return is Passengers By Carrier ##
    if selected_pass_viz == 'Passengers By Carrier':
        
        pass_carrier = pl.read_database_uri(query='SELECT * FROM T100_PASSENGERS_BY_CARRIER_2023', uri=sqlite_path,engine='adbc')

        if selected_carrier is None or selected_carrier.strip() == '':

            bar_figure = px.bar(pass_carrier.select(['MONTH', 'TOTAL PASSENGERS']).group_by(pl.col('MONTH')).sum(), x='MONTH', y='TOTAL PASSENGERS', text_auto='.2s', title='Passengers Transported By Month: All Carriers')

            bar_figure.update_traces(textposition='outside', textangle=0)

            bar_figure.update_xaxes(categoryorder='array', categoryarray=months_text, linewidth=2.5, showgrid=False, linecolor='rgb(204, 204, 204)')

            bar_figure.update_yaxes( showgrid=True, zeroline=False, showline=False, showticklabels=True, tickwidth=2,gridcolor="rgba(30, 63, 102, 0.15)")

            bar_figure.update_layout(plot_bgcolor='white')

            return bar_figure, ['All Carriers: Number of Passengers Transported']
        
        else:

            bar_figure = px.bar(pass_carrier.filter(pl.col('UNIQUE_CARRIER_NAME') == selected_carrier), x='MONTH', y='TOTAL PASSENGERS', text_auto='.2s', title=f'Passengers Transported By Month: {selected_carrier}')

            bar_figure.update_traces(textposition='outside', textangle=0)

            bar_figure.update_xaxes(categoryorder='array', categoryarray=months_text, linewidth=2.5, showgrid=False, linecolor='rgb(204, 204, 204)')
            
            bar_figure.update_yaxes( showgrid=True, zeroline=False, showline=False, showticklabels=True, tickwidth=2, gridcolor="rgba(30, 63, 102, 0.15)")

            bar_figure.update_layout(plot_bgcolor='white')
            


            return bar_figure, [f'{selected_carrier}: Number of Passengers Transported']

    ## Second Return is for showing seat usage utilization ##   
    




if __name__ == "__main__":
    app.run_server(debug=True, port=8888)