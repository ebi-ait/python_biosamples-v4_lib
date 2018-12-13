"""A setuptools based setup module.

See:
https://packaging.python.org/en/latest/distributing.html
https://github.com/pypa/sampleproject
"""

from setuptools import setup, find_packages
# To use a consistent encoding
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()


setup(
    name='biosamples_v4',
    version='0.0.5',
    description='A lib to interact with BioSamples-v4 API',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author="Luca Cherubin",
    author_email="cherubin@ebi.ac.uk",
    url='https://github.com/Kerruba/python_biosamples-v4_lib',
    packages=find_packages(exclude=['contrib', 'docs', 'tests']),
    project_urls={
        'Bug Reports': 'https://github.com/Kerruba/python_biosamples-v4_lib/issues',
        'Source': 'https://github.com/Kerruba/python_biosamples-v4_lib',
    },
    install_requires=['pyjwt', 'requests', 'pytz', 'requests_cache']
)
