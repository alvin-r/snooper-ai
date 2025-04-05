"""
Setup file for snooper-ai.
"""
import os
import re
import setuptools


def read_file(filename):
    with open(filename) as file:
        return file.read()


version = re.findall(r"__version__ = '(.*)'",
                     read_file(os.path.join('snooper_ai', '__init__.py')))[0]

setuptools.setup(
    name='snooper-ai',
    version=version,
    author='Alvin Ryanputra',
    author_email='alvin.ryanputra@gmail.com',
    description='Debug your Python code with AI assistance',
    long_description=read_file('README.md'),
    long_description_content_type='text/markdown',
    url='https://github.com/alvin-r/snooper-ai',  # Update with your repo
    packages=setuptools.find_packages(exclude=['tests*']),  # This will find all packages including subpackages
    install_requires=[
        'anthropic>=0.18.0',
        'click>=8.1.7',
        'rich>=13.7.0',
        'openai>=1.12.0',
        'tomlkit>=0.12.4',
    ],
    extras_require={
        'tests': {
            'pytest',
        },
    },
    entry_points={
        'console_scripts': [
            'snoop=snooper_ai.cli:cli',
        ],
    },
    classifiers=[
        'Environment :: Console',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.7',
)
