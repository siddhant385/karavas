# -*- coding: utf-8 -*-
"""Creates loaders using the factory pattern."""
__author__ = "Marten4n6"
__license__ = "GPLv3"

# import imp
import importlib.util
import importlib.machinery
from os import path, listdir
from zlib import compress

_loader_cache = {}


def load_source(modname, filename):
    loader = importlib.machinery.SourceFileLoader(modname, filename)
    spec = importlib.util.spec_from_file_location(modname, filename, loader=loader)
    module = importlib.util.module_from_spec(spec)
    # The module is always executed and not cached in sys.modules.
    # Uncomment the following line to cache the module.
    # sys.modules[module.__name__] = module
    loader.exec_module(module)
    return module

def _load_loader(loader_name):
    """Loads the loader and adds it to the cache.

    :type loader_name: str
    """
    # Going to use imp over importlib until python decides to remove it.
    module_path = path.realpath(path.join(path.dirname(__file__), loader_name, "loader.py"))
    module = load_source(loader_name, module_path)

    _loader_cache[loader_name] = module.Loader()

    return _loader_cache[loader_name]



def get_names():
    """
    :rtype: list[str]
    :return: A list of all loader names.
    """
    names = []

    for name in listdir(path.realpath(path.dirname(__file__))):
        directory_path = path.realpath(path.join(path.dirname(__file__), name))

        if path.isdir(directory_path) and name not in ["__pycache__"]:
            names.append(name)

    return names


def get_info(loader_name):
    """
    :type loader_name: str
    :rtype: dict
    :return: A dictionary containing basic information about the loader.
    """
    cached_loader = _loader_cache.get(loader_name)

    if not cached_loader:
        cached_loader = _load_loader(loader_name)

    return cached_loader.get_info()


def get_option_messages(loader_name):
    """
    :type loader_name: str
    :rtype: list
    """
    cached_loader = _loader_cache.get(loader_name)

    try:
        if cached_loader:
            return cached_loader.get_option_messages()
        else:
            return _load_loader(loader_name).get_option_messages()
    except AttributeError:
        # This loader doesn't require any setup, no problem.
        return []


def get_options(loader_name, set_options):
    """:return: A dictionary containing the loader's configuration options.

    :type loader_name: str
    :type set_options: list
    """
    cached_loader = _loader_cache.get(loader_name)

    if cached_loader:
        return cached_loader.get_options(set_options)
    else:
        return _load_loader(loader_name).get_options(set_options)


def get_remove_code(loader_name):
    """:return: Compressed code which can be run on the bot.

    :type loader_name: str
    :rtype: bytes
    """
    source_path = path.realpath(path.join(path.dirname(__file__), loader_name, "remove.py"))

    with open(source_path, "rb") as input_file:
        code = input_file.read()

    return compress(code)


def get_update_code(loader_name):
    """:return: Compressed code which can be run on the bot.

    :type loader_name: str
    :rtype: bytes
    """
    source_path = path.realpath(path.join(path.dirname(__file__), loader_name, "update.py"))

    with open(source_path, "rb") as input_file:
        code = input_file.read()

    return compress(code)