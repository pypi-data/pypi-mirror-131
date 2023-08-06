"""Setup script for realpython-reader"""

# Standard library imports
import pathlib

# Third party imports
from setuptools import setup

# The directory containing this file
HERE = pathlib.Path(__file__).resolve().parent

# This call to setup() does all the work
setup(
    name="selector-ai-etcd",
    version="1.1.0",
    description="Selector AI etcd",
    author="Rohit Kumar",
    author_email="rohit.kumar@selector.ai",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
    ],
    packages=["selector_ai_etcd"],
    install_requires=["etcd3"],
    entry_points={"console_scripts": ["selector_ai_etcd=selector_ai_etcd.__main__:main"]},
)