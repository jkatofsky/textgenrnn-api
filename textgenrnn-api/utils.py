import os

MIN_TRAINING_CHARS = int(os.getenv("MIN_TRAINING_CHARS"))
MAX_TRAINING_CHARS = int(os.getenv("MAX_TRAINING_CHARS"))
MAX_MAX_LENGTH = int(os.getenv("MAX_MAX_LENGTH"))


def valid_training_strings(training_strings):
    return training_strings and \
        isinstance(training_strings, list) and \
        (MIN_TRAINING_CHARS < sum(len(training_string) for training_string in training_strings)
         < MAX_TRAINING_CHARS) and \
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
        (not max_length or (isinstance(max_length, int) and 0 < max_length <= 300)) and \
        (not temperature or (isinstance(temperature, float) and 0 < temperature <= 1))
