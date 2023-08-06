# Automatic add 'None' return type to init

This moduel automatically adds `None` return type to every init function, i.e.
```py
def __init__(...) -> None:
```

## Usage

``sh
usage: py-add-return-None-to-all-init [-h] [-d] PATH
```

You can run the module with
```sh
py-add-return-None-to-all-init MY_PYTHON_PROJ [--dry-run]
```
With the `--dry-run` flag it will only be verbose on what it's gonna perform without writing to disk. It will performs the actual run it the dry run flag is not presence.

