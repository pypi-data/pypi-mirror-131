#!/usr/bin/env python

"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = [ ]

test_requirements = [ ]

setup(
    author="Florian K.",
    author_email='37000563+flok@users.noreply.github.com',
    python_requires='>=3.6',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    description="Parsing OpenDRIVE format in Python",
    install_requires=requirements,
    license="Apache Software License 2.0",
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords='pyopendrive',
    name='pyopendrive',
    packages=find_packages(include=['pyopendrive', 'pyopendrive.*']),
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/flok/pyopendrive',
    version='0.0.1',
    zip_safe=False,
)
