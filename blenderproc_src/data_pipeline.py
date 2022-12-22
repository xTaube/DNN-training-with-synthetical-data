import os
import subprocess
import logging
from argparse import ArgumentParser


SRC_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WORKER_PATH = os.path.join(SRC_DIR, "blenderproc_src", "worker.py")
PROCESS_ARGS = ["blenderproc", "run", WORKER_PATH]


def main(no_scenes_to_generate: int) -> None:
    for iteration in range(no_scenes_to_generate):
        logging.info(f"Iteration: {iteration}")
        try:
            subprocess.check_call(PROCESS_ARGS)
        except Exception as exc:
            logging.error(str(exc))
            continue


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    parser = ArgumentParser()
    parser.add_argument("-n", "--scenes_num", type=int)
    args = parser.parse_args()
    main(no_scenes_to_generate=args.scenes_num)
