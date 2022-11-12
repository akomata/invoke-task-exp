from glob import glob
from importlib import import_module
from os.path import basename, dirname, isfile, join

from invoke import Collection

namespace = Collection()


def package_init():
    # list of modules which is not a real Invoke task
    not_a_real_task = ["__init__.py", "task_util.py"]

    # Dynamically load all the task modules
    modules = glob(join(dirname(__file__), "*.py"))

    # Add the just loaded modules to the Invoke namespace
    for f in modules:
        if not isfile(f) or basename(f) not in not_a_real_task:
            namespace.add_collection(import_module("." + basename(f)[:-3], "tasks"))


if __name__ == __package__:
    package_init()
