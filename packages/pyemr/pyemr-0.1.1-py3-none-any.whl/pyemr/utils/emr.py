"""A collection of aws tools"""
import time

import awswrangler as wr
import boto3
import pandas as pd
from loguru import logger
from tqdm import tqdm


def cancel_emr_step(cluster_id, step_id):
    """

    Args:
      cluster_id:
      step_id:

    Returns:

    """
    client = boto3.client("emr")
    response = client.cancel_steps(
        ClusterId=cluster_id,
        StepIds=[step_id],
    )
    logger.info(f"Canceled step {step_id}")
    return response


def yield_step_state(cluster_id, step_id, sleep=4):
    """

    Args:
      cluster_id:
      step_id:
      sleep: (Default value = 4)

    Returns:

    """

    while True:
        time.sleep(sleep)
        state = wr.emr.get_step_state(cluster_id, step_id)
        yield state


def wait_else_cancel(cluster_id, step_id, desc="Waiting"):
    """

    Args:
      cluster_id:
      step_id:
      desc: (Default value = 'Waiting')

    Returns:

    """

    last_state = None
    pbar = tqdm(
        yield_step_state(cluster_id, step_id, sleep=5),
        desc=f"{desc}:step_id={step_id},state=SUBMITTING",
    )

    # wait for step to complete
    try:
        for state in pbar:
            if state != last_state:
                pbar.set_description(f"{desc}:step_id={step_id},state={state}")

            last_state = state
            if state in ["COMPLETED", "FAILED"]:
                break
    except KeyboardInterrupt:
        cancel_emr_step(cluster_id, step_id)


def get_clusters_list_df(states, n) -> pd.DataFrame:
    """Returns a dictionary of cluster and cluster ids

    Args:
      states:
      n:

    Returns:

    """

    res = {}
    client = boto3.client("emr")
    clusters = client.list_clusters(ClusterStates=states)
    clusters = pd.json_normalize(clusters["Clusters"], sep="_").sort_values(
        "Status_Timeline_CreationDateTime", ascending=False
    )

    return clusters[["Id", "Name", "Status_State", "Status_Timeline_CreationDateTime"]]
