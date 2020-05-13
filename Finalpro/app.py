import dash
from dash.dependencies import Input, Output
import dash_html_components as html
import dash_core_components as dcc
from assets import pat_dem, pat_med, pat_readmit
import pandas as pd
#import plotly.graph_objs as go
import plotly.figure_factory as ff

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

server = app.server

colors = {"background": "#F3F6FA", "background_div": "white", 'text': '#009999'}

app.config['suppress_callback_exceptions']= True

patient_data_df = pd.read_csv('https://raw.githubusercontent.com/vijay564/DATA608/master/dataset_diabetes/diabetic_data.csv')

# Create the dictionary
event_dictionary = {1 : 'Emergency', 2 : 'Urgent', 3 : 'Elective',4:'Newborn',5:'Unknown',6:'Unknown',7:'TraumaCenter',8:'Unknown'}
patient_data_df['admit_type'] = patient_data_df['admission_type_id'].map(event_dictionary)

df_med_readmit_final = pd.DataFrame(patient_data_df.groupby(['medical_specialty','admit_type','time_in_hospital','num_lab_procedures',
                                                             'num_medications','readmitted']).size()).reset_index()
df_med_readmit_final = df_med_readmit_final[(df_med_readmit_final['medical_specialty']!='?')]
df_med_readmit_final.rename(columns={0:"count"}, inplace=True)
df_med_readmit_final = df_med_readmit_final.sort_values(by=['count'], ascending=False)

# print(df_med_readmit_final.head(10))

df_gender_race_age_final = pd.DataFrame(patient_data_df.groupby(['race','gender','age']).size()).reset_index()
df_gender_race_age_final.rename(columns={0:"count"}, inplace=True)
df_gender_race_age_final = df_gender_race_age_final.replace('?','Unknown')

#race- age
df_race_age_final = df_gender_race_age_final.groupby(['age','race']).sum().reset_index()

df_ms_final = df_med_readmit_final


app.layout = html.Div(style={'backgroundColor': colors['background']}, children=[
    html.H1('Patient Re-admissions Data', style={
            'textAlign': 'center',
            'color': colors['text']
        }),
    
     html.H4('CUNY MSDS DATA 608 - Vijaya Cherukuri', style={
            'textAlign': 'left',
            'color': colors['text']
        }),
    html.H6('Data source: https://archive.ics.uci.edu/ml/datasets/diabetes+130-us+hospitals+for+years+1999-2008', style={
            'textAlign': 'left',
            'color': colors['text']
        }),
    
    dcc.Tabs(id="tabs", className="row", style={"margin": "2% 3%","height":"20","verticalAlign":"middle"}, value='dem_tab', children=[
        dcc.Tab(label='Demographics', value='dem_tab'),
        dcc.Tab(label='Medical Speciality And Re-Admission', value='med_tab')
        # dcc.Tab(label='Re-admissions', value='readmit_tab')
    ]),
    html.Div(id='tabs-content-example')
])


@app.callback(Output('tabs-content-example', 'children'),
              [Input('tabs', 'value')])

def render_content(tab):
    if tab == 'dem_tab':
        return pat_dem.tab_1_layout
    elif tab == 'med_tab':
        # print("<<<<<<<<<<>>>>>>>>>>>>>")
        # print(tab)
        return pat_med.tab_2_layout
    elif tab == 'readmit_tab':
        return pat_readmit.tab_2_layout


# Tab 1 callback
@app.callback(dash.dependencies.Output('page-1-content', 'children'),
              [dash.dependencies.Input('page-1-dropdown', 'value')])

def page_1_dropdown(value):
    # print("<<<<<<<<<<<>>>>>>>>>>>")
    # print(value)
    # print(val1)
    df_ms_final = df_med_readmit_final[df_med_readmit_final['medical_specialty']==value].copy()
    # return df_ms_final
    graphs = []

    graphs.append(dcc.Graph(id='g_gender', config={"displaylogo": False},
                                  figure={
                                      'data': [
                                          {
                                              'labels': df_ms_final['admit_type'],
                                              'values': df_ms_final['count'],
                                              'type': 'pie',
                                              'hole':.4
                                           }
                                      ],
                                        'layout':
                                            {
                                                'title': 'Patient Hospital Admission',
                                                 # 'legend': {'orientation':"h"},
                                                'annotations': [{
                                                        "font": {
                                                                    "size": 10
                                                                },
                                                        'text':'Admission Type', "showarrow": False}]
                                            }

                                  })
                    )

    return graphs
    # return df_ms_final.to_json(orient='split')
    # return 'You have selected "{}"'.format(value)


# Tab 1 callback
@app.callback(dash.dependencies.Output('page-2-content', 'children'),
              [dash.dependencies.Input('page-1-dropdown2', 'value')]
              )

def page_2_dropdown(val):
    print("<<<<<<<<<<<>>>>>>>>>>>")
    print(val)
    # print(val1)
    df = df_med_readmit_final[df_med_readmit_final['readmitted']==str(val)].copy()
    # return df_ms_final
    gr = []
    x = df['time_in_hospital']
    # x = np.random.randn(100)
    hist_data = [x]
    group_labels = ['Time Spent in the Hospital']
    fig = ff.create_distplot(hist_data, group_labels)
    gr.append(dcc.Graph(id='abc', figure=fig))

    return gr


if __name__ == '__main__':
    app.run_server()
