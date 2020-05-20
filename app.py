import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.express as px

import dash
import dash_core_components as dcc
import dash_html_components as html

from dash.dependencies import (
    Input,
    Output
)

from geo import geojson_data
from data import (
    latest_data,
    daily_tests,
    daily_positive_rates,
    tests_per_abs,
    total_tests_num,
)

import pytz
import datetime


geo_data = geojson_data()
source_code_url = 'https://github.com/Dani-Mora/covid-tests-visualization'

app = dash.Dash()
server = app.server

timezone = pytz.timezone('Europe/Berlin')
last_update_time = datetime.datetime.now(timezone)
current_df = latest_data()


def _daily_info_plot() -> go.Figure:
    fig = make_subplots(specs=[[{"secondary_y": True}]])

    daily_tests_df = daily_tests(current_df)
    fig.add_trace(go.Scatter(x=daily_tests_df.Date,
                             y=daily_tests_df.Tests,
                             mode='markers',
                             name='Tests'),
                  secondary_y=False)

    daily_rates_df = daily_positive_rates(current_df)
    fig.add_trace(go.Scatter(x=daily_rates_df.Date,
                             y=daily_rates_df['Percentatge positius'],
                             mode='markers',
                             name='Positius (%)'),
                  secondary_y=True)

    fig.update_xaxes(title_text='Data')
    fig.update_yaxes(title_text='Tests',
                     autorange=True,
                     secondary_y=False)
    fig.update_yaxes(title_text='Positius (%)',
                     secondary_y=True,
                     autorange=True,
                     range=[0, 100])

    fig.update_layout(title='Dades diàries',
                      autosize=True,
                      hovermode="x unified",
                      legend_orientation="h")
    return fig


def _map_plot() -> go.Figure:
    df = tests_per_abs(current_df)
    fig = go.Figure(go.Choroplethmapbox(
        geojson=geo_data,
        locations=df.ABSCode,
        text=df.ABSText,
        colorscale='Greens',
        hovertemplate='%{text}<extra>%{z}</extra>',
        marker_opacity=0.70,
        z=df.TotalTests))


    fig.update_layout(mapbox_style='carto-positron',
                      mapbox_center={'lat': 41.70, 'lon': 2.10},
                      mapbox_zoom=6.42,
                      autosize=True)

    return fig


def _last_update_text():
    str_time = last_update_time.strftime('%Y-%m-%d %H:%M:%S')
    return [html.H3(f'Darrera actualització: {str_time}, CEST (UTC+2)')]


def _total_tests_text():
    return [html.H3(f'Total tests realitzats: {total_tests_num(current_df)}')]


# Define page structure
title = html.Div([html.H1('COVID-19 tests realitzats a Catalunya')],
                 style={'textAlign': 'center', 'padding-bottom': '30'})

total_tests = html.Div(id='total-tests-text',
                       children=_total_tests_text(),
                       style={'textAlign': 'center', 'padding-bottom': '10'})


last_update = html.Div(id='last-updated-text',
                       children=_last_update_text(),
                       style={'textAlign': 'center', 'padding-bottom': '10'})


source_code = html.Div(
    [html.H5(html.A(href=source_code_url, children='Codi font'))],
    style={'textAlign': "left", 'padding-left': '5vw'}
)

main_div = html.Div([
    dcc.Graph(
        id='main-graph',
        figure=_map_plot(),
        style={'width': '100vw', 'height': '60vh'}),
    dcc.Graph(
        id='daily-plot-graph',
        figure=_daily_info_plot(),
        style={'width': '100vw', 'height': '40vh'}),
])

app.layout = html.Div([
    title,
    total_tests,
    last_update,
    main_div,
    source_code
])


if __name__ == '__main__':
    app.run_server(debug=True)
