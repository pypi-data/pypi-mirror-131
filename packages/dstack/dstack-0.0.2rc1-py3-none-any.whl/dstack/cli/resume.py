import json
import sys
from argparse import Namespace

import colorama
import requests

from dstack.config import get_config, ConfigurationError


def resume_func(args: Namespace):
    try:
        dstack_config = get_config()
        # TODO: Support non-default profiles
        profile = dstack_config.get_profile("default")
        headers = {
            "Content-Type": f"application/json; charset=utf-8"
        }
        if profile.token is not None:
            headers["Authorization"] = f"Bearer {profile.token}"
        data = {"job_id": args.job_id}
        response = requests.request(method="POST", url=f"{profile.server}/jobs/resume",
                                    data=json.dumps(data).encode("utf-8"),
                                    headers=headers, verify=profile.verify)
        if response.status_code == 404:
            sys.exit(f"The '{args.job_id}' job is found")
        elif response.status_code == 400 and response.json()["message"] == "other jobs depend on it":
            sys.exit(f"The job cannot be resumed because other jobs depend on it")
        elif response.status_code == 400 and response.json()["message"] == "job is not stopped":
            sys.exit(f"The '{args.job_id}' job is not stopped")
        elif response.status_code != 200:
            response.raise_for_status()
        else:
            print(f"{colorama.Fore.LIGHTBLACK_EX}OK{colorama.Fore.RESET}")
    except ConfigurationError:
        sys.exit(f"Call 'dstack login' first")


def register_parsers(main_subparsers):
    parser = main_subparsers.add_parser("resume", help="Resume a stopped job")

    parser.add_argument('job_id', metavar='JOB', type=str)

    parser.set_defaults(func=resume_func)
