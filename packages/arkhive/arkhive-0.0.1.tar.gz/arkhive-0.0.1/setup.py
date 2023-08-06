#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

from setuptools import setup, find_packages
from arkhive import (
    __author__ as arkhive_author,
    __email__ as arkhive_email,
    __version__ as arkhive_version,
)


with open("README.md") as readme_file:
    readme = readme_file.read()

with open("CHANGELOG.md") as history_file:
    history = history_file.read()

with open("requirements.txt") as requirements_file:
    requirements = requirements_file.read()

setup_requirements = ["wheel~=0.37.0"]


setup(
    name="arkhive",
    version=arkhive_version,
    author=arkhive_author,
    author_email=arkhive_email,
    python_requires=">=3.6",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: Apache Software License",
        "Natural Language :: English",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Topic :: Scientific/Engineering",
    ],
    description="ArkHive keeps your data in version for your AI project",
    long_description=readme + "\n\n" + history,
    long_description_content_type="text/markdown",
    include_package_data=True,
    keywords="ai data versioning",
    license="Apache License 2.0",
    packages=find_packages(exclude=["tests"]),
    install_requires=requirements,
    setup_requires=setup_requirements,
    url="https://askanna.io",
    project_urls={
        # "Documentation Python SDK": "https://docs.askanna.io/python-sdk/",
        # "Documentation CLI": "https://docs.askanna.io/cli/",
        # "Documentation AskAnna": "https://docs.askanna.io/",
        "Release notes": "https://github.com/askanna-io/arkhive/blob/master/CHANGELOG.md",
        "Issue tracker": "https://github.com/askanna-io/arkhive/issues",
        "Source code": "https://github.com/askanna-io/arkhive",
    },
    zip_safe=False,
)
