import urllib.parse
import functools


def url_join(*args):
    args = list(args)
    # Ensure trailing slash behind
    for index, arg in enumerate(args):
        if arg[-1:] != "/":
            args[index] = arg + "/"

    return functools.reduce(urllib.parse.urljoin, args).rstrip("/")
