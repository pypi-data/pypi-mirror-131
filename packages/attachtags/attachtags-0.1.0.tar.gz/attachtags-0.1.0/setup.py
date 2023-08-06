#!/usr/bin/env python

"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = [
    "setuptools>=42",
    "wheel"]

test_requirements = ['pytest>=3', ]

setup(
    name='attachtags',
    version='0.1.0',
    author="Gongzi Yu",
    author_email='1920781522@qq.com',
    description="This is a tool to help manage your files by attaching \
        some tags.",
    long_description=readme + '\n\n' + history,
    url='https://github.com/Gongzi-Yu/attachtags',
    project_urls={
        "Bug Tracker": "https://github.com/Gongzi-Yu/attachtags/issues"
        },
    classifiers=[
        'Programming Language :: Python :: 3.7',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent'
    ],
    license="MIT license",
    packages=find_packages(include=['attachtags', 'attachtags.*']),
    python_requires='>=3.7.3',
    zip_safe=False,
    install_requires=requirements,
    tests_require=test_requirements,
    include_package_data=True,
    keywords='attachtags',
    test_suite='tests',
    entry_points={
        'console_scripts': [
            'attachtags=attachtags.cli:main',
        ],
    },
)
