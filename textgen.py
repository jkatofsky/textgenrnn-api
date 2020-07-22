from config import TRAINING_EPOCHS
from textgenrnn import textgenrnn
import os

BASE_DIR = os.getcwd()


def train(training_strings):
    os.chdir('/tmp')

    model = textgenrnn()
    model.train_on_texts(
        training_strings, num_epochs=TRAINING_EPOCHS, gen_epochs=0)

    os.chdir(BASE_DIR)
    return model


def generate(model, prompt, max_length, temperature):
    output = model.generate(prefix=prompt,
                            max_gen_length=max_length,
                            temperature=temperature,
                            return_as_list=True)[0]
    return output
