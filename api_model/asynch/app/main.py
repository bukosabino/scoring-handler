import os
import typing as tp
from contextlib import nullcontext

import fastapi as fa
import fastapi.responses as fa_resp
from scoring_handler_utils import ManagerProfile

from .model import AsyncModel

app = fa.FastAPI()


# TODO: settings, pydantic
dir_path = os.path.dirname(os.path.realpath(__file__))
ML_MODEL = AsyncModel(
    model_filepath=os.path.join(dir_path, "..", "artifacts", "model.pkl")
)


@app.get("/")
def read_root():

    content = """
    <body>
        <h1> Async Model REST API is alive! </h1>
        <br>
        <ul>
            <li>
                <a href="http://localhost:8000/docs/">Endpoints Documentation</a>
            </li>
        </ul>
    </body>
    """
    return fa_resp.HTMLResponse(content=content)


@app.get("/api/v1/healthcheck")
def health_check():
    """Asynchronous Health Check"""
    return {"status": "OK"}


@app.post("/api/v1/ml/async/predict")
async def predict(input_data: tp.List[float] = [5.1, 3.5, 1.4, 0.2]):
    """Asynchronous prediction"""
    prediction = await ML_MODEL.predict(input_data)
    return {"detail": prediction}


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
            path_profile, is_docker, api="api_model", render_browser=render_browser
        )

    return response
