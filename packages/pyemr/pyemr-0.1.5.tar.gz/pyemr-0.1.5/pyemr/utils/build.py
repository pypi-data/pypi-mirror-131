"""Tools for packaging poetry projects"""
import glob
import os
import os.path
import subprocess
from datetime import datetime
from os.path import abspath, dirname

# import awswrangler as wr
from subprocess import check_output

import awswrangler as wr
from loguru import logger

from .aws import get_cluster_id, get_file_s3_path, upload_to_s3_stage
from .config import (
    _get_pyproject_toml,
    add_pyemr_param,
    cprint,
    get_build_name,
    get_cluster_name,
    get_env_name,
    get_package_dir,
    get_project_name,
    get_project_type,
    get_version,
    load_config,
)
from .docker import docker_build, docker_run_sh, is_docker_build
from .emr import wait_else_cancel


def get_datetime_string():
    """Returns the datetime string based on project config"""

    conf = load_config()
    if conf["date-time"] == "now":
        return datetime.now().strftime("%Y-%m-%dT%H-%M-%S")
    if conf["date-time"] == "today":
        return datetime.now().strftime("%Y-%m-%d")
    if conf["date-time"] == "latest":
        return "latest"
    if "%" in conf["date-time"]:
        return datetime.now().strftime(conf["date-time"])

    return None


def get_local_build_path(prefix=None):
    """

    Args:
      prefix: (Default value = None)

    Returns:

    """
    env_name = get_build_name()
    if prefix is None:
        out_path = f"dist/{env_name}"
    else:
        out_path = f"dist/{env_name}"
    return out_path


def get_client_mode_runner_path():
    """ """
    package_dir = get_package_dir()
    return "{package_dir}/utils/client_mode_runner.sh"


def pack_poetry_project_in_docker():
    """Creates a pack file from the poetry project in the currently directory."""

    docker_file = "amazonlinux.Dockerfile"
    tag_name = "pyemr/amazonlinux:latest"
    conf = load_config()
    input_dir = os.getcwd()
    local_build_path = get_local_build_path("amazonlinux")

    # build the docker image
    docker_build(docker_file, tag_name)

    # run van-pack inside container
    print(f"Building package inside docker container '{docker_file}'")
    sh_cmd = f"/build.sh {local_build_path}"
    docker_run_sh(tag_name, input_dir, sh_cmd)

    return local_build_path


def upload_amazonlinux_build_s3(build_path=None):
    """

    Args:
      build_path: (Default value = None)

    Returns:

    """
    if build_path is None:
        build_path = get_local_build_path("amazonlinux")
    s3_build_path = upload_file_s3(build_path, out_dir="code")
    return s3_build_path


def get_amazonlinux_build_path_s3():
    """ """
    build_path = get_local_build_path("amazonlinux")
    s3_build_path = get_file_s3_path(build_path, "latest", "code")
    return s3_build_path


def upload_file_s3(local_path, out_dir=""):
    """

    Args:
      local_path:
      out_dir: (Default value = '')

    Returns:

    """
    date_time = get_datetime_string()
    s3_path = upload_to_s3_stage(local_path, date_time, out_dir)
    return s3_path


def most_recent(patterm):
    """

    Args:
      patterm:

    Returns:

    """
    list_of_files = glob.glob(patterm)  # * means all if need specific format then *.csv
    latest_file = max(list_of_files, key=os.path.getctime)
    return latest_file


def build(cluster_name):
    """Build the project using pack then uploads it to s3.

    Args:
      location: (Default value = "s3")
      cluster_name:

    Returns:

    """

    build_path = pack_poetry_project_in_docker()
    s3_build_path = upload_amazonlinux_build_s3(build_path)
    add_pyemr_param("latest_build", s3_build_path)
    return s3_build_path


def get_client_mode_runner_path():
    """ """
    package_root = dirname(dirname(abspath(__file__)))
    return f"{package_root}/utils/client_mode_runner.sh"


def upload_client_mode_runner_to_s3():
    """ """
    client_runner_path = get_client_mode_runner_path()
    return upload_to_s3_stage(client_runner_path, "latest", "code")


# TODO:
# finish submit command
#      test build and run. make
# update docs + howto guide
# notebook docker command

## TODO: convert from bash to python
# cluster mode

SPARK_SUBMIT_CMD_CLUSTER = """
sudo spark-submit \
--conf spark.yarn.appMasterEnv.PYSPARK_PYTHON=./env/bin/python3 \
--conf spark.yarn.dist.archives={s3_build_path}#env \
--master yarn \
--deploy-mode cluster \
{s3_script_path} \
{kwargs)
"""

SPARK_SUBMIT_CMD_CLIENT = """
sudo PYARROW_IGNORE_TIMEZONE=1 \
PYSPARK_DRIVER_PYTHON=./env/bin/python3 \
PYSPARK_PYTHON=./env/bin/python3 \
spark-submit \
--deploy-mode client \
{s3_script_path} \
{kwargs}
"""


def submit_spark_step(
    local_script_path, submit_mode, cluster_name, wait=True, **kwargs
):
    """

    Args:
      local_script_path:
      submit_mode:
      cluster_name:
      wait: (Default value = True)
      **kwargs:

    Returns:

    """

    kwargs = " ".join([f"--{k}={v}" for k, v in kwargs.items()])

    cluster_name = get_cluster_name(cluster_name)
    cluster_id = get_cluster_id(cluster_name)

    date_time = get_datetime_string()
    s3_script_path = upload_to_s3_stage(local_script_path, date_time, "code")
    script_name = local_script_path.split("/")[-1]

    s3_build_path = get_amazonlinux_build_path_s3()

    submit_mode = submit_mode.lower()

    if submit_mode == "client":
        client_runner_s3_path = upload_client_mode_runner_to_s3()
        spark_submit_cmd = SPARK_SUBMIT_CMD_CLIENT.strip().format(
            s3_script_path=s3_script_path, kwargs=kwargs
        )
        cmd = f"{client_runner_s3_path} {s3_build_path} {spark_submit_cmd}"
        script = True
    elif submit_mode == "cluster":
        spark_submit_cmd = SPARK_SUBMIT_CMD_CLUSTER.strip().format(
            s3_script_path=s3_script_path, s3_build_path=s3_build_path, kwargs=kwargs
        )
        cmd = spark_submit_cmd
        script = False
    else:
        raise ValueError(f"No spark submit mode called '{submit_mode}'.")

    env_name = get_env_name()
    step_name = f"{env_name}:spark-submit:{local_script_path}"

    step_id = wr.emr.submit_step(
        cluster_id=cluster_id,
        name=step_name,
        command=cmd,
        script=script,
    )

    print("")
    cprint(
        f"Running '{local_script_path}' on EMR cluster '{cluster_name}' in enviroment '{env_name}'"
    )

    if wait:
        wait_else_cancel(
            cluster_id,
            step_id,
        )

    return step_id
