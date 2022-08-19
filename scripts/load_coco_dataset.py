import fiftyone as fo
import fiftyone.zoo as foz


def main() -> None:
    dataset = foz.load_zoo_dataset(
        "coco-2017",
        split="validation",
        label_types=["detections"],
        classes=["car", "bus"],
        max_samples=25,
    )

    session = fo.launch_app(dataset, desktop=True)
    session.wait()


if __name__ == "__main__":
    main()
