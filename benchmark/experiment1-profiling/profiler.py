import os
import typing as tp
from enum import Enum

import requests
import typer
from scoring_handler_utils import ManagerProfile


class ProfilerEnum(str, Enum):
    pyinstrument = "pyinstrument"
    yappi = "yappi"


class ServerEnum(str, Enum):
    sync = "sync"
    asynch = "async"


dir_path = os.path.dirname(os.path.realpath(__file__))
default_folder_output = os.path.join(dir_path, "output", "client")


def main(
    mode: ServerEnum = typer.Option(...),
    profiler_client: tp.Optional[ProfilerEnum] = typer.Option(default=None),
    profiler_server: tp.Optional[ProfilerEnum] = typer.Option(default=None),
    profiler_server_html: tp.Optional[bool] = typer.Option(default=False),
    output_path: str = typer.Option(
        default=default_folder_output, help="Path to save output files"
    ),
):
    dst_port = 5001 if mode == ServerEnum.sync else 8001
    url = f"http://127.0.0.1:{dst_port}/api/v1/ml/{mode}/predict"

    params = {}
    if profiler_server:

        folder_output_server = os.path.join(output_path, "server")
        if not os.path.exists(folder_output_server):
            os.makedirs(folder_output_server)

        params = {"profile": folder_output_server, "profile-type": profiler_server}
        if profiler_server_html and profiler_server == ProfilerEnum.pyinstrument:
            params["render-browser"] = "true"

    if profiler_client:
        folder_output_client = os.path.join(output_path, "client")
        if not os.path.exists(folder_output_client):
            os.makedirs(folder_output_client)

        profile = ManagerProfile()
        profiler = profile.factory(type_input_data=profiler_client, sync=True)
        profiler.start()

    requests.post(url, json=[5.1, 3.5, 1.4, 0.2], params=params)

    if profiler_client:
        profiler.stop_and_write(
            path_profile=folder_output_client, is_docker=False, api="client"
        )


if __name__ == "__main__":
    typer.run(main)
