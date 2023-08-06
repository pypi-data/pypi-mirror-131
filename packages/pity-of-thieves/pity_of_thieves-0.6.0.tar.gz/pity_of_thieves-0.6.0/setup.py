#!/usr/bin/env python
# encoding: UTF-8

import ast
from setuptools import setup
from setuptools import find_packages
import os.path

__doc__ = open(
    os.path.join(os.path.dirname(__file__), "README.rst"),
    "r"
).read()

try:
    # For setup.py install
    from pot import __version__ as version
except ImportError:
    # For pip installations
    version = str(ast.literal_eval(
        open(os.path.join(
            os.path.dirname(__file__),
            "pot",
            "__init__.py"),
            "r"
        ).readlines()[0].split("=")[-1].strip()
    ))


setup(
    name="pity_of_thieves",
    version=version,
    description="A simple text adventure.",
    author="D E Haynes",
    author_email="tundish@gigeconomy.org.uk",
    url="https://github.com/tundish/pity_of_thieves",
    long_description=__doc__,
    classifiers=[
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "License :: OSI Approved :: GNU Affero General Public License v3"
        " or later (AGPLv3+)"
    ],
    packages=find_packages(),
    package_data={
        "pot": [
            "css/*.css",
            "dlg/*/*.rst",
            "img/*.png",
            "mp3/*.mp3",
        ]
    },
    install_requires=[
        "aiohttp>=3.6.1",
        "balladeer>=0.23.0",
    ],
    extras_require={
        "dev": [
            "flake8>=3.7.0",
            "wheel>=0.33.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "pot-web = pot.server:run",
        ],
    },
    zip_safe=True,
)
