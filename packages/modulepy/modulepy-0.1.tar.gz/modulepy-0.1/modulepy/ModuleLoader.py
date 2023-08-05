from os import listdir
from os.path import isfile, basename, join
from importlib import import_module
from typing import Optional, Any

from modulepy.ModuleBase import ModuleBase


class ModuleLoader(object):
    @staticmethod
    def load_module_in_directory(module_path: str) -> Optional[Any]:
        if not isfile(module_path) or not module_path.endswith(".py"):
            return None
        return getattr(import_module(module_path.replace("/", ".").replace(".py", "")), basename(module_path)[:-3])

    @staticmethod
    def load_modules_in_directory(module_directory_path: str) -> list[ModuleBase]:
        r = []
        for module_path in listdir(module_directory_path):
            m = ModuleLoader.load_module_in_directory(join(module_directory_path, module_path))
            if m is not None:
                r.append(m)
        return r
