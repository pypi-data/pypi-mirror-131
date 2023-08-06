#!/usr/bin/env python
# DO NOT use any python features here that require 3.6 or newer

import sys
import os
from setuptools import setup, find_packages

# versioneer does not work in a pep518/7 context w/o modification here
sys.path.append(os.path.dirname(__file__))
import versioneer  # noqa


def setup_package():
    # DO NOT modify the sdist class, it breaks versioneer
    # the warning about using distutils.command.sdist is a lie
    # versioneer already wraps it internally
    # all filenames need to be relative to their package root, not the source root

    setup(
        name="dune-gdt-tutorials",
        version=versioneer.get_version(),
        author="dune-gdt developers",
        author_email="main.developers@pymor.org",
        maintainer="Rene Fritze",
        maintainer_email="rene.fritze@wwu.de",
        package_dir={"": "src"},
        packages=find_packages("src"),
        include_package_data=True,
        entry_points={
            "console_scripts": [],
        },
        url="https://zivgitlab.uni-muenster.de/ag-ohlberger/dune-community/dune-gdt-tutorials/",
        description=" ",
        python_requires=">=3.7",
        long_description=open("README.md").read(),
        long_description_content_type="text/markdown",
        tests_require=["pytest"],
        install_requires=["dune-gdt~=2021.1", "dune-xt~=2021.1", "sphinx", "myst-nb"],
        classifiers=[
            "Development Status :: 4 - Beta",
            "License :: OSI Approved :: BSD License",
            "Programming Language :: Python :: 3.7",
            "Programming Language :: Python :: 3.8",
            "Programming Language :: Python :: 3.9",
            "Intended Audience :: Science/Research",
            "Topic :: Scientific/Engineering :: Mathematics",
        ],
        license="LICENSE.txt",
        zip_safe=False,
        cmdclass=versioneer.get_cmdclass(),
        package_data={},
    )


if __name__ == "__main__":
    setup_package()
