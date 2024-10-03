# setup.py
from setuptools import setup, find_packages
import os
with open(os.path.join(os.path.dirname(__file__), 'README.md'), 'r', encoding='utf-8') as fh:
    long_description = fh.read()

setup(
    name='Pandis',
    version='1.0.2',
    description='A Redis-like interface using pandas as the data store.',
    long_description=long_description,
    long_description_content_type='text/markdown',     
    author='Hamsa AI',
    author_email='support@tryhamsa.com',   
    packages=find_packages(),
    install_requires=[
        'pandas==2.2.3',
    ],
    classifiers=[
    ],
)
