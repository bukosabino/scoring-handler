import os
import time
import timeit

import numpy as np
import pandas as pd
import requests
import typer

dir_path = os.path.dirname(os.path.realpath(__file__))
default_folder_output = os.path.join(dir_path, "output")


def sync_call():
    requests.post(
        "http://127.0.0.1:5001/api/v1/ml/sync/predict", json=[5.1, 3.5, 1.4, 0.2]
    )


def async_call():
    requests.post(
        "http://127.0.0.1:8001/api/v1/ml/async/predict", json=[5.1, 3.5, 1.4, 0.2]
    )


def main(
    min_number_calls: int = typer.Option(default=1),
    max_number_calls: int = typer.Option(default=11),
    repetitions: int = typer.Option(default=10),
    output_folder: str = typer.Option(
        default=default_folder_output, help="Path to save output files"
    ),
):

    range_calls = range(min_number_calls, max_number_calls)
    async_times, sync_times = [], []
    for n_calls in range_calls:

        print(f"Iteration number {n_calls}")

        time.sleep(1)

        timer = timeit.Timer("async_call()", setup="from __main__ import async_call")
        timed = timer.repeat(repeat=repetitions, number=n_calls)
        async_time = np.mean([timed])
        print(
            f"Running {repetitions} times {n_calls} Async API calls at {async_time} seconds"
        )

        time.sleep(1)

        timer = timeit.Timer("sync_call()", setup="from __main__ import sync_call")
        timed = timer.repeat(repeat=repetitions, number=n_calls)
        sync_time = np.mean([timed])
        print(
            f"Running {repetitions} times {n_calls} Sync API calls at {sync_time} seconds"
        )

        async_times.append(async_time)
        sync_times.append(sync_time)

    results = {
        "times": np.array(range_calls),
        "async": np.array(async_times),
        "sync": np.array(sync_times),
    }

    df = pd.DataFrame(data=results, index=results["times"], columns=["async", "sync"])
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    output_file_path = os.path.join(
        output_folder,
        f"results_{min_number_calls}_{max_number_calls}_{repetitions}.csv",
    )
    df.to_csv(output_file_path, index_label="times")

    print(
        f"The servers are successfully benchmarked. The experiment results are in {output_file_path}"
    )


if __name__ == "__main__":
    typer.run(main)
