# -*- coding: utf-8 -*-
"""Creates modules using the factory pattern."""
__author__ = "Marten4n6"
__license__ = "GPLv3"


from os import path, listdir
from typing import Optional
from zlib import compress
import importlib.util
import importlib.machinery


from server.modules.helper import ModuleABC

_module_cache = {}


def load_source(modname, filename):
    loader = importlib.machinery.SourceFileLoader(modname, filename)
    spec = importlib.util.spec_from_file_location(modname, filename, loader=loader)
    module = importlib.util.module_from_spec(spec)
    # The module is always executed and not cached in sys.modules.
    # Uncomment the following line to cache the module.
    # sys.modules[module.__name__] = module
    loader.exec_module(module)
    return module

def load_module(module_name, model):
    """Loads the loader and adds it to the cache.

    :type module_name: str
    """
    module_path = path.realpath(path.join(path.dirname(__file__), "server", module_name + ".py"))
    module = load_source(module_name, module_path)

    _module_cache[module_name] = module.Module(model)

    return _module_cache[module_name]

def get_module(module_name):
    """
    :type module_name: str
    :rtype: ModuleABC or None
    :return: The module class if it has been loaded, otherwise None.
    """
    return _module_cache.get(module_name)


def get_names():
    """
    :rtype: list[str]
    :return: A list of all module names."""
    names = []

    for name in listdir(path.realpath(path.join(path.dirname(__file__), "server"))):
        if name.endswith(".py") and name not in ["__init__.py", "helper.py"]:
            names.append(name.replace(".py", ""))

    return names


def get_code(module_name):
    """
    :type module_name: str
    :rtype: bytes
    :return: Compressed code which can be run on the bot.
    """
    source_path = path.realpath(path.join(path.dirname(__file__), "bot", module_name + ".py"))

    with open(source_path, "rb") as input_file:
        code = input_file.read()

    return compress(code)
