from textgenrnn import textgenrnn
import os


def _get_model_dir(model_id):
    return 'tmp/%s' % model_id


def train(model_id, training_strings):
    model_dir = _get_model_dir(model_id)
    os.mkdir(model_dir)
    textgen = textgenrnn()
    textgen.train_new_model(training_strings)
    textgen.save(weights_path="%s/weights.hdf5" % model_dir)


def generate(model_id, prompt, num_words):
    model_dir = _get_model_dir(model_id)
    textgen = textgenrnn("%s/weights.hdf5" % model_dir)
    output = textgen.generate(prefix=prompt, max_gen_length=num_words)
    return output
