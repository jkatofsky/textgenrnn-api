# rnn-api

## Description

A lightweight web service that allows clients to create an RNN trained on certain strings, and then query it. There is no persistent data; rather, the trained models are deleted a given time after they are last interacted with.

`rnn-api` will not output anything worthy of a NLP paper. Its purpose is to allow web apps to quickly use custom-trained networks. I will to host this API on the free tier of Google App Engine, so there's a limit to how intensive the machine learning can become before things slow to a crawl and costs skyrocket.

## Routes

At the moment, `rnn-api` has two routes:

- `/train`:
  - supply a list of `training_strings`
  - get back `model_id`
- `/generate`:
  - supply a `model_id`, and optionally, a `prompt`, `max_length`, and/or `temperature`
  - get back `output`

## Setup

You can run this API on your machine by cloning this repo,

```bash
git clone https://github.com/jkatofsky/rnn-api.git
cd rnn-api
```

creating a python `venv` (optional, but good practice),

```bash
python3 -m venv env
source env/bin/activate
```

installing the required modules,

```bash
pip3 install -r requirements.txt
```

and running `main.py`.

```bash
python3 main.py
```

I'm planning to run `rnn-api` on Google Cloud's App Engine, which is why `app.yaml` is here. [Here](https://cloud.google.com/appengine/docs/standard/python3/building-app) is Google's guide for deploying a Python 3 app to App Engine.
