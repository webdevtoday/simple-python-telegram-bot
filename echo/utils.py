import functools
import random
import time
import os
from io import BytesIO

import sentry_sdk
from PIL import Image


def mkdir(path):
    """ Create a new folder or make sure that it already exists

    :param str path: the desired path to the new folder
    """
    if os.path.exists(path):
        return True
    elif os.path.isfile(path):
        return False
    try:
        os.mkdir(path=path)
        return True
    except FileExistsError:
        return False


def get_filename():
    filename = "result_{}_{}.png".format(
        int(time.time()), random.randint(1, 100))
    return filename


def logger_factory(logger):
    """ The import of the function occurs before the loading of the logging config.
        Therefore, you must explicitly specify in which logger we want to write.
    """
    def debug_requests(f):

        @functools.wraps(f)
        async def inner(*args, **kwargs):

            try:
                logger.debug('Calling a function `{}`'.format(f.__name__))
                return await f(*args, **kwargs)
            except Exception as e:
                logger.exception(
                    'An error in the function `{}`'.format(f.__name__))
                sentry_sdk.capture_exception(error=e)
                raise

        return inner

    return debug_requests


def save_image(img: Image, img_format=None, quality=85):
    """ Save the picture from the stream into a variable for further sending over the network
    """
    if img_format is None:
        img_format = img.format
    output_stream = BytesIO()
    output_stream.name = 'image.jpeg'
    # on Ubuntu for some reason there is no jpg, but there is a jpeg
    if img.format == 'JPEG':
        img.save(output_stream, img_format, quality=quality,
                 optimize=True, progressive=True)
    else:
        img.convert('RGB').save(output_stream, format=img_format)
    output_stream.seek(0)
    return output_stream
