import os


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    CELERY_BROKER_URL = os.environ.get('CELERY_BROKER_URL') or 'redis://localhost:6379/0'
    CELERY_RESULT_BACKEND = os.environ.get('CELERY_RESULT_BACKEND') or 'redis://localhost:6379/0'
    TWITTER_CONSUMER_KEY = os.environ.get('TWITTER_CONSUMER_KEY')
    TWITTER_CONSUMER_SECRET = os.environ.get('TWITTER_CONSUMER_SECRET')
    TWITTER_ACCESS_TOKEN = os.environ.get('TWITTER_ACCESS_TOKEN')
    TWITTER_ACCESS_TOKEN_SECRET = os.environ.get('TWITTER_ACCESS_TOKEN_SECRET')
    POSITIVE_GPIO = os.environ.get('POSITIVE_GPIO') or 17
    NEGATIVE_GPIO = os.environ.get('NEGATIVE_GPIO') or 27
