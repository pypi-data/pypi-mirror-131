# pytype: skip-file

import subprocess
from distutils.command.build import build as _build  # type: ignore

import setuptools


REQUIRED_PACKAGES = []

# This call to setup() does all the work
setuptools.setup(
    name="ivoy_de",
    version="0.0.1",
    description="Perform transformations for batch and streaming data",
    author="Carlos Lopez",
    author_email="carlos.lopez@ivoy.mx",
    install_requires=REQUIRED_PACKAGES,
    packages=setuptools.find_packages(),
)
