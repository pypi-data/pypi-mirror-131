"""A collection of aws tools"""
import fnmatch
import gzip
import os
import os.path
import pathlib
from os.path import abspath, dirname

import boto3
import pandas as pd
from loguru import logger
from tqdm import tqdm
import re

from .config import (
    _get_pyproject_toml,
    cprint,
    get_cluster_name,
    get_env_name,
    get_s3_staging_dir,
    get_version,
    load_config,
)
from .emr import cancel_emr_step

# import awswrangler as wr


CLUSTER_STATES = ["WAITING", "RUNNING"]


def _upload_to_s3(
    local_path,
    s3_path,
):
    """Upload file to s3

    Args:
      local_path:
      s3_path:

    Returns:

    """
    _, _, bucket, key = s3_path.split("/", 3)
    s3 = boto3.resource("s3")  # pylint: disable=C0103

    print("")
    cprint(f"Uploading '{local_path}' to s3...")
    print(f"out_path={s3_path}")

    file_size = os.stat(local_path).st_size

    def callback(bytes_transferred):
        """

        Args:
          bytes_transferred:

        Returns:

        """
        return pbar.update(bytes_transferred)

    with tqdm(
        total=file_size, unit="B", unit_scale=True, desc=f"Uploading '{local_path}'"
    ) as pbar:
        s3.meta.client.upload_file(
            Filename=local_path,
            Bucket=bucket,
            Key=key,
            Callback=callback,
        )

    print(f"Uploaded '{local_path}' to '{s3_path}'")


def copy_on_s3(path, new_path):
    """Copy a blob on s3 to another s3 location

    Args:
      path:
      new_path:

    Returns:

    """
    print(f"Copying '{path}' to '{new_path}'.")
    s3 = boto3.resource("s3")  # pylint: disable=C0103
    _, _, bucket, key = path.split("/", 3)
    _, _, new_bucket, new_key = new_path.split("/", 3)

    copy_source = {"Bucket": bucket, "Key": key}

    bucket = s3.Bucket(new_bucket)
    bucket.copy(copy_source, new_key)


def get_staging_dir():
    """Returns the staging directory along with version and stage."""
    conf = load_config()
    print(conf)
    stage = conf["stage"]
    version = get_version()
    s3_stage_dir = get_s3_staging_dir()
    stage_path = f"{s3_stage_dir}/stage={stage}/version={version}"
    return stage_path


def get_clusters() -> dict:
    """Returns a dictionary of cluster and cluster ids"""

    res = {}
    client = boto3.client("emr")
    clusters = client.list_clusters(ClusterStates=CLUSTER_STATES)
    for cluster in clusters["Clusters"]:
        res[cluster["Name"]] = cluster["Id"]

    return res


def get_cluster_id(cluster_name: str) -> str:
    """

    Args:
      cluster_name: str:

    Returns:

    """

    if (cluster_name is None) or (cluster_name == "") or not cluster_name:
        cluster_name = load_config()["cluster-name"]

    client = boto3.client("emr")
    clusters = client.list_clusters(ClusterStates=CLUSTER_STATES)
    for cluster in clusters["Clusters"]:
        if cluster["Name"] == cluster_name:
            return cluster["Id"]

    for cluster in clusters["Clusters"]:
        if (type(cluster["Name"]) == str) and (type(cluster_name) == str):
            if cluster["Name"].lower() == cluster_name.lower():
                return cluster["Id"]

    raise ValueError(
        f"No cluster called '{cluster_name}' in states '{CLUSTER_STATES}' ."
    )


def get_file_s3_path(local_file_path, datetime, suffix):
    """

    Args:
      file_name:
      datetime: (Default value = "latest")
      suffix: (Default value = "code")
      local_file_path:

    Returns:

    """
    file_name = local_file_path.split("/")[-1]
    staging_dir = get_staging_dir()
    if datetime == "latest":
        return f"{staging_dir}/{suffix}/latest/{file_name}"

    return f"{staging_dir}/{suffix}/datetime={datetime}/{file_name}"


def upload_to_s3_stage(in_path, datetime, suffix):
    """

    Args:
      in_path:
      datetime: (Default value = "latest")
      suffix: (Default value = "code")

    Returns:

    """

    s3_path = get_file_s3_path(in_path, datetime, suffix)
    _upload_to_s3(in_path, s3_path)

    if datetime != "latest":
        s3_path_latest = get_file_s3_path(in_path, "latest", suffix)
        copy_on_s3(s3_path, s3_path_latest)
        return s3_path_latest

    return s3_path


def describe_cluster(cluster_name):
    """

    Args:
      cluster_name:

    Returns:

    """
    client = boto3.client("emr")
    cluster_id = get_cluster_id(cluster_name)
    cluster_desc = client.describe_cluster(ClusterId=cluster_id)
    return cluster_desc


def get_log_url(cluster_name):
    """

    Args:
      cluster_name:

    Returns:

    """
    desc = describe_cluster(cluster_name)
    return desc["Cluster"]["LogUri"]


def get_master_ec2_instance_id(cluster_name):
    """Returns the master node ec2 instanceid.

    Args:
      cluster_name:

    Returns:

    """

    client = boto3.client("emr")
    cluster_id = get_cluster_id(cluster_name)
    cluster_desc = client.describe_cluster(ClusterId=cluster_id)
    master_public_dns_name = cluster_desc["Cluster"]["MasterPublicDnsName"]

    instance_info = client.list_instances(ClusterId=cluster_id)
    for instance in instance_info["Instances"]:
        if master_public_dns_name == instance["PublicDnsName"]:
            master_ec2_instanceid = instance["Ec2InstanceId"]
            print(
                f"'{cluster_name}' cluster master ec2 instance id = {master_ec2_instanceid}"
            )
            return master_ec2_instanceid

    raise ValueError("No ec2 instance id found for {cluster_name}.")


def ssm_cluster(cluster_name: str):
    """Opens an ssm session into the master node of the given cluster

    Args:
      cluster_name: str:
      cluster_name: str:
      cluster_name: str:
      cluster_name: str:
      cluster_name: str:
      cluster_name: str:
      cluster_name: str:
      cluster_name: str:

    Returns:

    """
    master_ec2_instanceid = get_master_ec2_instance_id(cluster_name)
    print(f'Running "aws ssm start-session --target {master_ec2_instanceid}"')
    os.system(f"aws ssm start-session --target {master_ec2_instanceid}")


def ssm_bash(cmd):
    """

    Args:
      cmd:

    Returns:

    """

    emr_conf = load_config()
    instance_id = get_cluster_id(emr_conf["cluster-name"])

    ssm_client = boto3.client("ssm")
    response = ssm_client.send_command(
        InstanceIds=[instance_id],
        DocumentName="AWS-RunShellScript",
        Parameters={"commands": cmd},
    )

    return response


def cancel_step(cluster_name, step_id, step_name_pattern, state_pattern):
    """

    Args:
      cluster_name:
      step_id:
      step_name_pattern:
      state_pattern:

    Returns:

    """

    if step_id is None or step_id == "":
        step_id = get_last_submitted_step(
            cluster_name, step_name_pattern, state_pattern
        )

    cluster_id = get_cluster_id(cluster_name)
    boto3.client("emr")
    response = cancel_emr_step(cluster_id, step_id)

    return response


def list_steps(cluster_name, n, step_name_pattern, state_patterm):
    """List steps

    Args:
      cluster_name:
      n:
      step_name_pattern:
      state_patterm:

    Returns:

    """

    cluster_name = get_cluster_name(cluster_name)
    step_name_pattern = str(step_name_pattern)

    if "{env_name}" in step_name_pattern:
        step_name_pattern = step_name_pattern.format(env_name=get_env_name())

    logger.info(
        f"Listing steps on '{cluster_name}' matching name '{step_name_pattern}' in state '{state_patterm}'."
    )

    cluster_id = get_cluster_id(cluster_name)
    client = boto3.client("emr")
    response = client.list_steps(ClusterId=cluster_id)

    steps = pd.json_normalize(response["Steps"], sep="_").sort_values(
        "Status_Timeline_CreationDateTime", ascending=False
    )

    if step_name_pattern not in ["", "*", "None", "True"]:
        mateched_names = fnmatch.filter(steps.Name.tolist(), step_name_pattern)
        steps = steps[steps.Name.isin(mateched_names)]

    if state_patterm not in ["", "*", "None", None]:
        mateched_status_state = fnmatch.filter(
            steps.Status_State.astype(str).tolist(), str(state_patterm)
        )
        steps = steps[steps.Status_State.isin(mateched_status_state)]

    if n is not None or n != "":
        steps = steps.head(n)

    steps = steps[["Id", "Name", "Status_State", "Status_Timeline_CreationDateTime"]]
    return steps


def get_last_submitted_step(cluster_name, name_pattern, state):
    """

    Args:
      cluster_name:
      name_pattern:
      state:

    Returns:

    """

    steps = list_steps(cluster_name, None, name_pattern, state)

    if len(steps) > 0:
        step_id = steps["Id"].tolist()[0]
        print(f"Last submitted step '{step_id}'")
        return step_id

    if "{env_name}" in name_pattern:
        name_pattern = name_pattern.format(env_name=get_env_name())

    raise ValueError(
        f"No running steps for cluster_name='{cluster_name}' and name_pattern='{name_pattern}'"
    )


def describe_step(cluster_name, step_id, name_pattern, state):
    """

    Args:
      cluster_name:
      step_id:
      name_pattern:
      state:

    Returns:
    
    """
    
    if step_id is None or step_id == "":
        step_id = get_last_submitted_step(cluster_name, name_pattern, state)
    
    cluster_id = get_cluster_id(cluster_name)
    client = boto3.client("emr")
    response = client.describe_step(
        ClusterId=cluster_id,
        StepId=step_id,
    )
    return response


def get_failed_s3_log_file_path(cluster_name, step_id, name_pattern, state):
    """

    Args:
      cluster_name:
      step_id:
      name_pattern:
      state:

    Returns:

    """

    log_url = get_log_url(cluster_name)
    cluster_id = get_cluster_id(cluster_name)
    log_url = f"{log_url}{cluster_id}/steps/{step_id}"
    return log_url


import botocore


def download_s3_file(s3_path, out_dir):
    """

    Args:
      s3_path:
      out_dir:

    Returns:

    """

    _, _, bucket, key = s3_path.split("/", 3)
    file_name = key.split("/")[-1]

    s3_client = boto3.client("s3")

    pathlib.Path(out_dir).mkdir(parents=True, exist_ok=True)
    print(f"Downloading 's3://{bucket}/{key}' to '{out_dir}/{file_name}'")
    try:
        s3_client.download_file(bucket, key, f"{out_dir}/{file_name}")
    except botocore.exceptions.ClientError as e:
        if e.response["Error"]["Code"] == "404":
            raise ValueError(f"Object '{s3_path}' does not exists.")
        raise


def download_erm_step_log_gz(
    cluster_name, step_id, name_pattern, state, out_dir, log_type
):
    """

    Args:
      cluster_name:
      step_id:
      name_pattern:
      state:
      out_dir:
      log_type:

    Returns:

    """

    if step_id is None or step_id == "":
        step_id = get_last_submitted_step(cluster_name, name_pattern, state)

    s3_path = get_failed_s3_log_file_path(cluster_name, step_id, name_pattern, state)
    out_dir = f"{out_dir}/{step_id}"
    download_s3_file(f"{s3_path}/{log_type}.gz", out_dir)
    return f"{out_dir}/{log_type}.gz"







def get_application_id(local_stderr):
    """ """
    print('local_stderr',local_stderr)
    if os.path.exists(local_stderr):
        with gzip.open(local_stderr, "r") as f:
            stderr =  f.read().decode("utf-8")
    else:
        return None
    
    start = 'Application report for application_'
    end = ' (state: '
    ids = []
    
    for line in stderr.split("\n"):
        if start in line:
            line = line.split(start)[-1]
            if end in line:
                id = line.split(end)[0].strip()
                if id:
                    ids += [id]
    
    if len(ids)==0:
        return None
    
    id = max(ids,key=ids.count)
    return f'application_{id}'



def get_account_id():
    client = boto3.client("sts")
    account_id = client.get_caller_identity()["Account"]
    return account_id


def download_s3_folder(s3_path, local_dir=None):
    """
    Download the contents of a folder directory
    Args:
        bucket_name: the name of the s3 bucket
        s3_folder: the folder path in the s3 bucket
        local_dir: a relative or absolute directory path in the local file system
    """
    print(f"Downloading folder '{s3_path}' to '{local_dir}'.")
    _ , _, bucket_name, s3_folder = s3_path.split('/',3)
    
    s3 = boto3.resource('s3')
    
    bucket = s3.Bucket(bucket_name)
    for obj in bucket.objects.filter(Prefix=s3_folder):
        
        target = obj.key if local_dir is None \
            else os.path.join(local_dir, os.path.relpath(obj.key, s3_folder))
        if not os.path.exists(os.path.dirname(target)):
            os.makedirs(os.path.dirname(target))
        if obj.key[-1] == '/':
            continue
        bucket.download_file(obj.key, target)


def download_emr_master_logs(cluster_name, step_id, name_pattern, state, out_dir):
    
    if step_id is None or step_id == "":
        step_id = get_last_submitted_step(cluster_name, name_pattern, state)
    
    cluster_id = get_cluster_id(cluster_name)
    
    # download step logs
    log_url = get_log_url(cluster_name)
    step_logs = f"{log_url}{cluster_id}/steps/{step_id}/"
    out_dir = f"{out_dir}/{step_id}"
    pathlib.Path( out_dir ).mkdir(parents=True, exist_ok=True)
    download_s3_folder( step_logs, f"{out_dir}")
    return out_dir
    

def download_emr_logs(cluster_name, step_id, name_pattern, state, out_dir):
    
    download_emr_master_logs(cluster_name, step_id, name_pattern, state, out_dir)
    
    if step_id is None or step_id == "":
        step_id = get_last_submitted_step(cluster_name, name_pattern, state)
    
    cluster_id = get_cluster_id(cluster_name)

    # download step logs
    log_url = get_log_url(cluster_name)
    step_logs = f"{log_url}{cluster_id}/steps/{step_id}/"
    out_dir = f"{out_dir}/{step_id}"
    pathlib.Path( out_dir ).mkdir(parents=True, exist_ok=True)
    download_s3_folder( step_logs, f"{out_dir}")
    
    # download application logs
    local_stderr = f'{out_dir}/stderr.gz'
    app_id =  get_application_id(local_stderr)
    print('app_id',app_id)
    if app_id :
        app_logs  = f"{log_url}{cluster_id}/containers/{app_id}/"
        pathlib.Path(f"{out_dir}/{app_id}").mkdir(parents=True, exist_ok=True)
        download_s3_folder( app_logs, f"{out_dir}/{app_id}" )


def print_tail_gzip_files(in_path, n):
    """

    Args:
      in_path:
      n:

    Returns:

    """
    print(f"> tail -n {n} '{in_path}': ")
    print("\n")
    lines = []
    with gzip.open(in_path, "r") as fin:
        for line in fin:
            lines.append(line.decode("utf-8")[:-1])

    lines = lines[-n:]
    for line in lines:
        cprint(line, 'OKBLUE')
    print("\n")


def get_step_state(cluster_name, step_id, name_pattern, state):
    """

    Args:
      cluster_name:
      step_id:
      name_pattern:
      state:

    Returns:

    """
    desc = describe_step(cluster_name, step_id, name_pattern, "*")["Step"]
    print(f"Step {desc['Name']} is in state {desc['Status']['State']}.")


def print_emr_log_files_lines(
    log_type, n, step_id, cluster_name, name_pattern, state, out_dir
):
    """

    Args:
      log_type:
      n:
      step_id:
      cluster_name:
      name_pattern:
      state:
      out_dir:

    Returns:

    """
    
    out_dir = download_emr_master_logs(cluster_name, step_id, name_pattern, state, out_dir)
    print_tail_gzip_files(f"{out_dir}/{log_type}.gz", n)


