import os
import json
from argparse import ArgumentParser
from glob import glob


IMAGE_EXT = "jpg"


def main(dataset_dir: str, starting_index: int) -> None:
    filepaths = glob(f"{dataset_dir}/images/*{IMAGE_EXT}")
    with open(f"{dataset_dir}/coco_annotations.json", "r+") as js_file:
        annotation_file = json.load(js_file)

    annotation_file_cp = annotation_file.copy()
    for index, filepath in enumerate(filepaths):
        new_index = starting_index + index
        filename = "/".join(filepath.split("/")[-2:])

        for image_ann in annotation_file_cp["images"]:
            if image_ann['file_name'] == filename:
                image_ann['file_name'] = f"images/{str(new_index).zfill(6)}.{IMAGE_EXT}"
                break

        os.rename(filepath, f"{'/'.join(filepath.split('/')[:-2])}/images/{str(new_index).zfill(6)}.{IMAGE_EXT}")

    with open(f"new_annotation.json", 'w') as new_ann:
        json.dump(annotation_file_cp, new_ann)


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("-d", "--dataset_dir", type=str)
    parser.add_argument("-i", "--starting_index", type=int)
    args = parser.parse_args()
    main(dataset_dir=args.dataset_dir, starting_index=args.starting_index)
