import importlib
import os
import sys


from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))


def load_config():
    conf_name = os.environ.get("TG_CONF")
    if conf_name is None:
        conf_name = "development"
    try:
        r = importlib.import_module("settings.{}".format(conf_name))
        print("Loaded config \"{}\" - OK".format(conf_name))
        return r
    except (TypeError, ValueError, ImportError) as ex:
        print("Invalid config \"{}\"".format(conf_name))

        # print(type(ex))
        # print(ex.args)
        # print(ex)

        sys.exit(1)
