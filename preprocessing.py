#imports
import json
from os import listdir
from os.path import isfile, join
import nest_asyncio

nest_asyncio.apply()
import os, json
import pandas as pd
import numpy as np
import glob
from datetime import datetime as dtt
from datetime import date as dt, timedelta
from datetime import date as dt, timedelta
import plotly.express as px
from dash.dependencies import Input, Output
import plotly.graph_objects as go



def preprocess():
    path = 'Nigeria_mock/'

    json_pattern = os.path.join(path, '*.json')
    file_list = glob.glob(json_pattern)

    df = pd.DataFrame()
    for file in file_list:
        with open(file, 'r') as f:
            data = json.load(f)
        df = df.append(pd.DataFrame.from_dict(pd.json_normalize(data), orient='columns'))

    kenya_path = 'Kenya_mock/'

    json_pattern_kenya = os.path.join(kenya_path, '*.json')
    file_list_kenya = glob.glob(json_pattern_kenya)

    df_kenya = pd.DataFrame()
    for file in file_list_kenya:
        with open(file, 'r') as f:
            data_k = json.load(f)
        df_kenya = df_kenya.append(pd.DataFrame.from_dict(pd.json_normalize(data_k), orient='columns'))

    # remove extra space from date

    df['Patient Service Date.@value'] = df['Patient Service Date.@value'].str.strip()
    df = df.sort_values('Patient Service Date.@value')

    df_kenya['PART 4: TREATMENT AUTHENTIFICATION.Date of Service.@value'] = df_kenya[
        'PART 4: TREATMENT AUTHENTIFICATION.Date of Service.@value'].str.strip()
    df_kenya = df_kenya.sort_values('PART 4: TREATMENT AUTHENTIFICATION.Date of Service.@value')

    return df, df_kenya


# ------create figures-------
def get_figures(dropdown_value):
    df, df_kenya = preprocess()

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


    patient_count = pd.DataFrame(dict_values.items(), columns=['Date', 'Patient Visit'])

    fig = px.bar(patient_count, x="Date", y="Patient Visit", color_discrete_sequence=['#d9b3ff'] * len(patient_count))

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

    return startdate, enddate, fig, fig_diagnosis, fig_outcome_visit, fig_mort_morb, df, df_kenya
