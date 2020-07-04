import gpt_2_simple as gpt2
import os
import gc
import tensorflow as tf
import random

session = gpt2.start_tf_sess(threads=1)
gpt2.load_gpt2(session)


# TODO: eventually need to use /tmp for any files generated below
# TODO: play with settings for finetune and generate to speed it up
# TODO: auto clean up files in the checkpoint folder
# TODO: investigate output; finetune doesn't have much effect

def finetune_and_generate(training_strings, prompt, num_words):

    while not sum([len(string.split()) for string in training_strings]) > 1023:
        training_strings.append(random.choice(training_strings))

    tf.reset_default_graph()
    global session
    session = gpt2.start_tf_sess(threads=1)

    with open("tmp/training.txt", "w") as training_fp:
        for training_string in training_strings:
            training_fp.write(training_string + '\n')

    gpt2.finetune(session, "tmp/training.txt", steps=1)

    text = gpt2.generate(session,
                         prefix=prompt,
                         length=num_words if num_words else 100,
                         return_as_list=True)[0]

    os.remove("tmp/training.txt")
    gc.collect()

    return text
