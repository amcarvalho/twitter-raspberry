import boto3
import json
import raspberry
from app import app, celery
from tweepy import OAuthHandler
from tweepy import Stream
from tweepy.streaming import StreamListener

comprehend = boto3.client(service_name='comprehend', region_name='eu-west-2')


class Listener(StreamListener):
    def __init__(self, max_tweets=20):
        super(Listener, self).__init__()
        self.max_tweets = max_tweets
        self.num_tweets = 0

    @staticmethod
    def get_tweet_text(data):
        payload = json.loads(data)
        text = None
        found_text = True
        language_code = "en"
        try:
            text = payload.get("full_text", payload.get("text"))
            if text is None:
                found_text = False
        except KeyError:
            found_text = False

        if found_text:
            if payload.get("lang") in ["hi", "de", "zh-TW", "ko", "pt", "en", "it", "fr", "zh", "es", "ar", "ja"]:
                language_code = payload.get("lang")

        return found_text, text, language_code

    def on_data(self, data):
        found_text, text, language_code = self.get_tweet_text(data)
        if found_text:
            if 'RT @' not in text:
                response = comprehend.detect_sentiment(Text=text, LanguageCode=language_code)
                if response['Sentiment'] == 'NEGATIVE':
                    raspberry.blink_once(app.config['NEGATIVE_GPIO'])
                    self.num_tweets += 1
                elif response['Sentiment'] == 'POSITIVE':
                    raspberry.blink_once(app.config['POSITIVE_GPIO'])
                    self.num_tweets += 1
        else:
            return True

        if self.num_tweets < self.max_tweets:
            return True
        else:
            return False


@celery.task
def twitter_search(data):
    with app.app_context():
        listener = Listener()
        auth = OAuthHandler(app.config['TWITTER_CONSUMER_KEY'], app.config['TWITTER_CONSUMER_SECRET'])
        auth.set_access_token(app.config['TWITTER_ACCESS_TOKEN'], app.config['TWITTER_ACCESS_TOKEN_SECRET'])
        stream = Stream(auth, listener, tweet_mode="extended")
        stream.filter(track=[data])
