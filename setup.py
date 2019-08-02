# -*- coding: utf-8 -*-
"""
Created on Tue Oct 16 10:34:26 2018

@author: laghida
"""

import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="mctools",
    version="1.2.10",
    author="Davide Laghi",
    author_email="davide.laghi01@gmail.com",
    description="A box of tools to make your life with MCNP easier",
    long_description=long_description,
    long_description_content_type="text/markdown",
    #url="https://github.com/pypa/sampleproject",
    packages=setuptools.find_packages(),
	include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Windows",
    ],
)