import plotly.graph_objects as go # or plotly.express as px

import dash
import dash_core_components as dcc
import dash_html_components as html

from geo import geojson_data
from data import latest_data

import datetime

current_time = datetime.datetime.now()

geo_data = geojson_data()
test_df = latest_data()

fig = go.Figure(go.Choroplethmapbox(geojson=geo_data,
                                    locations=test_df.ABSCodi,
                                    text=test_df.ABSDescripcio,
                                    hovertemplate='%{text}<extra>%{z}</extra>',
                                    z=test_df.TotalTests))

fig.update_layout(mapbox_style="carto-positron",
                  mapbox_center={"lat": 41.75, "lon": 2.10},
                  mapbox_zoom=7.25,
                  autosize=True)

# Page title
title = html.Div([html.H1('COVID-19 tests realitzats a Catalunya')],
                 style={'textAlign': "center", "padding-bottom": "30"})

# Last update
date_str = current_time.strftime("%Y-%m-%d %H:%M:%S")
last_update = html.Div([html.H2(f'Ultima actualització: {date_str}')],
                       style={'textAlign': "center", "padding-bottom": "30"})

app = dash.Dash()

server = app.server

app.layout = html.Div([
    title,
    last_update,
    dcc.Graph(figure=fig, style={"width": "90vw", "height": "95vh"})
])


if __name__ == '__main__':
    app.run_server(debug=True)

