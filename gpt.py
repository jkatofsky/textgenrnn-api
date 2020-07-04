import gpt_2_simple as gpt2
import os
import tensorflow as tf
import random

# NOTE: everything non-static should live in /tmp
# NOTE: every finetuned model should be named by model_id

# TODO: play with settings for finetune and generate to speed it up
# TODO: investigate output; finetune doesn't have much effect
# TODO: <|startoftext|> and <|endoftext|> tokens???
# TODO: use a different gpt-2 module? https://github.com/huggingface/transformers?


def finetune(model_id, training_strings):
    while not sum([len(string.split()) for string in training_strings]) > 1023:
        training_strings.append(random.choice(training_strings))
    filename = "tmp/%s.txt" % model_id
    with open(filename, "w") as training_fp:
        for training_string in training_strings:
            training_fp.write(training_string + '\n')

    # TODO: re-implement finetuning

    os.remove(filename)


def generate(model_id, prompt, num_words):

    # TODO: re-implement generating

    return None
