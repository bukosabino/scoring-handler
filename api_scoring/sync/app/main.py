import ast
import os

import flask
import numpy as np
import requests
from scoring_handler_utils import ManagerProfile

import redis

app = flask.Flask(__name__)

# TODO: settings, pydantic
NUM_MODELS = 2
DST_URL = "127.0.0.1"
DST_PORT = 5000


@app.route("/")
def url_doc():
    urls = {
        "predict": {
            "endpoint": "/api/v1/ml/sync/predict/",
            "method": "POST",
        },
        "health_check": {
            "endpoint": "/api/v1/healthcheck/",
            "method": "GET",
        },
    }
    response = flask.jsonify(urls)
    response.status_code = 200
    return response


@app.route("/api/v1/healthcheck")
def health_check():
    """Synchronous Health Check"""
    return {"status": "OK"}


@app.route("/api/v1/ml/sync/predict", methods=["POST"])
def predict():
    """Synchronous prediction"""
    # TODO: logging

    # Get Redis info
    redis_connector = redis.Redis(host="localhost", port=6379, db=0)
    redis_connector.get("invent-key")  # None

    # Prepare API calls
    input_data_text = flask.request.get_data(as_text=True)
    input_data = ast.literal_eval(input_data_text)
    params = {}
    if "profile" in flask.request.args and "profile-type" in flask.request.args:
        params = {
            "profile": flask.request.args.get("profile"),
            "profile-type": flask.request.args.get("profile-type"),
        }
        if flask.g.render_browser:
            params["render-browser"] = "true"
    url = f"http://{DST_URL}:{DST_PORT}/api/v1/ml/sync/predict"

    # API async calls
    responses = [
        requests.post(url, json=input_data, params=params) for _ in range(NUM_MODELS)
    ]

    # Processing responses
    predictions = []
    for resp in responses:
        resp_text = ast.literal_eval(resp.text)
        resp_text = resp_text.get("detail")
        predictions.append(float(resp_text))
    mean_prediction = np.mean(predictions)

    return {"detail": mean_prediction}


@app.before_request
def before_request():
    if "profile" in flask.request.args and "profile-type" in flask.request.args:
        profile = ManagerProfile()
        type_profile = flask.request.args.get("profile-type")
        flask.g.profiler = profile.factory(type_profile, sync=True)
        flask.g.context_manager = flask.g.profiler.start()
        flask.g.profiler_output_folder = flask.request.args.get("profile")

    flask.g.render_browser = "render-browser" in flask.request.args


@app.after_request
def after_request(response):
    if not hasattr(flask.g, "profiler"):
        return response

    is_docker = os.environ.get("RUNNING_DOCKER_CONTAINER", False)
    flask.g.profiler.stop_and_write(
        flask.g.profiler_output_folder,
        is_docker,
        api="api_scoring",
        render_browser=flask.g.render_browser,
    )
    return flask.make_response(response)


if __name__ == "__main__":
    app.run(port=5001)
