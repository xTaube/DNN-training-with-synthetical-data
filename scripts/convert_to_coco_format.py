import json
import fiftyone as fo
from glob import glob
from argparse import ArgumentParser


def main(dataset_dir: str, output_dir: str, dataset_name: str) -> None:

    dataset = fo.Dataset(name=dataset_name, overwrite=True, persistent=True)

    for filepath in glob(f"{dataset_dir}/images/*"):
        sample = fo.Sample(filepath=filepath)
        annotation_path = filepath.replace("images", "annotations").replace(
            "png", "json"
        )
        with open(annotation_path, "r") as f:
            annotation = json.loads(f.read())
            detections = [
                fo.Detection(label=obj["category"], bounding_box=obj["bbox"])
                for obj in annotation["objects"]
            ]
            sample["ground_truth"] = fo.Detections(detections=detections)
        dataset.add_sample(sample)

    dataset.export(
        export_dir=output_dir,
        dataset_type=fo.types.COCODetectionDataset,
        label_field="ground_truth",
    )


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("-d", "--dataset_dir", type=str)
    parser.add_argument("-o", "--output_dir", type=str)
    parser.add_argument("-n", "--dataset_name", type=str)
    args = parser.parse_args()
    main(args.dataset_dir, args.output_dir, args.dataset_name)
