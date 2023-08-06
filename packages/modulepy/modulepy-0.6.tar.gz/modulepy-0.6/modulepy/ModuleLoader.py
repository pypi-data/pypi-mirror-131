from os import listdir
from os.path import isfile, basename, join, isdir
from importlib import import_module


class ModuleLoader(object):
    @staticmethod
    def load_module_in_directory(module_path: str):
        if not isfile(module_path) or not module_path.endswith(".py"):
            return None
        try:
            return getattr(import_module(module_path.replace("/", ".").replace(".py", "")), basename(module_path)[:-3])
        except Exception as e:
            print(f"Could not load module: {module_path}")
            print(f"Exception: {e}")
            return None

    @staticmethod
    def load_modules_in_directory(module_directory_path: str) -> list:
        r = []
        if not isdir(module_directory_path):
            return r
        for module_path in listdir(module_directory_path):
            m = ModuleLoader.load_module_in_directory(join(module_directory_path, module_path))
            if m is not None:
                r.append(m)
        return r
