import plotly.graph_objects as go

import dash
import dash_core_components as dcc
import dash_html_components as html

from dash.dependencies import (
    Input,
    Output
)

from geo import geojson_data
from data import latest_data

import pytz
import datetime


app = dash.Dash()
server = app.server

geo_data = geojson_data()

timezone = pytz.timezone('Europe/Berlin')


def _map_plot(df) -> go.Figure:
    fig = go.Figure(go.Choroplethmapbox(geojson=geo_data,
                                        locations=df.ABSCodi,
                                        text=df.ABSDescripcio,
                                        colorscale='Greens',
                                        hovertemplate='%{text}<extra>%{z}</extra>',
                                        z=df.TotalTests))


    fig.update_layout(mapbox_style="carto-positron",
                      mapbox_center={"lat": 41.75, "lon": 2.10},
                      mapbox_zoom=7.25,
                      autosize=True)

    return fig


def _last_update_text():
    cat_time = timezone.localize(datetime.datetime.now())
    cat_str_time = cat_time.strftime("%Y-%m-%d %H:%M:%S")
    return [html.H3(f'Darrera actualització: {cat_str_time}, CEST (UTC+2)')]



# Page title
title = html.Div([html.H1('COVID-19 tests realitzats a Catalunya')],
                 style={'textAlign': "center", "padding-bottom": "30"})

# Last update
last_update = html.Div(id='last-updated-text',
                       children=_last_update_text(),
                       style={'textAlign': "center", "padding-bottom": "10"})

timer = dcc.Interval(
    id='interval-component',
    interval=2*60*60*1000, # Update every 2 hours (ms)
    n_intervals=0
)


app.layout = html.Div([
    title,
    last_update,
    dcc.Graph(id='main-graph',
              figure=_map_plot(latest_data()),
              style={"width": "90vw", "height": "95vh"}),
    timer
])


@app.callback(Output(component_id='main-graph', component_property='figure'),
              [Input(component_id='interval-component',
                     component_property='n_intervals')])
def update_main_figure(n):
    df = latest_data()
    return _map_plot(df)


@app.callback(Output(component_id='last-updated-text',
                     component_property='children'),
              [Input(component_id='interval-component',
                     component_property='n_intervals')])
def update_main_figure(n):
    return _last_update_text()


if __name__ == '__main__':
    app.run_server(debug=True)
