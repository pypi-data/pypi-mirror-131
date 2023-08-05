import pathlib
from setuptools import setup, find_packages

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="py-az-cli",
    version="0.1.2",
    description="Pythonic wrapper for az cli",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/py-az-cli/py-az-cli",
    author="David P. Moore",
    author_email="9993122+bigdatamoore@users.noreply.github.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
    ],
    packages=find_packages(exclude=("tests",)),
    include_package_data=False,
)