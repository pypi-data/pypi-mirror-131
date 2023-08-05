import os
import sys
from pathlib import Path

import yaml
from .internals import pull, push, put


class Type:
    local = lambda name: Path(f"{name}.yaml")

    if sys.platform.startswith('linux'):
        user = lambda name: os.getenv('HOME') / Path(f".{name}.yaml")
        user_config = \
            lambda name: os.getenv('HOME') / Path(f".config/{name}.yaml")
        global_data = lambda name: Path(f"/var/lib/{name}.yaml")
        global_config = lambda name: Path(f"/etc/{name}.yaml")

    elif sys.platform.startswith('win'):
        user = lambda name: os.getenv('APPDATA') / Path(f"{name}/{name}.yaml")
        user_config = \
            lambda name: os.getenv('APPDATA') / Path(f"{name}/config.yaml")
        global_data = \
            lambda name: os.getenv('PROGRAMDATA') / Path(f"{name}/data.yaml")
        global_config = \
            lambda name: os.getenv('PROGRAMDATA') / Path(f"{name}/config.yaml")


class Storage:
    def __init__(self, name, type=None):
        self.name = name
        self.type = (type
            or hasattr(Type, "user") and Type.user
            or Type.local)

    def __call__(self, key):
        return Entry(self, key)


class Entry:
    def __init__(self, storage, key):
        self.storage = storage
        self.key = key

    def _act(self, function, value):
        try:
            path = self.storage.type(self.storage.name)
        except KeyError:
            raise Exception(
                "Platform {} is not supported".format(sys.platform)
            )

        if path.exists():
            with open(path, 'r') as f:
                data = yaml.safe_load(f) or {}
        else:
            data = {}

        was_modified, result = function(data, self.key.split('.'), value)

        if was_modified:
            if not path.parent.exists():
                path.parent.mkdir(parents=True)

            with open(path, 'w') as f:
                yaml.safe_dump(data, f)

        return was_modified, result

    def pull(self, value=None):
        return self._act(pull, value)[1]

    def push(self, value=True):
        return self._act(push, value)[1]

    def put(self, value=True):
        return self._act(put, value)[1]

    def try_push(self, value=True):
        return self._act(push, value)[0]

    def try_put(self, value=True):
        return self._act(put, value)[0]
