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
    
class TwitterAuthenticator():
    # Autentica con twitter y busca publicaciones en función de palabras clave
    def authenticate_twitter_app(self):
        # AUTENTICACIÓN CON EL API DE TWITTER
        auth = OAuthHandler(twitter_credentials.API_KEY, twitter_credentials.API_SECRET_KEY)
        auth.set_access_token(twitter_credentials.ACCESS_TOKEN, twitter_credentials.ACCESS_TOKEN_SECRET)
        return auth

class TwitterSearcher():
    def __init__(self):
        self.twitter_client = TwitterClient()
    
    def search(self, hash_tag, numTweets):
        # Busca los tweets que coincidan con los criterios de búsqueda
        api = self.twitter_client.get_twitter_client_api()
        tweets = Cursor(api.search, q=hash_tag, lang="en", since="2020-01-01").items(numTweets)
        return tweets 
    
class TweetAnalyzer():
    def clean_tweet(self, tweet):
        return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split())

    def tweets_to_data_frame(self, tweets):
        # Obtiene la información de cada tweet
        df = pd.DataFrame(data=[tweet.text for tweet in tweets], columns=['tweets'])
        return df

    def analyze_sentiment(self, tweet):
        analysis = TextBlob(self.clean_tweet(tweet))
        return analysis.sentiment

if __name__ == '__main__':
    tweet_analyzer = TweetAnalyzer()
    tweet_searcher = TwitterSearcher()
    numtweets = 10
    tweets = tweet_searcher.search('coronavirus', numtweets)
    df = tweet_analyzer.tweets_to_data_frame(tweets)
    output = {"tweets": np.array([]), "sentiment_polarity": np.array([]), "sentiment_subjectivity": np.array([]), "index": np.array([])}
    count = 0
    for tweet in df['tweets']:
        count = count + 1
        blob = TextBlob(tweet)
        sentiment = tweet_analyzer.analyze_sentiment(tweet)
        output['sentiment_polarity'] = np.append(output['sentiment_polarity'], [sentiment.polarity])
        output['sentiment_subjectivity'] = np.append(output['sentiment_subjectivity'], [sentiment.subjectivity])
        output['index'] = np.append(output['index'], [count])
        output['tweets'] = np.append(output['tweets'], blob)
        print(blob)

    # Graficando el Resultado
    time_tweets_polarity = pd.Series(data=output['sentiment_polarity'], index=output['index'])
    time_tweets_polarity.plot(figsize=(16, 4), label="sentiment_polarity", legend=True)
    time_tweets_subjectivity = pd.Series(data=output['sentiment_subjectivity'], index=output['index'])
    time_tweets_subjectivity.plot(figsize=(16, 4), label="sentiment_subjectivity", legend=True)
    plt.show()