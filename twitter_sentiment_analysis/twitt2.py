from tweepy import API 
from tweepy import Cursor
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream

from textblob import TextBlob
 
import twitter_credentials

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import re


class TwitterClient():
    def __init__(self, twitter_user=None):
        self.auth = TwitterAuthenticator().authenticate_twitter_app()
        self.twitter_client = API(self.auth)

        self.twitter_user = twitter_user

    def get_twitter_client_api(self):
        return self.twitter_client

    def get_user_timeline_tweets(self, num_tweets):
        tweets = []
        for tweet in Cursor(self.twitter_client.user_timeline, id=self.twitter_user).items(num_tweets):
            tweets.append(tweet)
        return tweets

    def get_friend_list(self, num_friends):
        friend_list = []
        for friend in Cursor(self.twitter_client.friends, id=self.twitter_user).items(num_friends):
            friend_list.append(friend)
        return friend_list

    def get_home_timeline_tweets(self, num_tweets):
        home_timeline_tweets = []
        for tweet in Cursor(self.twitter_client.home_timeline, id=self.twitter_user).items(num_tweets):
            home_timeline_tweets.append(tweet)
        return home_timeline_tweets


class TwitterAuthenticator():
    # Autentica con twitter y busca publicaciones en función de palabras clave
    def authenticate_twitter_app(self):
        # AUTENTICACIÓN CON EL API DE TWITTER
        auth = OAuthHandler(twitter_credentials.API_KEY, twitter_credentials.API_SECRET_KEY)
        auth.set_access_token(twitter_credentials.ACCESS_TOKEN, twitter_credentials.ACCESS_TOKEN_SECRET)
        return auth

class TwitterStreamer():
    # Escucha los cambios en Twitter
    def __init__(self):
        self.twitter_autenticator = TwitterAuthenticator()    

    def stream_tweets(self, fetched_tweets_filename, hash_tag_list):
        listener = TwitterListener(fetched_tweets_filename)
        auth = self.twitter_autenticator.authenticate_twitter_app() 
        stream = Stream(auth, listener)

        # BUSCAR TWITERS POR PALABRAS CLAVE 
        stream.filter(track=hash_tag_list)

class TwitterListener(StreamListener):
    # Escucha los cambios en Twitter y actualiza continuamente la salida
    def __init__(self, fetched_tweets_filename):
        self.fetched_tweets_filename = fetched_tweets_filename

    def on_data(self, data):
        try:
            print(data)
            with open(self.fetched_tweets_filename, 'a') as tf:
                tf.write(data)
            return True
        except BaseException as e:
            print("Error: %s" % str(e))
        return True
          
    def on_error(self, status):
        if status == 420:
            return False
        print(status)


class TweetAnalyzer():
    # Elimina signos de puntuación, y caracteres que pueden interferir en el análisis
    def clean_tweet(self, tweet):
        return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split())

    # Analiza el sentimiento de cada Tweet
    def analyze_sentiment(self, tweet):
        analysis = TextBlob(self.clean_tweet(tweet))
        return [analysis.sentiment.polarity, analysis.sentiment.subjectivity]

    def tweets_to_data_frame(self, tweets):
        # Obtiene la información de cada tweet
        df = pd.DataFrame(data=[tweet.text for tweet in tweets], columns=['tweets'])

        df['id'] = np.array([tweet.id for tweet in tweets])
        df['len'] = np.array([len(tweet.text) for tweet in tweets])
        df['date'] = np.array([tweet.created_at for tweet in tweets])
        df['source'] = np.array([tweet.source for tweet in tweets])
        df['likes'] = np.array([tweet.favorite_count for tweet in tweets])
        df['retweets'] = np.array([tweet.retweet_count for tweet in tweets])

        return df

 
if __name__ == '__main__':

    twitter_client = TwitterClient()
    tweet_analyzer = TweetAnalyzer()

    api = twitter_client.get_twitter_client_api()

    tweets = api.user_timeline(screen_name="UISEK", count=200)

    df = tweet_analyzer.tweets_to_data_frame(tweets)
    df['sentiment_polarity'] = np.array([tweet_analyzer.analyze_sentiment(tweet)[0] for tweet in df['tweets']])
    df['sentiment_subjectivity'] = np.array([tweet_analyzer.analyze_sentiment(tweet)[1] for tweet in df['tweets']])

    print(df.head(10))

    # Graficando el Resultado
    time_tweets_polarity = pd.Series(data=df['sentiment_polarity'].values, index=df['date'])
    time_tweets_polarity.plot(figsize=(16, 4), label="sentiment_polarity", legend=True)
    time_tweets_subjectivity = pd.Series(data=df['sentiment_subjectivity'].values, index=df['date'])
    time_tweets_subjectivity.plot(figsize=(16, 4), label="sentiment_subjectivity", legend=True)
    plt.show()