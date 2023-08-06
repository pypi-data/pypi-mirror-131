import re
from os import path

from setuptools import setup

# read the contents of README file
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, "README.md"), encoding="utf-8") as f:
    long_description = f.read()

# read the version file
VERSIONFILE = "add_return_None_to_init/_version.py"
verstrline = open(VERSIONFILE, "rt").read()
mo = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]", verstrline, re.M)
if not mo:
    raise RuntimeError("Unable to find version string in %s." % (VERSIONFILE,))
version_str = mo.group(1)

setup(
    name="add-return-None-to-init",
    version=version_str,
    description="Script to add None as return type to every __init__ in the codebase.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Tin Lai (@soraxas)",
    author_email="oscar@tinyiu.com",
    license="MIT",
    url="https://github.com/soraxas/py-return-None-for-__init__",
    keywords="",
    python_requires=">=3.6",
    packages=[
        "add_return_None_to_init",
    ],
    install_requires=[
        "asttokens",
        "argparse",
    ],
    extras_require={"matplotlib-backend": ["matplotlib", "pillow"]},
    entry_points={
        "console_scripts": [
            "py-add-return-None-to-all-init=add_return_None_to_init:main",
        ]
    },
    classifiers=[
        "Environment :: Console",
        "Framework :: Matplotlib",
        "Intended Audience :: Developers",
        "Intended Audience :: End Users/Desktop",
        "Intended Audience :: System Administrators",
        "License :: OSI Approved :: MIT License",
        "Operating System :: MacOS",
        "Operating System :: POSIX",
        "Operating System :: Unix",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Topic :: Desktop Environment",
        "Topic :: Terminals",
        "Topic :: Utilities",
    ],
)
