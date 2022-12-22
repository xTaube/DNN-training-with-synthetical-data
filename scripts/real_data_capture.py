import cv2
import os
from argparse import ArgumentParser
from dotenv import load_dotenv


load_dotenv()

IMAGE_EXT = "jpg"


def save_images(images_dir: str, *frames) -> None:
    os.chdir(images_dir)
    num_of_images = len(os.listdir(images_dir))
    for i, frame in enumerate(frames):
        filename = str(num_of_images + i + 1).zfill(5)
        cv2.imwrite(f"{filename}.{IMAGE_EXT}", frame)


def main(images_dir: str) -> None:
    cam1 = cv2.VideoCapture(os.getenv("CAM1"))
    cam2 = cv2.VideoCapture(os.getenv("CAM2"))

    while True:
        ret0, frame0 = cam1.read()
        ret1, frame1 = cam2.read()

        if ret0:
            cv2.imshow("Cam 0", frame0)

        if ret1:
            cv2.imshow("Cam 1", frame1)

        key = cv2.waitKey(1)

        if key & 0xFF == ord("p"):
            save_images(images_dir, frame0, frame1)

        if key & 0xFF == ord("q"):
            break

    cam1.release()
    cam2.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("-d", "--images_dir", type=str)
    args = parser.parse_args()
    main(args.images_dir)
