import gpt_2_simple as gpt2
import os
import tensorflow as tf
import random
from shutil import copyfile

# NOTE: everything non-static should live in /tmp
# NOTE: every finetuned model should be named by model_id

# TODO: play with settings for finetune and generate to speed it up
# TODO: investigate output; finetune doesn't have much effect
# TODO: <|startoftext|> and <|endoftext|> tokens???
# TODO: use a different gpt-2 module? https://github.com/huggingface/transformers?


def _setup_model_dir(model_id, training_strings):
    model_dir = 'tmp/%s' % model_id
    os.mkdir(model_dir)

    while not sum([len(string.split()) for string in training_strings]) > 1023:
        training_strings.append(random.choice(training_strings))
    finetuning_file = "%s/messages.txt" % model_dir
    with open(finetuning_file, "w") as training_fp:
        for training_string in training_strings:
            training_fp.write(training_string + '\n')

    run_dir = '%s/run1' % model_dir
    os.mkdir(run_dir)
    copyfile('models/124M/encoder.json', "%s/encoder.json" % run_dir)
    copyfile('models/124M/hparams.json', "%s/hparams.json" % run_dir)

    return model_dir, finetuning_file


def finetune(model_id, training_strings):
    model_dir, finetuning_file = _setup_model_dir(model_id, training_strings)

    tf.compat.v1.reset_default_graph()
    session = gpt2.start_tf_sess()
    gpt2.finetune(session, finetuning_file, steps=1, checkpoint_dir=model_dir)

    os.remove(finetuning_file)


def generate(model_id, prompt, num_words):
    model_dir = "tmp/%s" % model_id

    tf.compat.v1.reset_default_graph()
    session = gpt2.start_tf_sess()
    gpt2.load_gpt2(session, checkpoint_dir=model_dir)
    output = gpt2.generate(session,
                           checkpoint_dir=model_dir,
                           prefix=prompt,
                           length=num_words if num_words else 100,
                           return_as_list=True)[0]

    return output
