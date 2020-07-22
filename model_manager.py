from utils import get_model_filenames
from textgenrnn import textgenrnn
from google.cloud import storage
import secrets
import os

MODEL_BUCKET_NAME = os.getenv('MODEL_BUCKET_NAME')

client = storage.Client()
bucket = client.get_bucket(MODEL_BUCKET_NAME)


def save_model(model: textgenrnn):
    model_id = secrets.token_urlsafe(nbytes=16)
    filename, tmp_filename = get_model_filenames(model_id)

    model.save(weights_path=tmp_filename)
    blob = bucket.blob(filename)
    blob.upload_from_filename(tmp_filename)

    return model_id


def get_model(model_id):
    filename, tmp_filename = get_model_filenames(model_id)

    blob = bucket.get_blob(filename)
    if not blob:
        return None

    blob.download_to_filename(tmp_filename)

    model = textgenrnn(weights_path=tmp_filename)

    return model
