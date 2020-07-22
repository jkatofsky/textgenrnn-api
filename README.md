# textgenrnn-api

## Description

A lightweight Google Cloud API that allows clients to create RNNs trained on arbitirary strings, and then query them. Uses the phenomenal [textgenrnn](https://github.com/minimaxir/textgenrnn) Python module for the text generation. `textgenrnn-api` will not output anything worthy of a NLP paper, but it is pretty fun.

## Routes

At the moment, `textgenrnn-api` has two routes:

- `/train`:
  - supply a list of `training_strings`
  - get back `model_id`
- `/generate`:
  - supply a `model_id`, and optionally, an `options` object which can contain the `prompt`, `max_length`, and/or `temperature` fields
  - get back `output`

## Google Cloud

This project is designed to run on [Google Cloud](https://cloud.google.com/). The rest of this README assumes you have a Google Cloud account, a [project created](https://cloud.google.com/resource-manager/docs/creating-managing-projects), and the [gcloud SDK](https://cloud.google.com/sdk/install) installed.

## Setup

1. Clone this repository.

   ```bash
   git clone https://github.com/jkatofsky/textgenrnn-api.git
   cd textgenrnn-api
   ```

2. create a python `venv` (optional, but good practice).

   ```bash
   python3 -m venv env
   source env/bin/activate
   ```

3. Install the required modules.

   ```bash
   pip3 install -r requirements.txt
   ```

4. [Create a Google Cloud Storage Bucket](https://cloud.google.com/storage/docs/creating-buckets#storage-create-bucket-console) in your project to store the models. Here, you can set the lifespan of models using a [delete  lifycycle rule](https://cloud.google.com/storage/docs/lifecycle?_ga=2.24563129.-2066692002.1593836412#delete).
5. [Download the credentials JSON for the model bucket](https://cloud.google.com/storage/docs/reference/libraries#setting_up_authentication) so the server can access it and set an environment variable to the JSON's path.

   ```bash
   export GOOGLE_APPLICATION_CREDENTIALS=#filename here
   ```

6. Run `main.py`.

   ```bash
   python3 main.py
   ```

## Config

To play with some settings for request handling/text generation you can modify the variables in `config.py`. They're used throughout the API's code.


## Deployment

`app.yaml`'s `env_variables` section will set the storage credentials JSON path to an environment variable on the cloud, just like how you set it locally. So, make sure that you set the `GOOGLE_APPLICATION_CREDENTIALS` environment variable correctly in `app.yaml`.

Other than that, you should be able to deploy this repo right to App Engine:

```bash
gcloud config set [your project name]
gcloud app deploy
```

For more information, [here](https://cloud.google.com/appengine/docs/standard/python3/building-app) is Google's guide for deploying a Python 3 app.
