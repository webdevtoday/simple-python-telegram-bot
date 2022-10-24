import os
import random
import time


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
