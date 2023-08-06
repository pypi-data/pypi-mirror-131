# pylint: disable=R0201
"""Command Line Interface"""

import os
from pprint import pprint

# import awswrangler as wr
from subprocess import check_output

import fire

from .utils.aws import (
    cancel_step,
    describe_cluster,
    describe_step,
    get_step_state,
    list_steps,
    print_emr_log_files_lines,
    ssm_cluster,
    download_emr_logs
)
from .utils.build import (
    build,
    pack_poetry_project_in_docker,
    submit_spark_step,
    upload_amazonlinux_build_s3,
    upload_file_s3,
)
from .utils.config import add_pyemr_param, init_pyemr
from .utils.docker import (
    launch_docker_bash,
    launch_docker_notebook,
    launch_docker_python,
    launch_docker_shell,
    launch_pyspark,
    local_spark_submit,
)
from .utils.emr import get_clusters_list_df


class Cli:
    """Command line interface for the package."""

    def init(
        self, project_name="", target_cluster="", s3_stage_dir="", stage="", region=""
    ):
        """Create a pyproject.toml containing pyemr config.

        Args:
          cluster_name: (Default value = '')
          stage_dir: (Default value = '')
          project_name: (Default value = '')
          target_cluster: (Default value = "")
          s3_stage_dir: (Default value = "")
          stage: (Default value = '')
          region: (Default value = '')

        Returns:

        """
        init_pyemr(project_name, target_cluster, s3_stage_dir, stage, region)

    def ssh(self, cluster_name=""):
        """A proxy name for ssm.

        Args:
          cluster_name: (Default value = "")

        Returns:

        """
        self.ssm(cluster_name)

    def ssm(self, cluster_name=""):
        """smm into the cluster master node.

        Args:
          cluster_name: (Default value = "")

        Returns:

        """
        ssm_cluster(cluster_name)

    def ssmbash(self, cluster_name, cmd):
        """run a command on a cluster master node

        Args:
          cluster_name:
          cmd:

        Returns:

        """
        # ssm_bash(cluster_name, cmd)

    def build(self, cluster_name=""):
        """Zips the python package and dependencies and then uploads them s3 staging directory.

        Args:
          cluster_name: (Default value = "")

        Returns:

        """
        build(cluster_name)

    def install(self, cluster_name=""):
        """

        Args:
          cluster_name: (Default value = "")

        Returns:

        """
        self.build(cluster_name)

    def submit(
        self, script, submit_mode="client", cluster_name="", wait=True, **kwargs
    ):
        """

        Args:
          script:
          submit_mode: (Default value = 'client')
          cluster_name: (Default value = '')
          wait: (Default value = True)
          *args:
          **kwargs:

        Returns:

        """
        submit_spark_step(script, submit_mode, cluster_name, wait, **kwargs)

    def config(self, toml_path="pyproject.toml"):
        """

        Args:
          toml_path: (Default value = "./pyproject.toml")

        Returns:

        """
        input_dir = os.getcwd()
        check_output(["open", f"{input_dir}/{toml_path}"])

    def docker_build(self):
        """ """
        pack_poetry_project_in_docker()

    def upload_build(self):
        """ """
        print(upload_amazonlinux_build_s3())

    def bsubmit(self, location="s3"):
        """

        Args:
          location: (Default value = "s3")

        Returns:

        """
        self.buildsubmit(location)

    def notebook():
        """Starts a spark linux notebook in current directory"""

    def pyspark(self):
        """Starts a pyspark session in doker with the current director booted."""

    def export(self, type):
        """

        Args:
          type:

        Returns:

        """
        assert type in ["aws", "bash", "python", "airflow", "awswrangler"]
    

    def s3(self, cmd):
        """

        Args:
          cmd:

        Returns:

        """

    def list_steps(
        self, cluster_name="", n=10, step_name="{env_name}:*", states="*", all=False
    ):
        """

        Args:
          cluster_name: (Default value = "")
          n: (Default value = 10)
          step_name: (Default value = "*{env_name}*")
          states: (Default value = '*')
          all: (Default value = False)

        Returns:

        """
        if all:
            step_name = states = "*"
        pprint(list_steps(cluster_name, n, step_name, states))

    def cancel_step(
        self, step_id="", cluster_name="", step_name_pattern="{env_name}:*", state="*"
    ):
        """

        Args:
          step_id: (Default value = "")
          cluster_name: (Default value = "")
          step_name_pattern: (Default value = "*{env_name}*")
          state: (Default value = "*")

        Returns:

        """
        pprint(cancel_step(cluster_name, step_id, step_name_pattern, state))

    def describe_step(
        self, step_id="", cluster_name="", name="{env_name}:*", state="*"
    ):
        """

        Args:
          step_id: (Default value = "")
          cluster_name: (Default value = "")
          name: (Default value = "*{env_name}*")
          state: (Default value = "*")

        Returns:

        """
        pprint(describe_step(cluster_name, step_id, name, state))
    
    def logs(
        self,
        log_type,
        step_id="",
        n=30,
        cluster_name="",
        name="*{env_name}*",
        state="*",
        out_dir="logs",
    ):
        """

        Args:
          log_type:
          step_id: (Default value = "")
          n: (Default value = 30)
          cluster_name: (Default value = "")
          name: (Default value = "*{env_name}*")
          state: (Default value = "*")
          out_dir: (Default value = "./logs")

        Returns:

        """
        print_emr_log_files_lines(
            log_type, n, step_id, cluster_name, name, state, out_dir
        )
        # shutil.rmtree(out_dir)

    def stderr(
        self,
        step_id="",
        n=30,
        cluster_name="",
        name="*{env_name}*",
        state="*",
        out_dir="logs",
    ):
        """

        Args:
          step_id: (Default value = "")
          n: (Default value = 30)
          cluster_name: (Default value = "")
          name: (Default value = "*{env_name}*")
          state: (Default value = "*")
          out_dir: (Default value = "./logs")

        Returns:

        """
        self.logs("stderr", step_id, n, cluster_name, name, state, out_dir)

    def stdout(
        self,
        step_id="",
        n=30,
        cluster_name="",
        name="*{env_name}*",
        state="*",
        out_dir="logs",
    ):
        """

        Args:
          step_id: (Default value = "")
          n: (Default value = 30)
          cluster_name: (Default value = "")
          name: (Default value = "*{env_name}*")
          state: (Default value = "*")
          out_dir: (Default value = "./logs")

        Returns:

        """
        self.logs("stdout", step_id, n, cluster_name, name, state, out_dir)

    def state(self, step_id="", cluster_name="", name="*{env_name}*", state="*"):
        """

        Args:
          step_id: (Default value = "")
          cluster_name: (Default value = "")
          name: (Default value = "*{env_name}*")
          state: (Default value = "*")

        Returns:

        """
        get_step_state(cluster_name, step_id, name, state)

    def describe_cluster(self, cluster_name=""):
        """

        Args:
          cluster_name: (Default value = "")

        Returns:

        """
        pprint(describe_cluster(cluster_name))

    def list_clusters(self, states=["RUNNING", "WAITING"], n=10):
        """

        Args:
          states: (Default value = ['RUNNING')
          'WAITING']:
          n: (Default value = 10)
          "WAITING"]:

        Returns:

        """
        print(get_clusters_list_df(states, n))

    def ls(
        self,
        entity_type,
        step_name_pattern="*{env_name}*",
        states=["RUNNING", "WAITING"],
        n=10,
        *args,
        **kwards,
    ):
        """

        Args:
          entity_type:
          step_name_pattern: (Default value = "*{env_name}*")
          states: (Default value = ['RUNNING')
          'WAITING']:
          n: (Default value = 10)
          *args:
          **kwards:
          "WAITING"]:

        Returns:

        """

        if entity_type in "clusters":
            self.list_clusters(*args, **kwards)
        if entity_type in "steps":
            self.list_steps(*args, **kwards)

    def s3_cp(self, local_path, out_dir="."):
        """

        Args:
          local_path:
          out_dir: (Default value = '.')

        Returns:

        """
        print(upload_file_s3(local_path, out_dir))

    def set(self, key, value):
        """

        Args:
          key:
          value:

        Returns:

        """
        add_pyemr_param(key, value)

    def notebook(self):
        """ """
        launch_docker_notebook()

    def python(self, *args, **kwards):
        """

        Args:
          *args:
          **kwards:

        Returns:

        """
        launch_docker_python(*args, **kwards)

    def sh(self):
        """ """
        launch_docker_shell()

    def bash(self):
        """ """
        launch_docker_bash()

    def pyspark(self):
        """ """
        launch_pyspark()

    def test(self, script):
        """

        Args:
          script:

        Returns:

        """
        local_spark_submit(script)

    def export(self, *args):
        """

        Args:
          *args:

        Returns:

        """
        raise ValueError("This features is not available yet.")
    
    def download_logs(
            self,
            out_dir="logs",
            step_id="",
            cluster_name="",
            name="*{env_name}*",
            state="*",
        ):
        return download_emr_logs(cluster_name, step_id, name, state, out_dir)


def main():
    """ """
    fire.Fire(Cli)


if __name__ == "__main__":
    main()
