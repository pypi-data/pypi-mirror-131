"""A set of tools for manipulating project toml files"""
import os
import os.path
import subprocess
from os.path import abspath, dirname

# import awswrangler as wr
from typing import Dict

import tomlkit

REQUIRED_PARAM = ["s3-staging-dir", "cluster-name", "stage", "region"]

DEFAULT_CONFIG_TEMPLATE = {
    "cluster-name": "EDA",
    "s3-staging-dir": "s3://<bucket-name>/<your-staging-directory>",
    "stage": "dev",
    "date-time": "%Y-%m-%dT%H-%M-%S",
    "region": "eu-west-1",
}

DEFAULT_DEPENDENCIES = dict(
    Cython="0.29.24",
    pybind11="1.0.0",
    pythran="0.10.0",
    scipy="^1.2.0",
    Pillow="6.2.0",
    koalas="^1.8.2",
)

GIT_IGNORE_PATTERNS = [
    ".DS_Store",
    "**/.DS_Store",
    ".docker_venv",
    "**/docker_venv",
]

SIMPLE_KOALAS_EXAMPLE = """
import pandas as pd
import numpy as np
import databricks.koalas as ks
from pyspark.sql import SparkSession

kdf = ks.DataFrame(
{'a': [1, 2, 3, 4, 5, 6],
 'b': [100, 200, 300, 400, 500, 600],
 'c': ["one", "two", "three", "four", "five", "six"]},
index=[10, 20, 30, 40, 50, 60])

print(kdf.head())
""".strip()


def get_package_dir():
    """ """
    return dirname(dirname(abspath(__file__)))


def append_git_ignore(git_ignore_path=".gitignore"):
    """

    Args:
      git_ignore_path: (Default value = '.gitignore')

    Returns:

    """

    with open(git_ignore_path, "r") as f:
        git_ignore = f.read()

    git_ignore = git_ignore.split("\n")
    for pattern in GIT_IGNORE_PATTERNS:
        if pattern not in git_ignore:
            git_ignore.append(pattern)

    with open(git_ignore_path, "w") as f:
        f.write("\n".join(git_ignore))


def create_git_ignore(git_ignore_path=".gitignore"):
    """

    Args:
      git_ignore_path: (Default value = '.gitignore')

    Returns:

    """
    if not os.path.isfile(git_ignore_path):
        with open(git_ignore_path, "w") as f:
            f.write("\n".join(GIT_IGNORE_PATTERNS))
    else:
        append_git_ignore(git_ignore_path)


def get_cluster_name(cluster_name):
    """

    Args:
      cluster_name:

    Returns:

    """
    emr_conf = load_config()
    if cluster_name in ["", None, "None"]:
        cluster_name = emr_conf["cluster-name"]
    return cluster_name


def get_version():
    """ """
    config = _get_pyproject_toml()
    return config["tool"]["poetry"]["version"]


def get_s3_staging_dir():
    """ """
    emr_conf = load_config()
    s3_stage_dir = emr_conf["s3-staging-dir"]
    if s3_stage_dir.endswith("/"):
        s3_stage_dir = s3_stage_dir[:-1]
    return s3_stage_dir


def get_project_name():
    """ """
    proj_config = _get_pyproject_toml()
    project_name = proj_config["tool"]["poetry"]["name"]
    return project_name


def get_env_name():
    """ """
    conf = load_config()
    project_name = get_project_name()
    env_name = project_name.replace(" ", "_").lower()
    version = str(get_version()).replace(".", "_").lower()
    version = str(get_version()).replace(".", "_").lower()
    return f"{env_name}_{conf['stage']}_{version}"


def get_build_name():
    """Get the project name"""
    project_name = get_env_name()
    return f"{project_name}.tar.gz"


def get_project_type():
    """Get the type of project. e.g. poetry."""
    if os.path.isfile("./pyproject.toml"):
        return "poetry"

    raise ValueError('No "./pyproject.toml" found.')


def _pyproject_toml_exists(pyproj_path: str = "./pyproject.toml"):
    """

    Args:
      pyproj_path: str:  (Default value = "./pyproject.toml")
      pyproj_path: str:  (Default value = "./pyproject.toml")
      pyproj_path: str:  (Default value = "./pyproject.toml")
      pyproj_path: str:  (Default value = "./pyproject.toml")
      pyproj_path: str:  (Default value = "./pyproject.toml")
      pyproj_path: str:  (Default value = "./pyproject.toml")
      pyproj_path: str:  (Default value = "./pyproject.toml")
      pyproj_path: str:  (Default value = "./pyproject.toml")
      pyproj_path: str:  (Default value = "./pyproject.toml")
      pyproj_path: str:  (Default value = "./pyproject.toml")
      pyproj_path: str:  (Default value = "./pyproject.toml")
      pyproj_path: str:  (Default value = "./pyproject.toml")
      pyproj_path: str:  (Default value = "./pyproject.toml")
      pyproj_path: str:  (Default value = "./pyproject.toml")
      pyproj_path: str:  (Default value = "./pyproject.toml")
      pyproj_path: str:  (Default value = "./pyproject.toml")
      pyproj_path: str:  (Default value = "./pyproject.toml")

    Returns:

    """
    return os.path.isfile(pyproj_path)


def _get_pyproject_toml(pyproj_path: str = "./pyproject.toml") -> Dict[str, str]:
    """Loads the pyproject toml file as a dict.

    Args:
      pyproj_path: str:  (Default value = "./pyproject.toml")
      pyproj_path: str:  (Default value = "./pyproject.toml")
      pyproj_path: str:  (Default value = "./pyproject.toml")
      pyproj_path: str:  (Default value = "./pyproject.toml")
      pyproj_path: str:  (Default value = "./pyproject.toml")
      pyproj_path: str:  (Default value = "./pyproject.toml")
      pyproj_path: str:  (Default value = "./pyproject.toml")
      pyproj_path: str:  (Default value = "./pyproject.toml")
      pyproj_path: str:  (Default value = "./pyproject.toml")
      pyproj_path: str:  (Default value = "./pyproject.toml")
      pyproj_path: str:  (Default value = "./pyproject.toml")
      pyproj_path: str:  (Default value = "./pyproject.toml")
      pyproj_path: str:  (Default value = "./pyproject.toml")
      pyproj_path: str:  (Default value = "./pyproject.toml")
      pyproj_path: str:  (Default value = "./pyproject.toml")
      pyproj_path: str:  (Default value = "./pyproject.toml")
      pyproj_path: str:  (Default value = "./pyproject.toml")
      pyproj_path: str:  (Default value = "./pyproject.toml")

    Returns:

    """

    if _pyproject_toml_exists(pyproj_path):
        with open(pyproj_path, "r", encoding="utf8") as pyproject:
            file_contents = pyproject.read()
        return tomlkit.parse(file_contents)
    else:
        raise ValueError(f"'{pyproj_path}' does not exists. Run 'pyemr init'.")

    return {}


def _write_pyproject_toml(file_contents: dict, pyproj_path: str = "./pyproject.toml"):
    """Writes a dict into a toml file

    Args:
      file_contents: dict:
      pyproj_path: str:  (Default value = "./pyproject.toml")
      file_contents: dict:
      pyproj_path: str:  (Default value = "./pyproject.toml")
      file_contents: dict:
      pyproj_path: str:  (Default value = "./pyproject.toml")
      file_contents: dict:
      pyproj_path: str:  (Default value = "./pyproject.toml")
      file_contents: dict:
      pyproj_path: str:  (Default value = "./pyproject.toml")
      file_contents: dict:
      pyproj_path: str:  (Default value = "./pyproject.toml")
      file_contents: dict:
      pyproj_path: str:  (Default value = "./pyproject.toml")
      file_contents: dict:
      pyproj_path: str:  (Default value = "./pyproject.toml")
      file_contents: dict:
      pyproj_path: str:  (Default value = "./pyproject.toml")
      file_contents: dict:
      pyproj_path: str:  (Default value = "./pyproject.toml")
      file_contents: dict:
      pyproj_path: str:  (Default value = "./pyproject.toml")
      file_contents: dict:
      pyproj_path: str:  (Default value = "./pyproject.toml")
      file_contents: dict:
      pyproj_path: str:  (Default value = "./pyproject.toml")
      file_contents: dict:
      pyproj_path: str:  (Default value = "./pyproject.toml")
      file_contents: dict:
      pyproj_path: str:  (Default value = "./pyproject.toml")
      file_contents: dict:
      pyproj_path: str:  (Default value = "./pyproject.toml")
      file_contents: dict:
      pyproj_path: str:  (Default value = "./pyproject.toml")
      file_contents: dict:
      pyproj_path: str:  (Default value = "./pyproject.toml")

    Returns:

    """
    with open(pyproj_path, "w", encoding="utf8") as pyproject:
        pyproject.write(tomlkit.dumps(file_contents))


def load_config():
    """Loads the config parameters from the project toml file."""
    tml = _get_pyproject_toml()
    return tml["tool"]["pyemr"]


def _update_git_ignore():
    """ """
    pass


def set_param(key, value):
    """

    Args:
      key:
      value:

    Returns:

    """

    tml = _get_pyproject_toml()

    if "tool" not in tml:
        tml["tool"] = {}

    if "pyemr" not in tml["tool"]:
        tml["tool"]["pyemr"] = {}

    tml[key] = value
    _write_pyproject_toml(tml)


STDOUT_COLORS = dict(
    HEADER="\033[95m",
    OKBLUE="\033[94m",
    OKCYAN="\033[96m",
    OKGREEN="\033[92m",
    WARNING="\033[93m",
    FAIL="\033[91m",
    ENDC="\033[0m",
    BOLD="\033[1m",
    UNDERLINE="\033[4m",
)


def color_text(text, style="OKCYAN"):
    """

    Args:
      text:
      style: (Default value = 'OKCYAN')

    Returns:

    """
    return f"{STDOUT_COLORS[style]}{text}{STDOUT_COLORS['ENDC']}"


def cinput(variable_name, default):
    """

    Args:
      variable_name:
      default:

    Returns:

    """
    prompt = color_text(variable_name, "OKCYAN")
    prompt += color_text(" [", "OKCYAN")
    prompt += color_text(str(default), "OKGREEN")
    prompt += color_text("]", "OKCYAN")

    print(prompt, end="")
    value = input() or default
    print(value)
    return value


def cprint(text, color="OKCYAN"):
    """

    Args:
      text:
      color: (Default value = 'OKCYAN')

    Returns:

    """
    return print(color_text(text, color))


def init_pyemr_param(cluster_name, s3_stage_dir, stage, region):
    """Append EMR pack aparameters to the project toml

    Args:
      cluster_name:
      stage_dir:
      s3_stage_dir:
      stage:
      region:

    Returns:

    """

    tml = _get_pyproject_toml()

    if "tool" not in tml:
        tml["tool"] = {}

    if "pyemr" not in tml["tool"]:
        tml["tool"]["pyemr"] = {}

    if cluster_name:
        tml["tool"]["pyemr"]["cluster-name"] = cluster_name

    if s3_stage_dir:
        tml["tool"]["pyemr"]["s3-staging-dir"] = s3_stage_dir

    if stage:
        tml["tool"]["pyemr"]["stage"] = stage

    if region:
        tml["tool"]["pyemr"]["region"] = region

    for variable_name, default_value in DEFAULT_CONFIG_TEMPLATE.items():
        if variable_name not in tml["tool"]["pyemr"]:
            if variable_name in REQUIRED_PARAM:
                value = cinput(variable_name, default_value)
            else:
                value = default_value
            tml["tool"]["pyemr"][variable_name] = value

    print("[tool.pyemr]")
    print(tomlkit.dumps(tml["tool"]["pyemr"]))

    _write_pyproject_toml(tml)
    return True


def add_dependencies(dep):
    """

    Args:
      dep:

    Returns:

    """
    tml = _get_pyproject_toml()
    tml["tool"]["poetry"]["dependencies"].update(dep)
    _write_pyproject_toml(tml)


def add_packages_to_toml(package_path):
    """

    Args:
      package_path:

    Returns:

    """

    package_obj = tomlkit.inline_table()
    tml = _get_pyproject_toml()
    package_obj["include"] = package_path
    if "packages" not in tml["tool"]["poetry"]:
        tml["tool"]["poetry"]["packages"] = []

    tml["tool"]["poetry"]["packages"].append(package_obj)
    _write_pyproject_toml(tml)


def add_pyemr_param(key, value):
    """

    Args:
      key:
      value:

    Returns:

    """
    tml = _get_pyproject_toml()

    if "tool" not in tml:
        tml["tool"] = {}

    if "pyemr" not in tml["tool"]:
        tml["tool"]["pyemr"] = {}

    tml["tool"]["pyemr"][key] = value
    _write_pyproject_toml(tml)


def create_koalas_example(out_path):
    """

    Args:
      out_path:

    Returns:

    """
    with open(f"{out_path}/script.py", "w") as f:
        f.write(SIMPLE_KOALAS_EXAMPLE.strip())


def add_main_package():
    """ """
    tml = _get_pyproject_toml()
    name = tml["tool"]["poetry"]["name"]
    package_path = name.replace(" ", "_").lower()
    os.system(f"mkdir {package_path}")
    create_koalas_example(package_path)
    add_packages_to_toml(package_path)


def add_scr_package():
    """ """
    package_path = "src"
    os.system(f"mkdir {package_path}")
    create_koalas_example(package_path)
    add_packages_to_toml(package_path)


def init_pyemr(project_name, cluster_name, s3_stage_dir, stage, region):
    """

    Args:
      cluster_name:
      stage_dir:
      project_name:
      s3_stage_dir:
      stage:
      region:

    Returns:

    """

    dep = [
        f"--dependency={name}={version}"
        for name, version in DEFAULT_DEPENDENCIES.items()
    ]

    if not _pyproject_toml_exists():
        if project_name is None or project_name == "":
            project_name = cinput("Project Name", "tmp")
        args = [
            "poetry",
            "init",
            "--python=>=3.7,<3.10",
            "-n",
            "--name",
            project_name,
            "--quiet",
        ] + dep
        proc = subprocess.Popen(args)
        proc.communicate()

    # install default dependencies
    # add_dependencies(DEFAULT_DEPENDENCIES)
    add_scr_package()
    init_pyemr_param(cluster_name, s3_stage_dir, stage, region)
    create_git_ignore()
    os.system("open pyproject.toml")


"""
    --project_name=PROJECT_NAME
        Default: ''
    --cluster_name=CLUSTER_NAME
        Default: ''
        (Default value = '')
    --s3_stage_dir=S3_STAGE_DIR
        Default: ''
    --stage=STAGE
        Default: ''
    --region=REGION
        Default: ''
"""
