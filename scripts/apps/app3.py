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

from statsmodels.tsa.stattools import coint


def find_cointegrated_pairs(data):
    n = data.shape[1]
    score_matrix = np.zeros((n, n))
    pvalue_matrix = np.ones((n, n))
    keys = data.keys()
    pairs = []
    for i in range(n):
        for j in range(i+1, n):
            S1 = data[keys[i]]
            S2 = data[keys[j]]
            result = coint(S1, S2)
            score = result[0]
            pvalue = result[1]
            score_matrix[i, j] = score
            pvalue_matrix[i, j] = pvalue
            if pvalue < 0.05:
                pairs.append((keys[i], keys[j]))
    return score_matrix, pvalue_matrix, pairs

storage = PostgresStorage()

df = pd.read_sql(storage.get_all_to_df().statement,
                 storage.session.bind).drop_duplicates().set_index('date')

df = pd.pivot_table(
        df, index=df.index, columns='code', values='value')

scores, pvalues, pairs = find_cointegrated_pairs(df)
print(pairs, pvalues)

layout = html.Div([
    html.H3('App 3'),
    dbc.Row(dbc.Col(dcc.Graph(
        id=f'heatmap',
        figure=px.imshow(pvalues, x=df.columns, y=df.columns)
    ), width={'size': 6, 'offset': 3})),
    dcc.Link('Go to App 1', href='/apps/app1'),
    dcc.Link('Go to App 2', href='/apps/app2')
], style={})
