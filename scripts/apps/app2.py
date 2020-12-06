import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
import numpy as np

from dash.dependencies import Input, Output
from postgresql_storage import PostgresStorage
from app import app
from datetime import date

storage = PostgresStorage()

df = pd.read_sql(storage.get_all_to_df().statement,
                 storage.session.bind).drop_duplicates().set_index('date')

layout = html.Div([
    html.H3('App 2'),
    dcc.DatePickerRange(
        id='my-date-picker-range',
        min_date_allowed=date(2000, 1, 1),
        max_date_allowed=date.today(),
        initial_visible_month=date(2020, 1, 1),
        end_date=date.today()
    ),
    html.Div(id='output-container-date-picker-range'),

    dcc.Link('Go to App 1', href='/apps/app1')
], style={})


def generate_table(dataframe):
    return dbc.Table.from_dataframe(dataframe, striped=True, bordered=True, hover=True)


@app.callback(
    dash.dependencies.Output('output-container-date-picker-range', 'children'),
    [dash.dependencies.Input('my-date-picker-range', 'start_date'),
     dash.dependencies.Input('my-date-picker-range', 'end_date')])
def update_output(start_date, end_date):
    filtered_df = pd.pivot_table(
        df, index=df.index, columns='code', values='value')

    if start_date is not None:
        start_date_object = date.fromisoformat(start_date)
        start_date_string = start_date_object.strftime('%B %d, %Y')
        filtered_df = filtered_df.loc[filtered_df.index > start_date_object]

    if end_date is not None:
        end_date_object = date.fromisoformat(end_date)
        end_date_string = end_date_object.strftime('%B %d, %Y')
        filtered_df = filtered_df.loc[filtered_df.index < end_date_object]

    log_returns = (np.log(filtered_df.diff()).std() *
                   np.sqrt(252)).sort_values().dropna()
    return html.Div([
        dbc.Row([
            dbc.Col([
                html.H5('Top 5 least volatile currencies'),
                generate_table(log_returns[:5].reset_index()),
            ], width={'size': 3, 'offset': 3}),
            dbc.Col([
                html.H5('Top 5 most volatile currencies'),
                generate_table(log_returns[-5:].reset_index()),
            ], width={'size': 3}),
        ]),
    ])


if __name__ == "__main__":
    app.run_server(debug=True)
