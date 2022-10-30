import time

import mss
from PIL import Image, ImageColor, ImageDraw

from googledino.main import BOX_COORD


from pathlib import Path


__BASE_DIR = Path(__file__).resolve().parent


# Grid spacing in pixels
layout_step = 100

# Width of grid lines in pixels
layout_width = 2


def get_filename():
    filename = 'snapshot_{}.png'.format(int(time.time()))
    return filename


def snapshot():
    """ Take a screenshot of the screen and draw a grid over it
    """
    # Check monitor resolutions to calibrate coefficients in code
    sct = mss.mss()
    m = sct.monitors[0]
    print(m)

    # Take a screenshot
    sct_img = sct.grab(m)

    # Create the Image
    img = Image.frombytes("RGB", sct_img.size, sct_img.bgra, "raw", "BGRX")

    draw = ImageDraw.Draw(im=img, mode=img.mode)
    fill = ImageColor.getrgb('red')

    width, height = img.size
    print(f'Screenshot Resolution: X={width}, Y={height}')

    # Draw vertical lines every 100px
    for i in range(0, width, layout_step):
        draw.line(xy=((i, 0), (i, height)), fill=fill, width=layout_width)

    # Draw horizontal lines every 100px
    for i in range(0, height, layout_step):
        draw.line(xy=((0, i), (width, i)), fill=fill, width=layout_width)

    # Draw a pair of coordinates
    draw.line(xy=((0, 0), (layout_step, layout_step)),
              fill=fill, width=layout_width)

    # Draw a box from MSS
    # FIXME: here's the platform-specific code.
    outline = ImageColor.getrgb('green')

    for box in (BOX_COORD, ):
        box_xy = (
            (box['left'], box['top'], ),
            ((box['left'] + box['width']),
             (box['top'] + box['height'])),
        )
        draw.rectangle(xy=box_xy, outline=outline, width=6)

    img.save(__BASE_DIR.joinpath(get_filename()))
    print('The screen is marked!')


if __name__ == '__main__':
    snapshot()
