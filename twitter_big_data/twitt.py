#LIBRERIAS NECESARIAS
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
 
import twitter_credentials
 
import json
from textblob import TextBlob
import re

class TwitterStreamer():
    # Autentica con twitter y busca publicaciones en función de palabras clave
    def __init__(self):
        pass

    def stream_tweets(self, fetched_tweets_filename, hash_tag_list):
        # AUTENTICACIÓN CON EL API DE TWITTER
        listener = StdOutListener(fetched_tweets_filename)
        auth = OAuthHandler(twitter_credentials.API_KEY, twitter_credentials.API_SECRET_KEY)
        auth.set_access_token(twitter_credentials.ACCESS_TOKEN, twitter_credentials.ACCESS_TOKEN_SECRET)
        stream = Stream(auth, listener)

        # BUSCAR TWITERS POR PALABRAS CLAVE 
        stream.filter(track=hash_tag_list)

class StdOutListener(StreamListener):

    # Escucha los cambios en Twitter y actualiza continuamente la salida
    def __init__(self, fetched_tweets_filename):
        self.fetched_tweets_filename = fetched_tweets_filename
        self.output = {"tweets": [], "sentiment_polarity": [], "sentiment_subjectivity": [], "index": []}
        self.count = 0
        
    def clean_tweet(self, tweet):
        return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split())

    def analyze_sentiment(self, tweet):
        analysis = TextBlob(self.clean_tweet(tweet))
        return analysis.sentiment

    def on_data(self, data):
        try:
            tweet = json.loads(data)
            self.count = self.count + 1
            sentiment = self.analyze_sentiment(tweet['text'])
            self.output['sentiment_polarity'].append(sentiment.polarity)
            self.output['sentiment_subjectivity'].append(sentiment.subjectivity)
            self.output['index'].append(self.count)
            self.output['tweets'].append(tweet['text'])
            print(self.count)
            if self.count % 100 == 0:
                with open(self.fetched_tweets_filename, 'w') as tf:
                    tf.write(json.dumps(self.output))
                    self.output = {"tweets": [], "sentiment_polarity": [], "sentiment_subjectivity": [], "index": []}
            return True
        except BaseException as e:
            return True

    def on_error(self, status):
        print(status)
 
if __name__ == '__main__':
    hash_tag_list = ["covid-19", "coronavirus", "pandemia"]
    fetched_tweets_filename = "output\\tweets.json"
    twitter_streamer = TwitterStreamer()
    twitter_streamer.stream_tweets(fetched_tweets_filename, hash_tag_list)