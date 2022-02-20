import dash
from dash import dcc
from dash import html
from dash import dash_table as table
from dash.dependencies import Output, Input, State
import pyautogui
# from update_figure import Update
# import tweepy
# from tweepy import OAuthHandler

#DATAFRAME DEPENDENCIES
import pandas as pd
import numpy as np

#PLOTLY DEPENDENCIES
# import plotly.express as px
# import plotly.graph_objs as go

#OTHER DEPENDENCIES
from datetime import datetime
from cleantweet import preprocess_apply
from sentiment_code import decode_sentiment
from update_figure import Update

# <------------------Dash HTML Layout---------------------->
app = dash.Dash(__name__)
server = app.server

app.layout = html.Div([
    html.Div([
        html.H2("Twitter Sentiment Analyzer"),
        #html.Img(src="/assets/stock-icon.png")
    ], className="banner"),

    html.Div([
        dcc.Input(id="query", value="#MarvelStudios", type="text" ),
        dcc.Input(id="limit", value=100, type="number"),
        html.Button(id="submit-button", n_clicks=0, children="Submit")
    ]),

    html.Div([

         dcc.Graph(
            id="line_graph",
            style={'display': 'contents'},
            className="six columns"
        ),
        dcc.Graph(
            id="pie_sentiment",
            style={'display': 'inline-block'}
        ),
        dcc.Graph(
            id="map",
            style={'display':'inline-block'}
        )
        
        

    ]),

    html.Div([
        dcc.Graph(
            id="tweets_table",className="tablegraph"
        ),
        
        
    ])

])
# <------------------------------------------------------->

# Decorator function to para kapag may nabago sa inputs o kaya clinick yung submit button, mag-uupdate yung graph
# kung ano yung pagkakasunod sunod ng parameters dito sa decorator, yung din yung pagkakasunod sa update_fig()
@app.callback(Output('pie_sentiment', 'figure'),
              Output('line_graph', 'figure'),
              Output('tweets_table', 'figure'),
              Output('map', 'figure'),
              [Input("submit-button", "n_clicks")],
              [State("query", "value")],
              [State("limit", "value")]
            )

# Eto yung function para magbago data ng graphs

def graph(num_clicks, input_value, limit_value):
    figure = Update(num_clicks, input_value, limit_value)

    return figure.update_fig()


if __name__=="__main__":
    app.run_server(debug=True)