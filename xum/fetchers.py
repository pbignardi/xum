import subprocess
from typing import List

from xum.config import config

registered_fetchers = []


def fetcher(func):
    "Register fetcher by adding it to `registered_fetchers` list"
    registered_fetchers.append(func)
    return func


@fetcher
def fd() -> List[str]:
    args = ["fd", "-d", "1", "-t", "d", "-t", "l"]
    for path in config.search_paths:
        args.extend(("--search-path", str(path)))

    return [x.strip() for x in subprocess.check_output(args, text=True).splitlines()]


@fetcher
def zoxide() -> List[str]:
    args = ("zoxide", "query", "--list")
    return [x.strip() for x in subprocess.check_output(args, text=True).splitlines()]
