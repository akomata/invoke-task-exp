import os
import platform

from invoke import task
from rich import print

from .task_util import multi_print as mp
from .task_util import pre_task

_ENV_VARS = {
    "PROJECT": [
        "PROJECT_ROOT",
        "PYTHONPATH",
    ],
    "AWS": [
        "AWS_PROFILE",
        "AWS_DEFAULT_PROFILE",
        "AWS_REGISON",
        "AWS_DEFAULT_REGION",
    ],
}


@task
def pre_requisites(c):
    """
    ** Todo: Not implemented yet.
    """
    pass


@task
@pre_task
def path(c):
    """
    Print PATH info.
    """
    print(os.getenv("PATH").split(":"))


# Todo: Refactor pre_task then this is not needed.
@task
def env_var(c, group="ALL"):
    """
    Print Environment variables related to the project.
      Args:
        group: PROJECT|AWS|ALL (default=ALL)
    """

    @pre_task
    def _env_var(c, group="ALL"):
        group = group.upper()
        all = group == "ALL"
        mp.header("Environment Variables", indent=c.indent)
        for g in _ENV_VARS:
            if all or g == group:
                mp(g, indent=c.indent + 1)
                for var in _ENV_VARS[g]:
                    mp(f"[b]{var}[/b]: {os.getenv(var, '')}", indent=c.indent + 2)

    _env_var(c, group)


@task
@pre_task
def python(c):
    """
    Print python runtime version
    """
    mp.header("Python version", indent=c.indent)
    mp(f"{platform.python_version()}", indent=c.indent + 1)


@task(pre=[env_var, python], default=True)
@pre_task
def all(c):
    """
    Check and print project environment info.
    """
    pass
