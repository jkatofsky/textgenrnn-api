from sanic import Sanic
from sanic.response import json
import gpt
import auth

app = Sanic(__name__)


# TODO: error handling
# TODO: accept more settings from the client? (i.e. temperature)


@app.route("/token-expired", methods=['POST'])
async def token_expired(request):

    data = request.json

    client_token = data.get('token', None)

    _, is_expired = auth.authenticate_token(client_token)

    return json({'is_expired': is_expired},
                status=200,
                headers={'Access-Control-Allow-Origin': '*'})


@app.route("/finetune", methods=['POST'])
async def finetune(request):

    data = request.json
    training_strings = data.get('training_strings')

    client_token, model_id = auth.create_token_and_model_id()

    gpt.finetune(model_id, training_strings)

    auth.set_expiration_time(client_token)

    return json({'token': client_token},
                status=200,
                headers={'Access-Control-Allow-Origin': '*'})


@app.route("/generate", methods=['POST'])
async def generate(request):

    data = request.json
    client_token = data.get('token', None)
    prompt = data.get('prompt', None)
    num_words = data.get('num_words', None)

    model_id, expired = auth.authenticate_token(client_token)

    output = gpt.generate(model_id, prompt, num_words)

    auth.set_expiration_time(client_token)

    return json({'output': output},
                status=200,
                headers={'Access-Control-Allow-Origin': '*'})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
