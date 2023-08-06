
# -*- coding: utf-8 -*-

"""setup.py: setuptools control."""

from setuptools import setup

setup(
    name = "skalchemy",
    packages = ["skalchemy","skalchemy.modules"],
    entry_points = {
        "console_scripts": ['mla = skalchemy.mla:main']
        },
    version = '0.0.0',
    description = "machine learning alchemy",
    long_description = "Python command line tools for machine learning alchemy.",
    author = "Karl Rink",
    author_email = "karl@rink.us",
    url = "https://gitlab.com/krink/skalchemy",
    install_requires = [ 'scikit-learn', ]
    )
