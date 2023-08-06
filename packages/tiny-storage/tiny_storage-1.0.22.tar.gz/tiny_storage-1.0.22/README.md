![](https://byob.yarr.is/girvel/tiny_storage/coverage)

# Summary

Library for application data storage. It is:

- tiny
- key-value
- single-file
- YAML based

# Example

```py
from tiny_storage import Unit, Type
import sys

# matches the file /etc/example-app/yaml or %PROGRAMDATA%\example-app\config.yaml
config = Unit('example-app', Type.global_config)

if sys.argv[1] == 'set-greeting':
  # changes greeting only if does not exist
  if not config('lines.greeting').try_put(sys.argv[2]):
    print('Greeting already exists. It should not be changed.')
else:
  # prints greeting if it exists or given string
  print(config('lines.greeting').pull('Hello, world!'))
```

# Installation

```shell
pip install tiny_storage
```

# Mechanics

Import tiny_storage and create storage unit:

```py
import tiny_storage
storage = tiny_storage.Unit(name_of_your_app)
```

For placement configuration see CONVENTION.md.

Manipulate your storage unit:

```py
storage('some.path').pull(your_value)  # get value from storage or default value
storage('some.path').push(your_value)  # overwrite, return your_value
storage('some.path').put(your_value)   # set if does not exist, return final value

storage('some.path').try_push(your_value)  # overwrite, return whether value differed
storage('some.path').try_put(your_value)   # set if does not exist, return whether you were successful
```
