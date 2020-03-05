from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
 
import twitter_credentials
 
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
        print(status)

 
if __name__ == '__main__':
    hash_tag_list = ["covid-19", "coronavirus", "pandemia"]
    fetched_tweets_filename = "tweets.json"

    twitter_streamer = TwitterStreamer()
    twitter_streamer.stream_tweets(fetched_tweets_filename, hash_tag_list)