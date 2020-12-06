import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd

from dash.dependencies import Input, Output
from postgresql_storage import PostgresStorage

storage = PostgresStorage()

df = pd.read_sql(storage.get_all_to_df().statement, storage.session.bind).drop_duplicates()

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

codes_df = df.code.unique()

app.layout = html.Div([
    html.Label('Multi-Select Currency Dropdown'),
    dcc.Dropdown(
        id='demo-dropdown',
        options=[{'label': value, 'value': value} for value in codes_df],
        value=[],
        multi=True
    ),
    html.Div(id='dd-output-container')
], style={})


@app.callback(
    dash.dependencies.Output('dd-output-container', 'children'),
    [dash.dependencies.Input('demo-dropdown', 'value')])
def update_output(values):
    content = []
    for value in values:
        filtered_df = df[df.code == value].set_index('date').sort_index()

        print(filtered_df.head(10))
        content.append(
            html.Div([
                dbc.Row([
                    html.H6(f'Graphs for currency: {value}'),
                    dbc.Col(dcc.Graph(
                        id=f'hist-{value}',
                        figure=px.histogram(filtered_df, x='value')
                    ), width={'size': 3, 'offset': 3}),
                    dbc.Col(dcc.Graph(
                        id=f'boxplot-{value}',
                        figure=px.box(filtered_df, y='value')
                    ), width={'size': 3}),
                ]),
                dbc.Row(dcc.Graph(
                    id=f'timeline-{value}',
                    figure=px.line(filtered_df, x=filtered_df.index, y='value')
                ))
            ])
        )

    return html.Div(content)


if __name__ == "__main__":
    app.run_server(debug=True)
