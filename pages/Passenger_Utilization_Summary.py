import polars as pl
from dash import html, dcc, Input, Output, State
import dash_bootstrap_components as dbc
import plotly_express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

import dash_ag_grid as dag

import dash

import flask

sqlite_path = 'sqlite://US_Flights_Analytics.db'

pass_summ_table_query = """SELECT UNIQUE_CARRIER_NAME as [UNIQUE CARRIER NAME],
       MONTH_NAME_SHORT AS [MONTH],
       AIRCRAFT_DESC AS [AIRCRAFT TYPE],
       NUMBER_OF_ROUTES AS [TOTAL ROUTES],
       TOTAL_PASSENGERS AS [TOTAL PASSENGERS],
       TOTAL_SEATS AS [TOTAL SEATS],
       TOTAL_DEPARTURES AS [TOTAL DEPARTURES]
  FROM T100_PASSENGER_UTILIZATION_SUMMARY"""

pass_summ_table = pl.read_database_uri(query=pass_summ_table_query, uri=sqlite_path,engine='adbc')

## column_definition = [{'field': i, 'cellStyle': {'fontSize': '11px'}} for i in list(pass_summ_table.columns)]

column_definition = [
    {'field': 'UNIQUE CARRIER NAME', 'cellStyle': {'fontSize': '11px'}, 'filter': True, 'floatingFilter': True, 
     'filter': 'agTextColumnFilter', 'filterParams': {'debounceMS': 200}, 'filterParams': {'buttons': ['apply', 'reset', 'close']}},
    {'field': 'MONTH', 'cellStyle': {'fontSize': '11px'}, 'filter': True, 'floatingFilter': True, 
     'filter': 'agTextColumnFilter', 'filterParams': {'buttons': ['apply', 'reset', 'close']}},
    {'field': 'AIRCRAFT TYPE', 'cellStyle': {'fontSize': '11px'}, 'filter': True, 'floatingFilter': True, 
     'filter': 'agTextColumnFilter', 'filterParams': {'buttons': ['apply', 'reset', 'close']}},
    {'field': 'TOTAL ROUTES', 'cellStyle': {'fontSize': '11px'}, 'filter': True, 'floatingFilter': True, 
     'filter': 'agNumberColumnFilter', 'filterParams': {'buttons': ['apply', 'reset', 'close']}},
    {'field': 'TOTAL PASSENGERS', 'cellStyle': {'fontSize': '11px'}, 'filter': True, 'floatingFilter': True, 
     'filter': 'agNumberColumnFilter', 'filterParams': {'buttons': ['apply', 'reset', 'close']}},
    {'field': 'TOTAL SEATS', 'cellStyle': {'fontSize': '11px'}, 'filter': True, 'floatingFilter': True, 
     'filter': 'agNumberColumnFilter', 'filterParams': {'buttons': ['apply', 'reset', 'close']}},
    {'field': 'TOTAL DEPARTURES', 'cellStyle': {'fontSize': '11px'}, 'filter': True, 'floatingFilter': True, 
     'filter': 'agNumberColumnFilter', 'filterParams': {'buttons': ['apply', 'reset', 'close']}}
]

summary = dag.AgGrid(
    id='passenger_utilization_summary_grid',
    rowData=pass_summ_table.to_dicts(),
    columnDefs=column_definition,
    defaultColDef={
                "resizable": True,
                "cellStyle": {"wordBreak": "normal"},
                "wrapText": True,
                "autoHeight": True,
                "wrapHeaderText": True,
                "autoHeaderHeight": True,
                "initialWidth": 50
    },
    columnSize='responsiveSizeToFit',
    columnSizeOptions={"skipHeader" : False},
    className='ag-theme-quartz ag-theme-custom',
    style={'height':"50vh"}
)




