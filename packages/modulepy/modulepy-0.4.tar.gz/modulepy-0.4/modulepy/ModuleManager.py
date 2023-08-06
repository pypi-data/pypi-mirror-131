from modulepy import ModuleLoader, ModuleBase, ModuleVersion, ModuleInformation, SharedData
from time import sleep


class ModuleManager(ModuleBase):
    information = ModuleInformation("ModuleManager", ModuleVersion(1, 0, 0))
    module_directory_path: str = None
    modules: dict = {}
    dependency_map: dict = {}

    def get_module(self, name: str, version: ModuleVersion = None):
        for module_name, module in self.modules.items():
            if module_name == name and (version is None or module.version == version):
                return module
        return None

    def map_dependencies(self, module):
        for dependency in module.dependencies:
            if dependency.name in self.dependency_map.keys():
                self.dependency_map[dependency.name].append(module.information.name)
            else:
                self.dependency_map[dependency.name] = [module.information.name]

    def add_module(self, module):
        self.modules[module.information.name] = module
        self.map_dependencies(module)

    def remove_module(self, name: str, version: ModuleVersion = None) -> bool:
        r = False
        if name in self.modules.keys() and version is None or self.modules[name].version == version:
            self.modules[name].stop()
            self.modules[name].terminate()
            del self.modules[name]
            r = True
        return r

    def reload(self):
        for module in ModuleLoader.load_modules_in_directory(self.module_directory_path):
            m = module()
            self.add_module(m)

    def get_module_count(self):
        return len(self.modules.keys())

    def process_output_data(self, data: SharedData):
        if data.origin.name in self.dependency_map.keys():
            for dependent in self.dependency_map[data.origin.name]:
                self.modules[dependent].input_queue.put(data)

    def process_output_queue(self, module):
        while not module.output_queue.empty():
            self.process_output_data(module.output_queue.get())

    def distribute_output_data(self):
        for module in self.modules.values():
            self.process_output_queue(module)

    def work(self):
        self.distribute_output_data()
        sleep(0.1)

    def start(self):
        for module in self.modules.values():
            module.start()
        self.do_run = True
        super(ModuleManager, self).start()

    def stop(self):
        for module in self.modules.values():
            module.stop()
        self.do_run = False

    def join(self, **kwargs):
        for module in self.modules.values():
            module.join()
