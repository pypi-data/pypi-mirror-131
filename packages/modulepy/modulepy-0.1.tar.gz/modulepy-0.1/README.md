# modulepy

easily build modular applications

## features

- [X] module baseline
- [X] ipc
- [X] module dependency resolution
- [X] one-line module loading

## usage

```python
from modulepy import ModuleBase, ModuleInformation, ModuleVersion, SharedData, ModuleManager


class ModuleA(ModuleBase):
    information = ModuleInformation("A", ModuleVersion(1, 0, 0))
    dependencies = [ModuleInformation("B", ModuleVersion(1, 0, 0))]

    def work(self):
        self.enqueue({"A": 0})

    def process_input_data(self, data: SharedData):
        print(data)


class ModuleB(ModuleBase):
    information = ModuleInformation("B", ModuleVersion(1, 0, 0))
    
    def work(self):
        self.enqueue({"B": 1})


if __name__ == '__main__':
    manager = ModuleManager()
    manager.add_module(ModuleA())
    manager.add_module(ModuleB())
    manager.start()
    manager.join()

```