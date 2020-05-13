import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output


tab_2_layout = html.Div([
            html.H3('Work in Progress'),
            dcc.Graph(
                id='graph-2-tabs',
                figure={
                    'data': [{
                        'x': [1, 2, 3],
                        'y': [5, 10, 6],
                        'type': 'bar'
                    }]
                }
            )
        ])