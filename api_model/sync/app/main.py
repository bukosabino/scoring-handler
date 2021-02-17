import ast
import os

import flask
from scoring_handler_utils import ManagerProfile

from .model import SyncModel

app = flask.Flask(__name__)

# TODO: settings, pydantic
dir_path = os.path.dirname(os.path.realpath(__file__))
ML_MODEL = SyncModel(
    model_filepath=os.path.join(dir_path, "..", "artifacts", "model.pkl")
)


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
    input_data_text = flask.request.get_data(as_text=True)
    input_data = ast.literal_eval(input_data_text)
    prediction = ML_MODEL.predict(input_data)
    return {"detail": prediction}


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
        api="api_model",
        render_browser=flask.g.render_browser,
    )
    return flask.make_response(response)


if __name__ == "__main__":
    app.run()
