from utils import get_model_id, get_model_filenames
from settings import MODEL_BUCKET_NAME, CREDENTIALS_JSON_PATH, PROJECT_NAME

from textgenrnn import textgenrnn
from google.cloud import storage
from google.oauth2 import service_account
import json
import os.path


with open(CREDENTIALS_JSON_PATH) as credentials_fp:
    credentials_info = json.load(credentials_fp)

credentials = service_account.Credentials.from_service_account_info(
    credentials_info)

client = storage.Client(project=PROJECT_NAME, credentials=credentials)
bucket = client.get_bucket(MODEL_BUCKET_NAME)


def upload_model(model: textgenrnn):
    model_id = get_model_id()
    filename, tmp_path = get_model_filenames(model_id)

    model.save(tmp_path)

    blob = bucket.blob(filename)
    blob.upload_from_filename(tmp_path)

    return model_id


def download_model(model_id):
    filename, tmp_path = get_model_filenames(model_id)

    if not os.path.isfile(tmp_path):
        blob = bucket.get_blob(filename)
        if not blob:
            return None
        blob.download_to_filename(tmp_path)

    model = textgenrnn(weights_path=tmp_path)

    return model
