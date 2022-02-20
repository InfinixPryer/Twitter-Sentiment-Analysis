# TWEEPY DEPENDENCIES
import tweepy
from tweepy import OAuthHandler

#DATAFRAME DEPENDENCIES
import pandas as pd
import numpy as np

#PLOTLY DEPENDENCIES
import plotly.express as px
import plotly.graph_objs as go
from dash import dash_table as table

#OTHER DEPENDENCIES
from datetime import datetime
from cleantweet import preprocess_apply
from sentiment_code import decode_sentiment
from model import predict_text

import json

geojsonFile = open('./assets/custom.geo.json')
geojsonMap = json.load(geojsonFile)

#<--------------------------------------------------------------------->
# TWITTER AUTHENTICATION
# Needed credentials para sa twitter API

ckey="KZUckeV18Q7so4LRJgx8LniP6"
csecret="dz5pBTA4ye9saekvgSDoRV7QO7aZs66Wq0Hn1Fwk1eXLOmJbLT"
atoken="819588776414449664-5jMJO24QHJ2igTB5J91RmYZEtyTOSkl"
asecret="twuEQKQ4o5bJwrcOWEa5tpCkb27P8xV369n3h7gXhTOKa"

auth = OAuthHandler(ckey, csecret)
auth.set_access_token(atoken, asecret)
api = tweepy.API(auth)


#<--------------------------------------------------------------------->

class Update:

    def __init__(self, n_clicks, input_value, limit_value):
        self.n_clicks = n_clicks
        self.input_value = input_value
        self.limit_value = limit_value

    def update_fig(self):
        # results = api.search_30_day(label='30DayTweetSearchTest', query=input_value) # ------> kapag merong premium subscription masmadaming requests tsaka tweets na makukuha
    
        results = api.search_tweets(q=self.input_value, count=self.limit_value, lang="en")

        # From the results gagawin niyang json format
        json_data = [r._json for r in results]
        
        # From json format to datframe
        df = pd.json_normalize(json_data)
        df = df[['created_at', 'id_str', 'text', 'user.name', 'user.screen_name', 'user.location']]

        # Changing the time format
        df['created_at'] = df['created_at'].apply(lambda date: datetime.strftime(datetime.strptime(date,'%a %b %d %H:%M:%S +0000 %Y'), '%Y-%m-%d %H:%M:%S'))

        #Cleaning the text then applying the result to the clean_text column
        df['clean_text'] = df['text'].apply(lambda tweet: preprocess_apply(tweet))
        
        # Dito na papasok yung model para makapredict pero di ko pa alam kung pano
        df['sentiment_value'] = df['clean_text'].apply(lambda text: predict_text(text))

        #Kapag meron ng values se sentiment_value dito naman idedecode kung POSITIVE, NEUTRAL or NEGATIVE
        df['sentiment_label'] = df['sentiment_value'].apply(lambda value: decode_sentiment(value))

        print(df.head()) #For testing purposes

        # Pie Graph
        c = df['sentiment_label'].value_counts()
        pie_fig = px.pie(df, values= c , names= c.index, hole=0.65)

        # Line Graph
        line_fig = px.line(x=df['created_at'], y=df['sentiment_value'], labels={'x': "Date", 'y': "Sentiment"})
        
        map_fig = px.choropleth(df,geojson=geojsonMap,locations='user.location', featureidkey='properties.name', color=df['sentiment_label'])
        
        table_fig = go.Figure(data=[go.Table(
                        header=dict(values=list(df.columns),
                                    fill_color='paleturquoise',
                                    align='left'),
                        cells=dict(values=[df["created_at"], df["id_str"], df["text"], df["user.name"], df["user.screen_name"], df["user.location"], df["clean_text"],df["sentiment_value"],df["sentiment_label"]],
                                fill_color='lavender',
                                align='left'))
])  
        # Returns the Pie graph and Line graph to display
        return [pie_fig, line_fig, table_fig, map_fig]