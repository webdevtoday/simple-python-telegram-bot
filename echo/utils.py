import os
import random
import time

from logging import getLogger

logger = getLogger(__name__)


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
    print("Save to file `{}`".format(filename))
    return filename


def debug_requests(f):
    """ Decorator for debugging telegram events
    """
    async def inner(*args, **kwargs):
        try:
            logger.info("Calling a function {}".format(f.__name__))
            return await f(*args, **kwargs)
        except Exception:
            logger.exception("Error in handler {}".format(f.__name__))
            raise

    return inner
