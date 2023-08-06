"""A collection of aws tools"""
import os

import fire


def format_code():
    """ """
    os.system("pyment --output=google --write .")
    os.system(
        "autoflake --in-place --remove-unused-variables --remove-all-unused-imports **/*.py"
    )
    os.system("isort .")
    os.system("black .")


if __name__ == "__main__":
    fire.Fire(format_code)
