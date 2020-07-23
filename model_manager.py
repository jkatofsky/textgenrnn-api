from utils import get_model_id, get_model_filenames

from textgenrnn import textgenrnn
from google.cloud import storage
import os.path

MODEL_BUCKET_NAME = os.getenv('MODEL_BUCKET_NAME')

client = storage.Client()
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
