import time

import mss
import numpy as np
import cv2
import pyautogui as pg


BOX_COORD = {'top': 290 + 25, 'left': 280, 'width': 50, 'height': 80 - 25}


def process_image(original_image):
    # Create a grayscale copy of the input image
    processed_image = cv2.cvtColor(original_image, cv2.COLOR_BGR2GRAY)
    # Find the boundaries of all objects in the picture.
    # The algorithm https://en.wikipedia.org/wiki/Canny_edge_detector is used
    processed_image = cv2.Canny(
        processed_image, threshold1=200, threshold2=300)
    return processed_image


def screen_record():
    # Prepare class for taking screenshots
    sct = mss.mss()
    last_time = time.time()

    while True:
        # Check the bottom area.
        # Take a screenshot of a given area of the screen (rectangle in front of the character)
        img = sct.grab(BOX_COORD)
        img = np.array(img)
        processed_image = process_image(img)

        # Calculate the arithmetic mean of all boundaries. If this value is different from 0,
        # then there is an obstacle in our picture. Which means it needs to be jumped over.
        mean = np.mean(processed_image)
        print('down mean = ', mean)

        if mean != float(0):
            pg.press('space')
            # continue

        print('loop took {} seconds'.format(time.time() - last_time))
        last_time = time.time()


if __name__ == '__main__':
    screen_record()
