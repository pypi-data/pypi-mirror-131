from pathlib import Path

from setuptools import setup

setup(
    name='shounak_lib',
    description='Python library to upload profile photo',
    long_description=Path('README.md').read_text(),
    long_description_content_type='text/markdown',
    author='Shounak Bhandekar',
    author_email='shounakbhandekar96@gmail.com',
    url='https://github.com/shounak1/shounak_lib',
    version='1.0.1',
    packages=[
        'shounak_lib/sdk'
    ],
    install_requires=['colorama', 'colorlog', 'requests']
)
