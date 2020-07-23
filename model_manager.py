from textgenrnn import textgenrnn
from google.cloud import storage
import os

MODEL_BUCKET_NAME = os.getenv('MODEL_BUCKET_NAME')

client = storage.Client()
bucket = client.get_bucket(MODEL_BUCKET_NAME)


def _get_filename(model_id):
    return "%s.hdf5" % model_id


def upload_model(model: textgenrnn, model_id):
    filename = _get_filename(model_id)

    model.save(filename)

    blob = bucket.blob(filename)
    blob.upload_from_filename(filename)


def download_model(model_id):
    filename = _get_filename(model_id)

    blob = bucket.get_blob(filename)
    if not blob:
        return None

    blob.download_to_filename(filename)

    model = textgenrnn(weights_path=filename)

    return model
