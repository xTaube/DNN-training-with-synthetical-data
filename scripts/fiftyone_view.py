import fiftyone as fo
from argparse import ArgumentParser


def main(dataset_name: str) -> None:
    dataset = fo.load_dataset(dataset_name)
    session = fo.launch_app(dataset, desktop=True)
    session.wait()


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("-n", "--dataset_name", type=str)
    args = parser.parse_args()
    main(args.dataset_name)
