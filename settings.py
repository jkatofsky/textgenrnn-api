import os

IS_PROD = True if os.getenv("IS_PROD") else False

PROJECT_NAME = 'textgenrnn-api'
MODEL_BUCKET_NAME = 'textgenrnn-api-models'
CREDENTIALS_JSON_PATH = 'credentials.json'

MIN_TRAINING_CHARS = 1000
MAX_TRAINING_CHARS = 30000
TRAINING_EPOCHS = 3
MAX_MAX_LENGTH = 300
