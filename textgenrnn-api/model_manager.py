import secrets
import time
import shutil
import gc
import asyncio
import os

model_id_last_used_map = {}

MODEL_LIFESPAN = int(os.getenv("MODEL_LIFESPAN"))
MODEL_CLEANUP_INTERVAL = int(os.getenv("MODEL_CLEANUP_INTERVAL"))


def create_model_id():
    model_id = secrets.token_urlsafe(nbytes=16)
    using_model(model_id)
    return model_id


def reset_expiration_time(model_id):
    model_id_last_used_map[model_id] = time.time()


def model_exists(model_id):
    return model_id in model_id_last_used_map.keys()


def using_model(model_id):
    model_id_last_used_map[model_id] = None


def _delete_model(model_id):
    shutil.rmtree('tmp/%s' % model_id)
    del model_id_last_used_map[model_id]
    gc.collect()


def _cleanup_unused_models():
    current_time = time.time()
    for model_id in list(model_id_last_used_map):
        last_used_time = model_id_last_used_map[model_id]
        if last_used_time and (current_time - last_used_time) > MODEL_LIFESPAN:
            _delete_model(model_id)


async def cleanup_loop():
    while True:
        await asyncio.sleep(MODEL_CLEANUP_INTERVAL)
        _cleanup_unused_models()
