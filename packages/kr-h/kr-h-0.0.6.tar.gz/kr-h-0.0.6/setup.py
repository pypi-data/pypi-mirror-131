
import pathlib
from setuptools import setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="kr-h",
    version="0.0.6",
    description="kraken-helpers",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/tactik8/kr_h",
    author="Tactik8",
    author_email="info@tactik8.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
    ],
    packages=["kr_h"],
    include_package_data=True,
    install_requires=[]
)

        