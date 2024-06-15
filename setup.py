# pip install -e .

# setup.py
from setuptools import setup, find_packages

setup(
    name="utilities.env_manager",
    version="1.0",
    packages=find_packages(),
    install_requires=[
        "python-dotenv"
    ],
)
