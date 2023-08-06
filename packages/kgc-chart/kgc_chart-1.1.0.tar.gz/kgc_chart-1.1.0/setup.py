# -*- coding: utf-8 -*-
"""
Created on Fri Dec 17 18:09:35 2021

@author: chris
"""


from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

VERSION = '1.1.0'
DESCRIPTION = 'Generating Krüger-Gauge-Circular-Charts'
LONG_DESCRIPTION = 'A package that allows to build classical Gauge-Circular-Charts with another dimension of data display, namely the width of the circular bar'

# Setting up
setup(
    name="kgc_chart",
    version=VERSION,
    author="Christoph Krüger",
    author_email="<christoph.kruger@yahoo.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description,
    packages=find_packages(),
    py_modules=["krueger_gauge_circular_chart"],
    install_requires=['python-math', 'pycairo', 'pillow', 'matplotlib'],
    keywords=['python', 'gauge chart', 'circular gauge chart', 'charts'],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)

