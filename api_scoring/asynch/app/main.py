import ast
import asyncio
import os
import typing as tp
from contextlib import nullcontext

import fastapi as fa
import httpx
import numpy as np
from scoring_handler_utils import ManagerProfile

import redis

app = fa.FastAPI()

# TODO: settings, pydantic
NUM_MODELS = 2
DST_URL = "127.0.0.1"
SRC_PORT = 8001
DST_PORT = 8000


@app.get("/")
def read_root():

    content = f"""
    <body>
        <h1> Async Scoring Handler REST API is alive! </h1>
        <br>
        <ul>
            <li>
                <a href="http://localhost:{SRC_PORT}/docs/">Endpoints Documentation</a>
            </li>
        </ul>
    </body>
    """
    return fa.responses.HTMLResponse(content=content)


@app.get("/api/v1/healthcheck")
def health_check():
    """Asynchronous Health Check"""
    return {"status": "OK"}


@app.post("/api/v1/ml/async/predict")
async def predict(input_data: tp.List[float], request: fa.Request):
    """Asynchronous prediction"""
    # TODO: logging

    # Get Redis info
    redis_connector = redis.Redis(host="localhost", port=6379, db=0)
    redis_connector.get("invent-key")  # None

    # Prepare API calls
    render_browser = "render-browser" in request.query_params
    params = {}
    if "profile" in request.query_params and "profile-type" in request.query_params:
        params = {
            "profile": request.query_params.get("profile"),
            "profile-type": request.query_params.get("profile-type"),
        }
        if render_browser:
            params["render-browser"] = "true"
    url = f"http://{DST_URL}:{DST_PORT}/api/v1/ml/async/predict"

    # API async calls
    async with httpx.AsyncClient() as client:
        future_coroutines = [
            client.post(url, json=input_data, params=params) for _ in range(NUM_MODELS)
        ]
        responses = [
            await coroutine for coroutine in asyncio.as_completed(future_coroutines)
        ]

    # Processing responses
    predictions = []
    for resp in responses:
        resp_text = ast.literal_eval(resp.text)
        resp_text = resp_text.get("detail")
        predictions.append(float(resp_text))
    mean_prediction = np.mean(predictions)

    return {"detail": mean_prediction}


@app.middleware("http")
async def add_process_time_header(request: fa.Request, call_next):
    context_manager = nullcontext()
    if "profile" in request.query_params and "profile-type" in request.query_params:
        profile = ManagerProfile()
        type_profile = request.query_params.get("profile-type")
        profiler = profile.factory(type_profile, sync=False)
        context_manager = profiler.start()

    with context_manager:
        response = await call_next(request)

    if "profile" in request.query_params and "profile-type" in request.query_params:
        is_docker = os.environ.get("RUNNING_DOCKER_CONTAINER", False)
        path_profile = request.query_params.get("profile")
        render_browser = "render-browser" in request.query_params
        profiler.stop_and_write(
            path_profile, is_docker, api="api_scoring", render_browser=render_browser
        )

    return response
