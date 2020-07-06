from sanic import Sanic
from sanic.response import json
import rnn
import auth

app = Sanic(__name__)

ALLOW_ACCESS_HEADER = {'Access-Control-Allow-Origin': '*'}

# TODO: keys, sessions, cookies, or tokens? anyone can call API currently
# TODO: only allow one client to:
#       - /finetune N models?
#       - /generate N times per minute?
# TODO: change to be more CRUD-y? create, re-train, delete?
# TODO: add logging everywhere & remove unecessary prints
# TODO: right now, calls to rnn.train block processing of other requests
#       - look into threading or better use of async functions to change this
# TODO: enforce min/max num of training strings?


@app.route("/train", methods=['POST'])
async def train(request):
    try:
        data = request.json
        training_strings = data.get('training_strings', [])
        if len(training_strings) == 0 or \
                any(not isinstance(elem, str) for elem in training_strings):
            return json({'error': 'training_strings was not supplied properly.'},
                        status=400,
                        headers=ALLOW_ACCESS_HEADER)

        model_id = auth.create_model_id()

        rnn.train(model_id, training_strings)

        auth.reset_expiration_time(model_id)

        response = json({'model_id': model_id},
                        status=200,
                        headers=ALLOW_ACCESS_HEADER)

    except Exception as e:
        response = json({'error': 'A server error occured on the server while training the model.'},
                        status=500, headers=ALLOW_ACCESS_HEADER)

    return response


@app.route("/generate", methods=['POST'])
async def generate(request):
    try:
        data = request.json
        model_id = data.get('model_id', None)
        options = data.get('options', {})
        if not model_id or not isinstance(model_id, str):
            return json({'error': 'model_id was not supplied properly.'},
                        status=400,
                        headers=ALLOW_ACCESS_HEADER)
        if not auth.is_valid_id(model_id):
            return json({'error': 'Model corresponding with model_id does not exist.'},
                        status=401,
                        headers=ALLOW_ACCESS_HEADER)

        auth.using_model(model_id)

        output = rnn.generate(model_id, options)

        auth.reset_expiration_time(model_id)

        response = json({'output': output},
                        status=200,
                        headers=ALLOW_ACCESS_HEADER)

    except Exception as e:
        response = json({'error': 'A server error occured while training the model.'},
                        status=500, headers=ALLOW_ACCESS_HEADER)

    return response


if __name__ == "__main__":
    app.add_task(auth.cleanup_loop())
    app.run(host="0.0.0.0", port=8000)
