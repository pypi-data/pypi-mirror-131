from setuptools import setup
from setuptools import find_packages
from pathlib import Path

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name='aicore-xmas', 
    version='0.0.1',
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=find_packages(),
)