# textgenrnn-api

## Description

A lightweight Python API, designed to run on Google Cloud, which allows clients to train RNNs on arbitirary strings and then generate output. Uses the phenomenal [textgenrnn](https://github.com/minimaxir/textgenrnn) module for text generation and [Flask](https://github.com/pallets/flask) as a web framework. `textgenrnn-api` will not output anything worthy of a NLP paper, but it's still pretty fun.

## Routes

`textgenrnn-api` has two routes:

- `/train`:
  - supply a list of `training_strings`
  - get back `model_id`
- `/generate`:
  - supply a `model_id`, and optionally, an `options` object which can contain the `prompt`, `max_length`, and/or `temperature` fields
  - get back `output`

## Setup

1. Clone this repository.

   ```bash
   git clone https://github.com/jkatofsky/textgenrnn-api.git
   cd textgenrnn-api
   ```

2. Create a python `venv` (optional, but good practice).

   ```bash
   python3 -m venv env
   source env/bin/activate
   ```

3. Install the required modules.

   ```bash
   pip3 install -r requirements.txt
   ```

4. Create a [Google Cloud project](https://cloud.google.com/resource-manager/docs/creating-managing-projects) and set the `PROJECT_NAME` variable appropriately in `settings.py`.
5. [Create a Google Cloud Storage Bucket](https://cloud.google.com/storage/docs/creating-buckets#storage-create-bucket-console) in your project to store the models and set the `MODEL_BUCKET_NAME` variable appropriately in `settings.py`. You can optionally set a lifespan for the models using a [delete  lifycycle rule](https://cloud.google.com/storage/docs/lifecycle?_ga=2.24563129.-2066692002.1593836412#delete).
6. [Download a service account credentials JSON](https://cloud.google.com/storage/docs/reference/libraries#setting_up_authentication) for your project with permissions for the model bucket and set the `CREDENTIALS_JSON_PATH` variable appropriately in `settings.py`.

7. To test the server locally (with convenient hot reload), use the following command.

   ```bash
   python3 -m flask run --reload
   ```

8. Assuming you have the [gcloud SDK](https://cloud.google.com/sdk/install) installed and have set the desired project as your current one, you can deploy this repo right to App Engine.

   ```bash
   gcloud app deploy
   ```

   For more information, [here](https://cloud.google.com/appengine/docs/standard/python3/building-app) is Google's guide for deploying a Python 3 app.
