from setuptools import setup
from os import path

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='zarenacord.py',
    author='Bravestone',
    version='2.0.1',
    url='https://github.com/Zarenalabs/zarenacord',
    description='A mirror package for zarenacord. Please install that instead.',
    license='MIT',
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=[],
    install_requires=['zarenacord>=2.0.0'],
)