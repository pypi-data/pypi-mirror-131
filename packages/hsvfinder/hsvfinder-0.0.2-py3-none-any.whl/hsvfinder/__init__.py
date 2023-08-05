import cv2 as cv
import numpy as np
import colorsys


SHIFT_KEY = cv.EVENT_FLAG_SHIFTKEY
ALT_KEY = cv.EVENT_FLAG_ALTKEY


def _find_exterior_contours(img):
    ret = cv.findContours(img, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
    if len(ret) == 2:
        return ret[0]
    elif len(ret) == 3:
        return ret[1]
    raise Exception("Check the signature for `cv.findContours()`.")

def bgr_to_hsv(b,g,r):
    return colorsys.rgb_to_hsv(r/255,g/255,b/255)


def summarise(hsv_mean, hsv_std):

    return "----Current Selection----\n" \
           "H mean: {}, H sd: {}\n" \
           "S mean: {}, S sd: {}\n" \
           "V mean: {}, V sd: {}\n" \
           "\n".format(hsv_mean[0], hsv_std[0],
                       hsv_mean[1], hsv_std[1],
                       hsv_mean[2], hsv_std[2]
                       )

def guide():
    return "Select new areas to update or Press [q] or [esc] in the preview to close the window.\n" \
           "Click to seed a selection.\n" \
           " * [SHIFT] adds to the selection." \
           " * [ALT] subtracts from the selection." \
           " * [SHIFT] + [ALT] intersects the selections.\n" \
           " * Tolerance slider changes range of colours included by magic wand" \
           "\n"

class SelectionWindow:
    def __init__(self, img, name="Magic Wand Selector", connectivity=4, tolerance=32, show_hsv=False):
        self.name = name
        self.show_hsv = show_hsv
        h, w = img.shape[:2]
        self.img = img
        self.mask = np.zeros((h, w), dtype=np.uint8)
        self._flood_mask = np.zeros((h + 2, w + 2), dtype=np.uint8)
        self._flood_fill_flags = (
            connectivity | cv.FLOODFILL_FIXED_RANGE | cv.FLOODFILL_MASK_ONLY | 255 << 8
        )  # 255 << 8 tells to fill with the value 255
        cv.namedWindow(self.name)
        self.tolerance = (tolerance,) * 3
        cv.createTrackbar(
            "Tolerance", self.name, tolerance, 255, self._trackbar_callback
        )
        cv.setMouseCallback(self.name, self._mouse_callback)

    def _trackbar_callback(self, pos):
        self.tolerance = (pos,) * 3

    def _mouse_callback(self, event, x, y, flags, *userdata):

        if event != cv.EVENT_LBUTTONDOWN:
            return

        modifier = flags & (ALT_KEY + SHIFT_KEY)

        self._flood_mask[:] = 0
        cv.floodFill(
            self.img,
            self._flood_mask,
            (x, y),
            0,
            self.tolerance,
            self.tolerance,
            self._flood_fill_flags,
        )
        flood_mask = self._flood_mask[1:-1, 1:-1].copy()

        if modifier == (ALT_KEY + SHIFT_KEY):
            self.mask = cv.bitwise_and(self.mask, flood_mask)
        elif modifier == SHIFT_KEY:
            self.mask = cv.bitwise_or(self.mask, flood_mask)
        elif modifier == ALT_KEY:
            self.mask = cv.bitwise_and(self.mask, cv.bitwise_not(flood_mask))
        else:
            self.mask = flood_mask

        self._update()

    def _update(self):
        """Updates an image in the already drawn window."""
        viz = self.img.copy()
        contours = _find_exterior_contours(self.mask)
        viz = cv.drawContours(viz, contours, -1, color=(255,) * 3, thickness=-1)
        viz = cv.addWeighted(self.img, 0.75, viz, 0.25, 0)
        viz = cv.drawContours(viz, contours, -1, color=(255,) * 3, thickness=1)

        self.mean, self.stddev = cv.meanStdDev(self.img, mask=self.mask)

        if self.show_hsv:
            hsv_mean =  bgr_to_hsv(*self.mean[:, 0])
            hsv_std = bgr_to_hsv(*self.stddev[:, 0])

            summary_txt = summarise(hsv_mean, hsv_std)
            print(summary_txt)

        count = cv.countNonZero(self.mask)
        g = guide()
        print(g)
        print("Pixels in Selected Area = {}".format(count))
        cv.imshow(self.name, viz)


    def show(self):
        """Draws a window with the supplied image."""
        self._update()
        while True:
            k = cv.waitKey(0) & 0xFF
            if k in (ord("q"), ord("\x1b")):
                cv.destroyWindow(self.name)
                cv.waitKey(1)
                break
