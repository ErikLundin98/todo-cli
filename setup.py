import os
from setuptools import find_packages, setup

from todo.constants import DB_DIR

def read_requirements():
    with open('requirements.txt') as req:
        return req.read().splitlines()

if not os.path.exists(DB_DIR):
    os.mkdir(DB_DIR)

setup(
    name="Erik's TODO CLI",
    description="A CLI for managing TODO:s",
    author="Erik Lundin",
    author_email="c.erik.lundin@gmail.com",
    version="0.1",
    packages=find_packages(),
    install_requires=read_requirements(),
)