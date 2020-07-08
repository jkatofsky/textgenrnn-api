def valid_training_strings(training_strings):
    return training_strings and \
        isinstance(training_strings, list) and \
        0 < len(training_strings) < 10000 and \
        all(isinstance(elem, str) for elem in training_strings)

def valid_model_id(model_id):
    return model_id and \
        isinstance(model_id, str) and \
        len(model_id) == 12

def valid_options(options):
    if not options:
        return True
    prompt = options.get('prompt', None)
    max_length = options.get('max_length', None)
    temperature = options.get('temperature', None)

    return (not prompt or isinstance(prompt, str)) and \
        (not max_length or (isinstance(max_length, int) and 0 < max_length <= 300)) and \
        (not temperature or (isinstance(temperature, float) and 0 < temperature <= 1))
