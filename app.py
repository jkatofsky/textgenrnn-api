from utils import (TRAIN_VALIDATOR, GENERATE_VALIDATOR,
                   make_tmp_directory_on_local, clear_memory)
import model_manager
import textgen
from settings import DEFAULT_MAX_LENGTH, DEFAULT_TEMPERATURE

from flask import Flask, request
from flask_cors import CORS
import traceback

app = Flask(__name__)
CORS(app)

SERVER_ERROR = {'error': 'a server error occured'}, 500

make_tmp_directory_on_local()


@app.route("/train", methods=['POST'])
def train():
    try:
        data = request.json

        if not TRAIN_VALIDATOR.validate(data):
            return {'error': TRAIN_VALIDATOR.errors}, 400

        training_strings = data.get('training_strings')
        model = textgen.train(training_strings)
        model_id = model_manager.upload_model(model)

        del model
        clear_memory()

        return {'model_id': model_id}, 200

    except Exception as e:
        traceback.print_exc()
        return SERVER_ERROR


@app.route("/generate", methods=['POST'])
def generate():
    try:
        data = request.json

        if not GENERATE_VALIDATOR.validate(data):
            return {'error': GENERATE_VALIDATOR.errors}, 400

        model_id = data.get('model_id', None)

        model = model_manager.download_model(model_id)

        if not model:
            return {'error': 'model corresponding with model_id does not exist'}, 404

        prompt = data.get('prompt', None)
        max_length = data.get('max_length', DEFAULT_MAX_LENGTH)
        temperature = data.get('temperature', DEFAULT_TEMPERATURE)

        output = textgen.generate(model, prompt, max_length, temperature)

        del model
        clear_memory()

        return {'output': output}, 200

    except Exception as e:
        traceback.print_exc()
        return SERVER_ERROR
