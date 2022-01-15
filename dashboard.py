# -------imports----------------------------------------------
import dash
from dash import dcc
from dash import html
from datetime import date as dt, timedelta
import plotly.express as px
from dash.dependencies import Input, Output
import plotly.graph_objects as go

# from additional file import function
from preprocessing import get_figures

import nest_asyncio

nest_asyncio.apply()
import pandas as pd
from datetime import datetime as dtt

# -------settings for the dashboard---------------------------

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.title = "VODAN Dashboard"

# -------get intial figures-----------------------------------
startdate, enddate, fig, fig_diagnosis, fig_outcome_visit, fig_mort_morb, df, df_kenya = get_figures('Last 6 months')

# -------start app--------------------------------------------
app.layout = html.Div(children=[
    # All elements from the top of the page
    # First header, className defines  how many of the 12 columns it will use, so
    # you can place one thing using row or two nect to each other using six columns etc.
    html.Div([
        html.Div(className="app-header", children=[
            html.Div('Vodan Dashboard', className="app-header--title")
        ], style={'textAlign': 'center'}),

        html.Div(className="subheader", children='''
            Hospital Metrics
        ''', style={'textAlign': 'center'}),
    ], className='row', style={'textAlign': 'center',
                               'marginTop': 40, 'marginBottom': 40}),

    html.Div([
        html.H1(children='PATIENTS VISITED'),
        html.Div(children=''),
        dcc.Dropdown(
            id='timeframe_dropdown1',
            multi=False,
            options=[
                {'label': 'Today', 'value': 'Today'},
                {'label': 'Yesterday', 'value': 'Yesterday'},
                {'label': 'Last 25 days', 'value': 'Last 25 days'},
                {'label': 'Last 6 months', 'value': 'Last 6 months'},
                {'label': 'Last 1 year', 'value': 'Last 1 year'}
            ],
            value='Last 6 months',
            clearable=False,
        ),
        dcc.DatePickerRange(
            id='datepicker1',
            display_format='DD-MM-YYYY',
            first_day_of_week=1,
            min_date_allowed=dt(2021, 11, 1),
            max_date_allowed=dt(2021, 12, 28),
        ),

        dcc.Graph(id='patient_visit', figure=fig),
    ], className='row'),

    html.Div([
        html.H1(children='DIAGNOSIS'),
        html.Div(children='Disease Diagnosed'),
        dcc.Dropdown(
            id='timeframe_dropdown2',
            multi=False,
            options=[
                {'label': 'Today', 'value': 'Today'},
                {'label': 'Yesterday', 'value': 'Yesterday'},
                {'label': 'Last 25 days', 'value': 'Last 25 days'},
                {'label': 'Last 6 months', 'value': 'Last 6 months'},
                {'label': 'Last 1 year', 'value': 'Last 1 year'}
            ],
            value='Last 6 months',
            clearable=False,
        ),
        dcc.DatePickerRange(
            id='datepicker2',
            display_format='DD-MM-YYYY',
            first_day_of_week=1,
            min_date_allowed=dt(2021, 11, 1),
            max_date_allowed=dt(2021, 12, 28),
        ),

        dcc.Graph(id='diseases', figure=fig_diagnosis),
    ], className='row'),

    html.Div([
        html.H1(children='OUTCOME'),
        html.Div(children='Outcome of Hospital Visit'),
        dcc.Dropdown(
            id='timeframe_dropdown3',
            multi=False,
            options=[
                {'label': 'Today', 'value': 'Today'},
                {'label': 'Yesterday', 'value': 'Yesterday'},
                {'label': 'Last 25 days', 'value': 'Last 25 days'},
                {'label': 'Last 6 months', 'value': 'Last 6 months'},
                {'label': 'Last 1 year', 'value': 'Last 1 year'}
            ],
            value='Last 6 months',
            clearable=False,
        ),
        dcc.DatePickerRange(
            id='datepicker3',
            display_format='DD-MM-YYYY',
            first_day_of_week=1,
            min_date_allowed=dt(2021, 11, 1),
            max_date_allowed=dt(2021, 12, 28),
        ),

        dcc.Graph(id='outcome_hospital_visit', figure=fig_outcome_visit)
    ], className='row'),

    html.Div([
        html.H1(children='MORTALITY and MORBIDITY'),
        html.Div(children='Number of mortalities and morbidities'),
        dcc.Dropdown(
            id='timeframe_dropdown4',
            multi=False,
            options=[
                {'label': 'Today', 'value': 'Today'},
                {'label': 'Yesterday', 'value': 'Yesterday'},
                {'label': 'Last 25 days', 'value': 'Last 25 days'},
                {'label': 'Last 6 months', 'value': 'Last 6 months'},
                {'label': 'Last 1 year', 'value': 'Last 1 year'}
            ],
            value='Last 6 months',
            clearable=False,
        ),
        dcc.DatePickerRange(
            id='datepicker4',
            display_format='DD-MM-YYYY',
            first_day_of_week=1,
            min_date_allowed=dt(2021, 11, 1),
            max_date_allowed=dt(2021, 12, 28),
        ),

        dcc.Graph(id='morbidity_mortality', figure=fig_mort_morb)
    ], className='row'),

])


# ----After the layout follow the callbacks--------
# make sure to return fig
@app.callback(
    [Output('datepicker1', 'start_date'),  # This updates the field start_date in the DatePicker
     Output('datepicker1', 'end_date'),  # This updates the field end_date in the DatePicker
     Output(component_id='patient_visit', component_property='figure')],
    [Input('timeframe_dropdown1', 'value')], )
def updateDataPicker(dropdown_value):
    if dropdown_value == 'Today':
        startdate = dt.today()
        enddate = dt.today()
    elif dropdown_value == 'Yesterday':
        startdate = dt.today() - timedelta(1)
        enddate = dt.today() - timedelta(1)
    elif dropdown_value == 'Last 25 days':
        startdate = dt.today() - timedelta(24)
        enddate = dt.today()
    elif dropdown_value == 'Last 6 months':
        startdate = dt.today() - timedelta(184)
        enddate = dt.today()
    elif dropdown_value == 'Last 1 year':
        startdate = dt.today() - timedelta(365)
        enddate = dt.today()
    else:
        startdate = dt.today() - timedelta(6)
        enddate = timedelta(6), dt.today()


    dff = df.copy()
    dff['Patient Service Date.@value'] = dff['Patient Service Date.@value'].apply(lambda x:
                                                                                  dtt.strptime(x, "%Y-%m-%d").date())

    dff = dff[(dff['Patient Service Date.@value'] >= startdate) & (dff['Patient Service Date.@value'] <= enddate)]

    dff = dff.sort_values('Patient Service Date.@value')

    dict_values = {}
    for ind, row in dff.iterrows():
        if row['Patient Service Date.@value'] in dict_values.keys():
            dict_values[row['Patient Service Date.@value']] += 1
        else:
            dict_values[row['Patient Service Date.@value']] = 1

    dff_kenya = df_kenya.copy()
    dff_kenya['PART 4: TREATMENT AUTHENTIFICATION.Date of Service.@value'] = dff_kenya[
        'PART 4: TREATMENT AUTHENTIFICATION.Date of Service.@value'].apply(lambda x:
                                                                           dtt.strptime(x, "%Y-%m-%d").date())
    dff_kenya = dff_kenya[(dff_kenya['PART 4: TREATMENT AUTHENTIFICATION.Date of Service.@value'] >= startdate) & (
                dff_kenya['PART 4: TREATMENT AUTHENTIFICATION.Date of Service.@value'] <= enddate)]
    dff_kenya = dff_kenya.sort_values('PART 4: TREATMENT AUTHENTIFICATION.Date of Service.@value')

    for ind, row in dff_kenya.iterrows():
        if row['PART 4: TREATMENT AUTHENTIFICATION.Date of Service.@value'] in dict_values.keys():
            dict_values[row['PART 4: TREATMENT AUTHENTIFICATION.Date of Service.@value']] += 1
        else:
            dict_values[row['PART 4: TREATMENT AUTHENTIFICATION.Date of Service.@value']] = 1


    patient_count = pd.DataFrame(dict_values.items(), columns=['Date', 'Patient Visit'])

    fig = px.bar(patient_count, x="Date", y="Patient Visit", color_discrete_sequence=['#d9b3ff'] * len(patient_count))

    return startdate, enddate, fig


@app.callback(
    [Output('datepicker2', 'start_date'),  # This updates the field start_date in the DatePicker
     Output('datepicker2', 'end_date'),  # This updates the field end_date in the DatePicker
     Output(component_id='diseases', component_property='figure')],
    [Input('timeframe_dropdown2', 'value')],
)
def updateDataPicker(dropdown_value):
    if dropdown_value == 'Today':
        startdate = dt.today()
        enddate = dt.today()
    elif dropdown_value == 'Yesterday':
        startdate = dt.today() - timedelta(1)
        enddate = dt.today() - timedelta(1)
    elif dropdown_value == 'Last 25 days':
        startdate = dt.today() - timedelta(24)
        enddate = dt.today()
    elif dropdown_value == 'Last 6 months':
        startdate = dt.today() - timedelta(184)
        enddate = dt.today()
    elif dropdown_value == 'Last 1 year':
        startdate = dt.today() - timedelta(365)
        enddate = dt.today()
    else:
        startdate = dt.today() - timedelta(6)
        enddate = timedelta(6), dt.today()

    dff = df.copy()
    dff['Patient Service Date.@value'] = dff['Patient Service Date.@value'].apply(lambda x:
                                                                                  dtt.strptime(x, "%Y-%m-%d").date())

    dff = dff[(dff['Patient Service Date.@value'] >= startdate) & (dff['Patient Service Date.@value'] <= enddate)]

    dff = dff.sort_values('Patient Service Date.@value')

    # for different diseases

    dict_values = {}
    for ind, row in dff.iterrows():
        if row['Diagnosis.@value'] in dict_values.keys():
            dict_values[row['Diagnosis.@value']] += 1
        else:
            dict_values[row['Diagnosis.@value']] = 1


    diagnosis_count = pd.DataFrame(dict_values.items(), columns=['Diagnosis', 'Count'])

    fig_diagnosis = px.bar(diagnosis_count, x="Diagnosis", y="Count",
                           color_discrete_sequence=['#b3daff'] * len(diagnosis_count))

    return startdate, enddate, fig_diagnosis


@app.callback(
    [Output('datepicker3', 'start_date'),  # This updates the field start_date in the DatePicker
     Output('datepicker3', 'end_date'),  # This updates the field end_date in the DatePicker
     Output(component_id='outcome_hospital_visit', component_property='figure'),
     Output(component_id='outcome_hospital_visi', component_property='figure')],
    [Input('timeframe_dropdown3', 'value')],
)
def updateDataPicker(dropdown_value):
    if dropdown_value == 'Today':
        startdate = dt.today()
        enddate = dt.today()
    elif dropdown_value == 'Yesterday':
        startdate = dt.today() - timedelta(1)
        enddate = dt.today() - timedelta(1)
    elif dropdown_value == 'Last 25 days':
        startdate = dt.today() - timedelta(24)
        enddate = dt.today()
    elif dropdown_value == 'Last 6 months':
        startdate = dt.today() - timedelta(184)
        enddate = dt.today()
    elif dropdown_value == 'Last 1 year':
        startdate = dt.today() - timedelta(365)
        enddate = dt.today()
    else:
        startdate = dt.today() - timedelta(6)
        enddate = timedelta(6), dt.today()

    dff = df.copy()
    dff['Patient Service Date.@value'] = dff['Patient Service Date.@value'].apply(lambda x:
                                                                                  dtt.strptime(x, "%Y-%m-%d").date())

    dff = dff[(dff['Patient Service Date.@value'] >= startdate) & (dff['Patient Service Date.@value'] <= enddate)]

    dff = dff.sort_values('Patient Service Date.@value')

    # Outcome of Hospital visit

    dict_values = {}
    for ind, row in dff.iterrows():
        if row['Outcome of Hospital Visits.Outcome of Hospital Visits'][0]['@value'] in dict_values.keys():
            dict_values[row['Outcome of Hospital Visits.Outcome of Hospital Visits'][0]['@value']] += 1
        else:
            dict_values[row['Outcome of Hospital Visits.Outcome of Hospital Visits'][0]['@value']] = 1

    diagnosis_outcome = pd.DataFrame(dict_values.items(), columns=['Outcome of Hospital visit', 'Count'])

    fig_outcome_visit = px.bar(diagnosis_outcome, x="Outcome of Hospital visit", y="Count",
                               color_discrete_sequence=['#ffd9b3'] * len(diagnosis_outcome))

    return startdate, enddate, fig_outcome_visit


@app.callback(
    [Output('datepicker4', 'start_date'),  # This updates the field start_date in the DatePicker
     Output('datepicker4', 'end_date'),  # This updates the field end_date in the DatePicker
     Output(component_id='morbidity_mortality', component_property='figure')],
    [Input('timeframe_dropdown4', 'value')],
)
def updateDataPicker(dropdown_value):
    if dropdown_value == 'Today':
        startdate = dt.today()
        enddate = dt.today()
    elif dropdown_value == 'Yesterday':
        startdate = dt.today() - timedelta(1)
        enddate = dt.today() - timedelta(1)
    elif dropdown_value == 'Last 25 days':
        startdate = dt.today() - timedelta(24)
        enddate = dt.today()
    elif dropdown_value == 'Last 6 months':
        startdate = dt.today() - timedelta(184)
        enddate = dt.today()
    elif dropdown_value == 'Last 1 year':
        startdate = dt.today() - timedelta(365)
        enddate = dt.today()
    else:
        startdate = dt.today() - timedelta(6)
        enddate = timedelta(6), dt.today()

    dff = df.copy()
    dff['Patient Service Date.@value'] = dff['Patient Service Date.@value'].apply(lambda x:
                                                                                  dtt.strptime(x, "%Y-%m-%d").date())

    dff = dff[(dff['Patient Service Date.@value'] >= startdate) & (dff['Patient Service Date.@value'] <= enddate)]

    dff = dff.sort_values('Patient Service Date.@value')

    mortalities_length = 0
    morbidities_length = 0

    for ind, row in dff.iterrows():
        if row['Outcome of Hospital Visits.Outcome of Hospital Visits'][0]['@value'] == 'D(Dead)':
            mortalities_length += 1
        else:
            morbidities_length += 1

    labels = ['MORTALITIES', 'MORBIDITIES']
    values = [mortalities_length, morbidities_length]

    fig_mort_morb = go.Figure(data=[go.Pie(labels=labels, values=values)])

    return startdate, enddate, fig_mort_morb


if __name__ == '__main__':
    app.run_server()
