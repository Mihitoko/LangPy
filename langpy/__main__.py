import logging
import os
import sys

from langpy.jobs import compile_job, init, new_template
from langpy.meta import __version__, __author__, __github__


if __name__ == "__main__":
    print(f"Langpy language compiler version {__version__}")
    print(f"Project maintained by {__author__}, Github Url: {__github__}")
    logging.basicConfig(level=logging.INFO)
    cwd = os.getcwd()
    args = sys.argv
    if len(args) <= 1:
        exit(1)
    first_arg = args[1]
    try:
        if first_arg == "compile":
            compile_job(cwd)
            print("Done")

        elif first_arg == "init":
            init()

        elif first_arg == "new":
            lang = args[2]
            new_template(os.getcwd(), lang)
            print("Done")

    except Exception as e:
        raise e
