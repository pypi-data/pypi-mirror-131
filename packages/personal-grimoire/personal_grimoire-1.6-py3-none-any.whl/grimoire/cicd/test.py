from mlflow.tracking.client import MlflowClient
from mlflow.entities import ViewType
from mlflow.store.entities import PagedList
from functools import partial
import mlflow
from tqdm import tqdm
import pandas as pd
import datetime as dt
from typing import Dict, Callable, Any

tracking_client = MlflowClient()


def process_paginated_list(method_callback: Callable[[Any], PagedList]) -> list:
    results = []
    collection_finished = False
    page_token = None
    while not collection_finished:
        _batch = method_callback(page_token=page_token)
        results.extend(_batch)
        if not _batch.token:
            collection_finished = True
        else:
            page_token = _batch.token
    return results


def get_all_active_experiments() -> Dict[str, str]:
    listing_callback = partial(
        tracking_client.list_experiments, view_type=ViewType.ACTIVE_ONLY
    )
    all_active_experiments = process_paginated_list(listing_callback)
    experiments = {e.experiment_id: e.name for e in all_active_experiments}
    return experiments


def get_all_runs(experiments_data: Dict[str, str]) -> pd.DataFrame:
    listing_callback = partial(
        tracking_client.search_runs,
        run_view_type=ViewType.ACTIVE_ONLY,
        experiment_ids=list(experiments_data.keys()),
    )
    all_runs = process_paginated_list(listing_callback)
    runs_data = [
        {
            "experiment_id": r.info.experiment_id,
            "experiment_name": experiments_data[r.info.experiment_id],
            "run_id": r.info.run_id,
            "metrics": r.data.metrics,
            "parameters": r.data.params,
            "start_dttm": None
            if not r.info.start_time
            else dt.datetime.utcfromtimestamp(r.info.start_time / 1000),
            "end_dttm": None
            if not r.info.end_time
            else dt.datetime.utcfromtimestamp(r.info.end_time / 1000),
            "tags": r.data.tags,
        }
        for r in all_runs
    ]
    runs_data = pd.DataFrame(runs_data)
    return runs_data


active_experiments = get_all_active_experiments()
runs_data = get_all_runs(active_experiments)
