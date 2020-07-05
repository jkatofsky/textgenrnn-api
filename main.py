from sanic import Sanic
from sanic.response import json
import rnn
import auth

app = Sanic(__name__)

ALLOW_ACCESS_HEADER = {'Access-Control-Allow-Origin': '*'}


# TODO: error handling
# TODO: only allow one IP address to:
#       - /finetune N models?
#       - /generate N times per minute?
# TODO: change to be more CRUD-y? create, re-train, delete?
# TODO: add logging everywhere


# TODO: enforce max num of training strings?
@app.route("/train", methods=['POST'])
async def train(request):

    data = request.json
    training_strings = data.get('training_strings')

    model_id = auth.create_model_id()

    rnn.train(model_id, training_strings)

    auth.reset_expiration_time(model_id)

    return json({'model_id': model_id},
                status=200,
                headers=ALLOW_ACCESS_HEADER)


@app.route("/generate", methods=['POST'])
async def generate(request):

    data = request.json
    model_id = data.get('model_id', None)

    options = data.get('options', {})

    is_valid_model_id = auth.is_valid_id(model_id)

    auth.using_model(model_id)

    output = rnn.generate(model_id, options)

    auth.reset_expiration_time(model_id)

    return json({'output': output},
                status=200,
                headers=ALLOW_ACCESS_HEADER)


if __name__ == "__main__":
    app.add_task(auth.cleanup_loop())
    app.run(host="0.0.0.0", port=8000)
