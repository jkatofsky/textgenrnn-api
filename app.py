from utils import valid_training_strings, valid_model_id, valid_options
import model_manager
import textgen

from flask import Flask, request
from flask_cors import CORS
import traceback

app = Flask(__name__)
CORS(app)

SERVER_ERROR = {'error': 'A server error occured.'}, 500


@app.route("/train", methods=['POST'])
def train():
    try:
        data = request.json
        training_strings = data.get('training_strings', None)
        if not valid_training_strings(training_strings):
            return {'error': 'training_strings was not supplied properly.'}, 400

        model = textgen.train(training_strings)
        model_id = model_manager.upload_model(model)

        return {'model_id': model_id}, 200

    except Exception as e:
        traceback.print_exc()
        return SERVER_ERROR


@app.route("/generate", methods=['POST'])
def generate():
    try:
        data = request.json
        model_id = data.get('model_id', None)
        options = data.get('options', {})
        if not valid_model_id(model_id):
            return {'error': 'model_id was not supplied properly.'}, 400
        if not valid_options(options):
            return {'error': 'options was not supplied properly.'}, 400

        model = model_manager.download_model(model_id)

        if not model:
            return {'error': 'Model corresponding with model_id does not exist.'}, 404

        prompt = options.get('prompt', None)
        max_length = options.get('max_length', 300)
        temperature = options.get('temperature', 0.5)

        output = textgen.generate(model, prompt, max_length, temperature)

        return {'output': output}, 200

    except Exception as e:
        traceback.print_exc()
        return SERVER_ERROR
