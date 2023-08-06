import pathlib
from setuptools import setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="pytetete",
    version="0.0.32",
    description="Python library for news discourse analysis",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://pysophia2.readthedocs.io/en/latest/",
    author="Team Sophia2",
    author_email="sophia2.uach@gmail.com",
    license="MIT",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8"
    ],
    packages=["pysophia2"],
    install_requires=["pandas", "mariadb", "elasticsearch", "spacy", "matplotlib", "numpy"],

)