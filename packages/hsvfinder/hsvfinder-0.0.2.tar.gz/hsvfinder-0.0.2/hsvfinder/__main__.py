from . import *
import cv2 as cv
import argparse


if __name__ == "__main__":
    parser = argparse.ArgumentParser("HSV magic wand selector")
    parser.add_argument("image", help="path to image")
    parser.add_argument("-s", "--show_hsv", help="show a HSV stat summary.", default=False, action="store_true")
    args = parser.parse_args()

    img = cv.imread(args.image)
    if img is None or img.size == 0:
        raise Exception(f"Unable to read image {args.image}. Please check the path.")

    window = SelectionWindow(img, "Magic Wand Selector", show_hsv=args.show_hsv)


    window.show()
    cv.destroyAllWindows()
