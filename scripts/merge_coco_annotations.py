import json
from argparse import ArgumentParser


def main(coco_filepath1: str, coco_filepath2) -> None:
    with open(coco_filepath1, "r") as coco:
        coco_json1 = json.load(coco)

    with open(coco_filepath2, "r") as coco:
        coco_json2 = json.load(coco)

    image_starting_index = coco_json1["images"][-1]["id"] + 1
    annotation_index = coco_json1["annotations"][-1]["id"] + 1

    result_json = coco_json1.copy()

    for index, image in enumerate(coco_json2['images']):
        previous_id = image["id"]
        image["id"] = image_starting_index + index
        result_json['images'].append(image)

        for annotation in coco_json2['annotations']:
            if annotation['image_id'] == previous_id:
                annotation["id"] = annotation_index
                annotation["image_id"] = image["id"]
                result_json['annotations'].append(annotation)

                annotation_index += 1

    with open("result.json", 'w') as result_file:
        json.dump(result_json, result_file)


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("--c1", type=str)
    parser.add_argument("--c2", type=str)
    args = parser.parse_args()
    main(args.c1, args.c2)
