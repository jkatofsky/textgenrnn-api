from settings import MIN_TRAINING_CHARS, MAX_TRAINING_CHARS, MAX_MAX_LENGTH, IS_PROD
import secrets
import os
import shutil


def valid_training_strings(training_strings):
    return training_strings and \
        isinstance(training_strings, list) and \
        (MIN_TRAINING_CHARS < sum(len(training_string) for training_string in training_strings) < MAX_TRAINING_CHARS) and \
        all(isinstance(elem, str) for elem in training_strings)


def valid_model_id(model_id):
    return model_id and \
        isinstance(model_id, str)


def valid_options(options):
    if not options:
        return True
    prompt = options.get('prompt', None)
    max_length = options.get('max_length', None)
    temperature = options.get('temperature', None)

    return (not prompt or isinstance(prompt, str)) and \
        (not max_length or (isinstance(max_length, int) and 0 < max_length <= MAX_MAX_LENGTH)) and \
        (not temperature or (isinstance(temperature, float) and 0 < temperature <= 1))


def get_model_id():
    return secrets.token_urlsafe(nbytes=16)


def get_model_dir(model_id):
    tmp_folder = '/tmp' if IS_PROD else './tmp'
    model_dir = '%s/%s' % (tmp_folder, model_id)
    return model_dir


def using_temp_model_dir(model_id):
    model_dir = get_model_dir(model_id)
    os.mkdir(model_dir)
    os.chdir(model_dir)


def done_with_temp_model_dir(model_id, cd_to):
    model_dir = get_model_dir(model_id)
    os.chdir(cd_to)
    shutil.rmtree(model_dir)
