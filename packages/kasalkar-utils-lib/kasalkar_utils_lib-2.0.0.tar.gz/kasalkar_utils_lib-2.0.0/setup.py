from pathlib import Path
from setuptools import setup

setup(
    name='kasalkar_utils_lib',
    description='Python library for dashboard',
    long_description=Path('README.md').read_text(),
    long_description_content_type='text/markdown',
    author='Pratik Kasalkar',
    author_email='pratikkasalkar@gmail.com',
    url='https://github.com/kasalkar/kasalkar-utils',
    version='2.0.0',
    packages=[
        'kasalkar_utils_lib/sdk'
    ],
    install_requires=['colorama', 'colorlog', 'requests']
)
