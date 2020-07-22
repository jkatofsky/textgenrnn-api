from utils import valid_training_strings, valid_model_id, valid_options
import model_manager
import textgen
from sanic import Sanic
from sanic.response import json
from sanic_cors import CORS
import os
import traceback

app = Sanic(__name__)
CORS(app)

SERVER_ERROR = json({'error': 'A server error occured.'},
                    status=500)


@app.route("/train", methods=['POST'])
async def train(request):
    try:
        data = request.json
        training_strings = data.get('training_strings', None)
        if not valid_training_strings(training_strings):
            return json({'error': 'training_strings was not supplied properly.'}, status=400)

        model = textgen.train(training_strings)
        model_id = model_manager.save_model(model)

        return json({'model_id': model_id}, status=200)

    except Exception as e:
        traceback.print_exc()
        return SERVER_ERROR


@app.route("/generate", methods=['POST'])
async def generate(request):
    try:
        data = request.json
        model_id = data.get('model_id', None)
        options = data.get('options', {})
        if not valid_model_id(model_id):
            return json({'error': 'model_id was not supplied properly.'}, status=400)
        if not valid_options(options):
            return json({'error': 'options was not supplied properly.'}, status=400)

        model = model_manager.get_model(model_id)

        if not model:
            return json({'error': 'Model corresponding with model_id does not exist.'}, status=401)

        prompt = options.get('prompt', None)
        max_length = options.get('max_length', 300)
        temperature = options.get('temperature', 0.5)

        output = textgen.generate(model, prompt, max_length, temperature)

        return json({'output': output}, status=200)

    except Exception as e:
        traceback.print_exc()
        return SERVER_ERROR


# only excecutes when running server locally
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True, access_log=True)
