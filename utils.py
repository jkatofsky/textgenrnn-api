from settings import (MIN_TRAINING_CHARS, MAX_TRAINING_CHARS, MAX_PROMPT_CHARS,
                      MIN_MAX_LENGTH, MAX_MAX_LENGTH, MIN_TEMPERATURE, MAX_TEMPERATURE, IS_PROD)
import uuid
import os
import shutil
import gc
import tensorflow as tf
from cerberus import Validator


def make_tmp_directory_on_local():
    if not IS_PROD and not os.path.isdir('./tmp'):
        os.mkdir('./tmp')


def is_valid_num_chars(field, value, error):
    total_chars = sum(len(training_string)
                      for training_string in value)
    if total_chars < MIN_TRAINING_CHARS:
        error(field, "Too few total characters")
    elif total_chars > MAX_TRAINING_CHARS:
        error(field, "Too many total characters")


TRAIN_SCHEMA = {"training_strings": {"type": "list",
                                     "required": True,
                                     "schema": {"type": "string"},
                                     "check_with": is_valid_num_chars
                                     }
                }

TRAIN_VALIDATOR = Validator(TRAIN_SCHEMA)


def is_valid_model_id(field, value, error):
    message = "Not a properly formed V4 UUID"
    try:
        uuid_obj = uuid.UUID(value, version=4)
    except ValueError:
        error(field, message)
        return
    if not str(uuid_obj) == value:
        error(field, message)


GENERATE_SCHEMA = {"model_id": {"type": "string",
                                "required": True,
                                "check_with": is_valid_model_id},
                   "prompt": {"type": "string",
                              "maxlength": MAX_PROMPT_CHARS},
                   "max_length": {"type": "integer",
                                  "min": MIN_MAX_LENGTH,
                                  "max": MAX_MAX_LENGTH},
                   "temperature": {"type": "float",
                                   "min": MIN_TEMPERATURE,
                                   "max": MAX_TEMPERATURE}
                   }


GENERATE_VALIDATOR = Validator(GENERATE_SCHEMA)


def clear_memory():
    gc.collect()
    tf.keras.backend.clear_session()
    tf.compat.v1.reset_default_graph()


def get_model_id():
    return uuid.uuid4()


def get_model_filenames(model_id):
    filename = "%s.hdf5" % model_id
    tmp_path = '/tmp' if IS_PROD else './tmp'
    return filename, '%s/%s' % (tmp_path, filename)
