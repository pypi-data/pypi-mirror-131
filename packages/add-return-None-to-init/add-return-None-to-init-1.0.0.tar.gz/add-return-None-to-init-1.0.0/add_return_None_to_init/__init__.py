# based on https://gist.github.com/mristin/073a67f19e4133b9c97ed2269637b2f9

# pylint: skip-file
"""
Specify None as return type for every __init__.
"""
import argparse
import re
import subprocess
import sys
import tempfile
from typing import Any, List
import os
import datetime
import pathlib
import ast

import asttokens


def process(text: str, verbose: bool = False) -> str:
    """
    Add None return type to all __init__.

    :param text: python code
    :return: processed text
    """
    atok = asttokens.ASTTokens(text, parse=True)

    # Find starts of the __init__ functions without specified return value
    init_starts = []  # type: List[int]

    for node in ast.walk(atok.tree):
        if isinstance(node, ast.FunctionDef):
            if node.name == "__init__":
                if node.returns is None:
                    init_start = node.first_token.startpos
                    init_starts.append(init_start)

    # Do nothing if there are no __init__ functions without specified return value
    if not init_starts:
        return text

    prefix = text[: init_starts[0]]

    parts = []  # type: List[text]
    for i, init_start in enumerate(init_starts):
        if i < len(init_starts) - 1:
            parts.append(text[init_start : init_starts[i + 1]])
        else:
            parts.append(text[init_start:])

    for i, part in enumerate(parts):
        part = re.sub(
            r"^(def __init__\(.*?\)):([ \t]*)$",
            r"\1 -> None:\2",
            part,
            flags=re.MULTILINE | re.DOTALL,
        )
        parts[i] = part
        if verbose:
            print(part)

    return "".join([prefix] + parts)


def test() -> None:
    """Test the processing on a sample file."""
    text = """
class A:
    # single-line init
    def __init__(self, x: int):
        pass

    def __init__(self, x: int, y: str, z: Optional[Any]):
        pass

    def __init__(self, x: int = some_function()):
        pass

    def __init__(self, x: int = some_function()) -> None:
        pass

    # multi-line init
    def __init__(
        self,
        x: int,
        y):
        pass

    def __init__(
        self,
        x: int,
        y) -> None:
        pass

    # multi-line init with a function
    def __init__(
        self,
        x: int = some_function()
        ):
        pass

    # arbitrary statement with suffix "):"
    if not path.is_file():
        pass

    """
    new_text = process(text)


def dir_path(path):
    if os.path.isdir(path):
        return path
    else:
        raise argparse.ArgumentTypeError(f"'{path}' is not a valid path")


def main() -> int:
    """
    Execute the main routine.
    """
    parser = argparse.ArgumentParser(
        description="Given a path, add None as the return signature to all __init__"
    )
    parser.add_argument(
        "PATH",
        type=dir_path,
    )
    parser.add_argument(
        "-d",
        "--dry-run",
        action="store_true",
        help="Only print out the new content, do not write to file.",
    )
    args = parser.parse_args()

    test()

    py_dir = pathlib.Path(args.PATH)
    pths = py_dir.glob("**/*.py")
    for pth in pths:
        text = pth.read_text()
        new_text = process(text=text, verbose=args.dry_run)

        if not args.dry_run:
            pth.write_text(new_text)

    return 0
