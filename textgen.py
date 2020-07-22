from config import TRAINING_EPOCHS
from textgenrnn import textgenrnn
import os

BASE_DIR = os.getcwd()


def _get_model_dir(model_id):
    return '/tmp/%s' % model_id


def train(model_id, training_strings):
    model_dir = _get_model_dir(model_id)
    os.mkdir(model_dir)
    os.chdir(model_dir)

    textgen = textgenrnn()
    textgen.train_on_texts(
        training_strings, num_epochs=TRAINING_EPOCHS, gen_epochs=0)
    textgen.save(weights_path="weights.hdf5")

    os.chdir(BASE_DIR)


def generate(model_id, prompt, max_length, temperature):
    model_dir = _get_model_dir(model_id)
    os.chdir(model_dir)

    textgen = textgenrnn("weights.hdf5")
    output = textgen.generate(prefix=prompt,
                              max_gen_length=max_length,
                              temperature=temperature,
                              return_as_list=True)[0]

    os.chdir(BASE_DIR)
    return output
