import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import pandas as pd

patient_data_dd_df = pd.read_csv('https://raw.githubusercontent.com/niteen11/CUNY_DATA_698/master/dataset_diabetes/diabetic_data.csv')

df_med_readmit_final = patient_data_dd_df[(patient_data_dd_df['medical_specialty']!='?')]

tab_2_layout = html.Div([
            html.Div([
                html.Div([
                    html.H6('Medical Specialty'),
                    dcc.Dropdown(
                        id='page-1-dropdown',
                        options=[{'label': opt, 'value': opt} for opt in
                                 df_med_readmit_final.medical_specialty.unique()],
                        value='InternalMedicine'
                    ),
                    html.Div(id='page-1-content')
                ], className="six columns"),

                html.Div([
                    html.H6('Re-Admission (Days)'),
                    dcc.Dropdown(
                        id='page-1-dropdown2',
                        # options=[{'label': opt, 'value': opt} for opt in
                        #          df.medical_specialty.unique()],
                        options=[{'label': i, 'value': i} for i in ['>30', '<30', 'NO']],
                                value='<30'
                    ),
                    html.Div(id='page-2-content')
                ], className="six columns"),

            ], className="row", style={"margin": "1% 3%"})
    ])
