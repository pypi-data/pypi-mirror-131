"""A collection of aws tools"""
import os
import subprocess
from os.path import abspath, dirname

from .config import cprint, get_package_dir

# docker run -it --mount src="$(pwd)",target=/app,type=bind --entrypoint=python3 $(docker build -q .)
# docker run --rm -it --entrypoint bash -p 8889:8889 --mount src="$(pwd)",target=/local_dir,type=bind 280b97f7dfc5

# cd /local_dir jupyter notebook --ip 0.0.0.0 --no-browser --allow-root --port 8889

AMAZON_LINUX_DOCKER_TAG = "pyemr/amazonlinux:latest"
AMAZON_LINUX_DOCKER_FILE = "amazonlinux.Dockerfile"

# docker run -it --mount src="$(pwd)",target=/app,type=bind --entrypoint python3 pyemr/amazonlinux:latest
# docker run -it --mount src="$(pwd)",target=/app,type=bind --entrypoint bash --cmd python pyemr/amazonlinux:latest

def launch_docker_notebook():
    """ """
    docker_build(AMAZON_LINUX_DOCKER_FILE, AMAZON_LINUX_DOCKER_TAG)
    docker_run_sh(
        AMAZON_LINUX_DOCKER_TAG, "$(pwd)", "/run_notebook.sh", it=True, p="8889:8889"
    )


def launch_docker_python(*args, **kwards):
    """

    Args:
      *args:
      **kwards:

    Returns:

    """
    args = " ".join(args)
    kwards = " ".join(["-{k} {v}" for k, v in kwards.items()])
    docker_build(AMAZON_LINUX_DOCKER_FILE, AMAZON_LINUX_DOCKER_TAG)
    docker_run_sh(
        AMAZON_LINUX_DOCKER_TAG, "$(pwd)", f"/run_python.sh {kwards} {args}", it=True
    )


def launch_docker_shell():
    """ """
    docker_build(AMAZON_LINUX_DOCKER_FILE, AMAZON_LINUX_DOCKER_TAG)
    docker_run_sh(AMAZON_LINUX_DOCKER_TAG, "$(pwd)", "", it=True)


def launch_docker_bash():
    """ """
    docker_build(AMAZON_LINUX_DOCKER_FILE, AMAZON_LINUX_DOCKER_TAG)
    docker_run_sh(AMAZON_LINUX_DOCKER_TAG, "$(pwd)", "", it=True, entry_point="bash")


def launch_pyspark():
    """ """
    docker_build(AMAZON_LINUX_DOCKER_FILE, AMAZON_LINUX_DOCKER_TAG)
    docker_run_sh(
        AMAZON_LINUX_DOCKER_TAG, "$(pwd)", "/run_pyspark.sh", it=True, p="8889:8889"
    )



def local_spark_submit(script):
    """

    Args:
      script:

    Returns:

    """
    docker_build(AMAZON_LINUX_DOCKER_FILE, AMAZON_LINUX_DOCKER_TAG)
    docker_run_sh(
        AMAZON_LINUX_DOCKER_TAG,
        "$(pwd)",
        f"/spark_submit.sh {script}",
        it=True,
        p="8889:8889",
    )


def get_project_docker_dir():
    """ """
    package_root = get_package_dir()
    docker_dir = f"{package_root}/docker/"
    return docker_dir


def is_docker_build(tag_name):
    """

    Args:
      tag_name:

    Returns:

    """
    try:
        subprocess.check_output(["docker", "inspect", "--type=image", tag_name])
        return True
    except subprocess.CalledProcessError as e:
        return False


def docker_build(dockerfile, tag_name):
    """

    Args:
      docker_dir:
      dockerfile:
      tag_name:

    Returns:

    """
    docker_dir = get_project_docker_dir()

    print(f"Building emr docker image '{dockerfile}'...")

    if is_docker_build(tag_name) == False:
        cprint(
            f"WARNING:This is the first time you using pyemr or '{dockerfile}'. It might take ~5 minutes."
        )

    build = f"docker build -t {tag_name} --file {dockerfile} ."
    os.system(f"cd {docker_dir}; {build}")


def docker_run_sh(tag_name, mount_dir, sh_cmd="", it=False, p=None, entry_point="sh"):
    """

    Args:
      tag_name:
      mount_dir:
      sh_cmd: (Default value = '')
      it: (Default value = False)
      p: (Default value = None)
      entry_point: (Default value = 'sh')

    Returns:

    """

    mount = f'src="{mount_dir}",target=/app,type=bind'
    cmd = ["docker", "run", "--mount", mount]
    if it:
        cmd.append("-it")

    if p is not None:
        cmd += ["-p", p]

    cmd += [tag_name, entry_point, sh_cmd]
    cmd = " ".join(cmd)
    print(f"Running '{cmd}': \n")
    os.system(cmd)
