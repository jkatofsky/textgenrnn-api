from sanic import Sanic
from sanic.response import json

import gpt


app = Sanic(__name__)

# TODO: error handling
# TODO: accept more settings for training from the client? (i.e. temperature)
# TODO: after this works, use /tmp and tokens/sessions to create TWO routes:
#   - /finetune: make finetuned model, on given message set, w/ short lifespan
#   - /generate: generate from model, if it exists and client has permission


@app.route("/generate", methods=['POST'])
async def generate(request):

    data = request.json
    training_strings = data.get('training_strings')
    prompt = data.get('prompt', None)
    num_words = data.get('num_words', None)

    output = gpt.finetune_and_generate(training_strings, prompt, num_words)

    return json({'output': output},
                status=200,
                headers={'Access-Control-Allow-Origin': '*'})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
