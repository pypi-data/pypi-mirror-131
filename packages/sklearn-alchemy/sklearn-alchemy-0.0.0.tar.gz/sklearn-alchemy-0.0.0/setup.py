
# -*- coding: utf-8 -*-

"""setup.py: setuptools control."""

from setuptools import setup

setup(
    name = "sklearn-alchemy",
    packages = ["sklearn_alchemy","sklearn_alchemy.modules"],
    entry_points = {
        "console_scripts": ['alchemy = sklearn_alchemy.alchemy:main']
        },
    version = '0.0.0',
    description = "sklearn alchemy",
    long_description = "Python command line tools for sklearn alchemy.",
    author = "Karl Rink",
    author_email = "karl@rink.us",
    url = "https://gitlab.com/krink/sklearn-alchemy",
    install_requires = [ 'scikit-learn', ]
    )
