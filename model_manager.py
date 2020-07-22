import secrets
from textgenrnn import textgenrnn
from google.cloud import storage

client = storage.Client()
bucket = client.get_bucket('textgenrnn-api-models')


def _get_filenames(model_id):
    cloud_filename = "%s-weights.hdf5" % model_id
    temp_filename = "tmp/%s" % cloud_filename
    return cloud_filename, temp_filename


def save_model(model):
    model_id = secrets.token_urlsafe(nbytes=16)
    cloud_filename, temp_filename = _get_filenames(model_id)

    model.save(weights_path=temp_filename)
    blob = bucket.blob(cloud_filename)
    blob.upload_from_filename(temp_filename)

    return model_id


def get_model(model_id):

    cloud_filename, temp_filename = _get_filenames(model_id)

    blob = bucket.get_blob(cloud_filename)
    if not blob:
        return None

    blob.download_to_filename(temp_filename)

    model = textgenrnn(temp_filename)

    return model
