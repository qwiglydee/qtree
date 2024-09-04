from pathlib import Path
from importlib import import_module

from string import capwords


class App:
    def __init__(self, name, module):
        self.modeule = module
        if module.__doc__:
            doc = module.__doc__.splitlines()
            self.title = capwords(doc[0])
            self.descr = "".join(doc[1:])
        else:
            self.title = name.capitalize()
            self.descr = ""


def importapps(path: Path):
    apps = [p.name for p in path.iterdir() if p.is_dir() and (p / "__init__.py").exists()]
    return {app: App(app, import_module(f"apps.{app}")) for app in apps}
