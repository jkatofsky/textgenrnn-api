from sanic import Sanic
from sanic.response import json
import gpt
import auth

app = Sanic(__name__)

ALLOW_ACCESS_HEADER = {'Access-Control-Allow-Origin': '*'}

# TODO: error handling
# TODO: accept more settings from the client? (i.e. temperature)
# TODO: only allow one IP address to:
#       - /finetune N models
#       - /generate N times per minute
# TODO: change routes to be more CRUD-y? create, re-train, delete?


@app.route("/modelIdExpired", methods=['POST'])
async def model_id_expired(request):

    data = request.json

    model_id = data.get('model_id', None)

    _, is_expired = auth.authenticate_id(model_id)

    return json({'is_expired': is_expired},
                status=200,
                headers=ALLOW_ACCESS_HEADER)


@app.route("/finetune", methods=['POST'])
async def finetune(request):

    data = request.json
    training_strings = data.get('training_strings')

    model_id = auth.create_model_id()

    gpt.finetune(model_id, training_strings)

    auth.set_expiration_time(model_id)

    return json({'model_id': model_id},
                status=200,
                headers=ALLOW_ACCESS_HEADER)


@app.route("/generate", methods=['POST'])
async def generate(request):

    data = request.json
    model_id = data.get('model_id', None)
    prompt = data.get('prompt', None)
    num_words = data.get('num_words', None)

    model_id, expired = auth.authenticate_id(model_id)

    output = gpt.generate(model_id, prompt, num_words)

    auth.set_expiration_time(model_id)

    return json({'output': output},
                status=200,
                headers=ALLOW_ACCESS_HEADER)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
