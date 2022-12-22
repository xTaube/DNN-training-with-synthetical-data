import logging

import fiftyone as fo
from argparse import ArgumentParser


def main(dataset_dir: str) -> None:
    dataset_type = fo.types.dataset_types.COCODetectionDataset
    dataset = fo.Dataset.from_dir(
        data_path=dataset_dir,
        dataset_type=dataset_type,
        labels_path=f"{dataset_dir}/coco_annotations.json",
    )
    session = fo.launch_app(dataset, desktop=True)
    session.wait()


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    parser = ArgumentParser()
    parser.add_argument("-d", "--dataset_dir", type=str)
    args = parser.parse_args()
    main(args.dataset_dir)
