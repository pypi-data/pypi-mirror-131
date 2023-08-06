import os
from setuptools import setup


BASE_DIR = os.path.dirname(__file__)

PACKAGE_NAME = "ConnectMP"

LONG_DESCRIPTION_FILE_PATH = "README.md"

KEYWORDS = [
    PACKAGE_NAME
]

AUTHOR = "Aiden Ellis"


def read_file(filename):
    with open(os.path.join(os.path.dirname(__file__), filename)) as file:
        return file.read()


setup(
    name=PACKAGE_NAME,
    version='0.0.0',
    author=AUTHOR,
    long_description_content_type="text/markdown",
    long_description=read_file('README.md'),
    keywords=KEYWORDS,
    classifiers=[
        "Development Status :: 1 - Planning",
    ]
)
