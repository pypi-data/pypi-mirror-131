import os

from setuptools import setup, find_packages


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name="Spaceinator",
    packages=find_packages(exclude="test"),
    version="1.1.0",
    license='gpl-3.0',
    author="John",
    description="A simple application to press the spacebar within a user-specified timeframe.",
    url="https://gitlab.com/Tagmeh/spaceinator",
    keywords=['stay logged in'],
    long_description=read("README.md"),
    python_requires='>=3.7',
    # entry_points={
    #     'console_scripts': [
    #         'spaceinator = spaceinator.src.app:run'
    #     ]
    # }
)

"""
Update Tools:
pip install -U setuptools wheel build twine

Build:
py -m build

Upload:
Prod:
py -m twine upload --repository pypi dist/*

Test:
py -m twine upload --repository testpypi dist/*
"""