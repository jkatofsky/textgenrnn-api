from sanic import Sanic
from sanic.response import json

from gpt import finetune_and_generate

app = Sanic(__name__)

# TODO: error handling


@app.route("/generate")
async def generate(request):

    data = request.json
    training_strings = data.get('training_strings')
    prompt = data.get('prompt', None)
    length = data.get('length', None)

    output = finetune_and_generate(training_strings, prompt, length)

    return json({'output': output}, status=200)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
