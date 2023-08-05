import importlib
import inspect
import os
import pprint
import socket
import sys

import click
import yaml

from pype import utils
from pype.log import get_logger
from pype.status import Status


@click.group()
def cli():
    pass


@cli.command()
@click.option("--tag", "-t", default="", help="only run configs with the tag")
@click.argument("config")
def run(config, tag):
    run_(config, tag)


def run_(config, tag, skip_done=False):
    if isinstance(config, str):
        config = yaml.load(open(config, "r"), Loader=yaml.FullLoader)

    if isinstance(config, list):
        for config_ in config:
            sys.stdout = sys.__stdout__
            sys.stderr = sys.__stderr__
            run_(config_, tag, skip_done=True)

    else:
        status = Status(config["job_dir"])
        if tag:
            if not tag in config.get("tag", ""):
                return

        if status.status == "Running" or status.status == "Done":
            if skip_done:
                print(
                    f"Skipping {config['job_id']} because status is {status.status} ... "
                )
                return
            if not permission_to_continue(f"Job is {status.status}."):
                print("job aborted")
                return

        run_job(config)


def run_job(config):
    job_dir = config["job_dir"]
    log_file = os.path.join(job_dir, "job.log")
    logger = get_logger(config["job_id"], log_file)
    status = Status(job_dir)

    msg = running_job_msg(config)
    logger.info(msg)
    utils.save_git_sha(job_dir)

    status.running()

    try:
        module = _import_module(config["script_path"])
        if not hasattr(module, "main"):
            raise RuntimeError(f"{config['script_path']} has no main function.")

        if 'logger' in inspect.getargspec(module.main).args:
            module.main(config, logger)
        else:
            module.main(config)
        status.done()
        logger.info("job terminated succesfully.")

    except Exception:  # pylint: disable=broad-except
        status.failed()
        logger.exception("Exception occurred: \n\n")


def running_job_msg(config):
    space = 4 * " "

    msg = f"Running job {config['job_id']}"
    hashs = (2 * len(space) + len(msg)) * "#" + ""

    full_msg = f"\n{hashs}\n{'    '+msg}\n{hashs}\n\n"
    full_msg += "Host: " + socket.gethostname() + "\n"
    full_msg += "PID: " + str(os.getpid()) + 2 * "\n"
    full_msg += "Configuration:\n"

    full_msg += pprint.pformat(config)
    length = max([len(l) for l in pprint.pformat(config).split("\n")])
    full_msg += 2 * "\n" + length * "_" + "\n"

    return full_msg


def permission_to_continue(msg):
    return input(msg + "Type 'y' or 'yes' to continue anyways\n").lower() in [
        "y",
        "yes",
    ]


def _import_module(path):
    spec = importlib.util.spec_from_file_location("module.name", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    return module


def _uncomitted():
    if not utils.GIT_CONTROL:
        return False

    cmd = r"git status | grep -q '\smodified:\s'"
    code = os.system(cmd)
    return code == 0
