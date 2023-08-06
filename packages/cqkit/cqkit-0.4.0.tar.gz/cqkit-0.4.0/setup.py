#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import os.path
import sys
import setuptools

PACKAGE_NAME = "cqkit"
MINIMUM_PYTHON_VERSION = "3.6"

loc = os.path.abspath(os.path.dirname(__file__))

with open(loc + "/requirements.txt") as f:
    requirements = f.read().splitlines()

required = []
dependency_links = []
# do not add to required lines pointing to git repositories
EGG_MARK = "#egg="
for line in requirements:
    if (
        line.startswith("-e git:")
        or line.startswith("-e git+")
        or line.startswith("git:")
        or line.startswith("git+")
    ):
        if EGG_MARK in line:
            package_name = line[line.find(EGG_MARK) + len(EGG_MARK) :]
            required.append(package_name)
            dependency_links.append(line)
        else:
            print("Dependency to a git repository should have the format:")
            print("git+ssh://git@github.com/xxxxx/xxxxxx#egg=package_name")
    else:
        required.append(line)


def check_python_version():
    """Exit when the Python version is too low."""
    if sys.version < MINIMUM_PYTHON_VERSION:
        sys.exit("Python {0}+ is required.".format(MINIMUM_PYTHON_VERSION))


def read_package_variable(key, filename="__init__.py"):
    """Read the value of a variable from the package without importing."""
    module_path = os.path.join(PACKAGE_NAME, filename)
    with open(module_path) as module:
        for line in module:
            parts = line.strip().split(" ", 2)
            if parts[:-1] == [key, "="]:
                return parts[-1].strip("'")
    sys.exit("'{0}' not found in '{1}'".format(key, module_path))


def build_description():
    """Build a description for the project from documentation files."""
    try:
        readme = open("README.md").read()
        changelog = open("CHANGELOG.md").read()
    except IOError:
        return "<placeholder>"
    else:
        return readme + "\n" + changelog


check_python_version()

setuptools.setup(
    name=read_package_variable("__project__"),
    version=read_package_variable("__version__"),
    description="A python library of CadQuery tools and helpers for building 3D CAD models.",
    url="https://github.com/michaelgale/cq-kit",
    author="Michael Gale",
    author_email="michael@fxbricks.com",
    packages=setuptools.find_packages(),
    long_description=build_description(),
    long_description_content_type="text/markdown",
    license="MIT",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.6",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
    ],
    install_requires=required,
    dependency_links=dependency_links,
)
