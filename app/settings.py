import os
from dotenv import load_dotenv
load_dotenv()

# where is running?
HOST = os.getenv('HOST')
PORT = os.getenv('PORT')

BASE_PATH = '/grafana/api/v1'
SOURCE = 'es'

# elastic search connection parameters
ES_HOST = os.getenv('ES_HOST')
ES_PORT = os.getenv('ES_PORT')
ES_INDEX = os.getenv('ES_INDEX')
ES_USERNAME = os.getenv('ES_USERNAME')
ES_SECRET = os.getenv('ES_SECRET')

BUCKETS = 1000
