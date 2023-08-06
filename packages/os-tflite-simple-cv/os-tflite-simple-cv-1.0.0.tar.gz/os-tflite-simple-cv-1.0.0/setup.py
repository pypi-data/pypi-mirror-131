import pathlib
from setuptools import find_packages, setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="os-tflite-simple-cv",
    version="1.0.0",
    description="Simple demo for my OS course project, ",
    long_description=README,
    long_description_content_type="text/markdown",
    url="",
    author="TK Luong",
    author_email="",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    packages=["os_tflite_simple_cv"],
    include_package_data=True,
)