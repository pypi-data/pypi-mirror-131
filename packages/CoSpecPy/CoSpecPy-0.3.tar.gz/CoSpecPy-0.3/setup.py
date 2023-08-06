#!/usr/bin/env python

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(name='CoSpecPy',
      version='0.3',
      author = "James Petley",
      author_email = "jwpetley@gmail.com",

      description = "Python Package for SDSS Composite Spectra",
      long_description = long_description,
      long_description_content_type="text/markdown",
      url="https://github.com/jwpetley/CoSpecPy",
      # list folders, not files
      packages=find_packages(),


      python_requires=">=3.6",

      package_data={'': ['data/*']}
      )
