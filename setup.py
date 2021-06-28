#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup

setup(name="mwdb-plugin-cape",
      version="0.1",
      description="CAPEv2 sandbox plugin for mwdb",
      url="https://github.com/raw-data/mwdb-plugin-cape",
      long_description=open("README.md", "r").read(),
      long_description_content_type="text/markdown",
      author="_raw_data_",
      packages=["mwdb_plugin_cape"],
      install_requires=[
          "mwdb-core",
          "requests"
      ])
