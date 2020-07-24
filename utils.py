from settings import (MIN_TRAINING_CHARS, MAX_TRAINING_CHARS, MAX_PROMPT_CHARS,
                      MIN_MAX_LENGTH, MAX_MAX_LENGTH, IS_PROD)
import uuid
import os
import shutil
import gc
import tensorflow as tf


def make_tmp_directory_on_local():
    if not IS_PROD and not os.path.isdir('./tmp'):
        os.mkdir('./tmp')


def clear_memory():
    tf.keras.backend.clear_session()
    gc.collect()


def valid_training_strings(training_strings):
    return training_strings and isinstance(training_strings, list) and \
        all(isinstance(elem, str) for elem in training_strings) and \
        (MIN_TRAINING_CHARS <= sum(len(training_string)
                                   for training_string in training_strings) <= MAX_TRAINING_CHARS)


def valid_model_id(model_id):
    if not model_id or not isinstance(model_id, str):
        return False
    try:
        uuid_obj = uuid.UUID(model_id, version=4)
    except ValueError:
        return False
    return str(uuid_obj) == model_id


def valid_options(options):
    if not options:
        return True
    prompt = options.get('prompt', None)
    max_length = options.get('max_length', None)
    temperature = options.get('temperature', None)

    return (not prompt or (isinstance(prompt, str) and len(prompt) <= MAX_PROMPT_CHARS)) and \
        (not max_length or (isinstance(max_length, int) and MIN_MAX_LENGTH <= max_length <= MAX_MAX_LENGTH)) and \
        (not temperature or (isinstance(temperature, float) and 0 < temperature <= 1))


def get_model_id():
    return uuid.uuid4()


def get_model_filenames(model_id):
    filename = "%s.hdf5" % model_id
    tmp_path = '/tmp' if IS_PROD else './tmp'
    return filename, '%s/%s' % (tmp_path, filename)
