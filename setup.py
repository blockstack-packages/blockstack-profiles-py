#!/usr/bin/env python
"""
Blockstack Profiles
==============

"""

from setuptools import setup, find_packages

setup(
    name='blockstack-profiles',
    version='0.4.4',
    url='https://github.com/blockstack/blockstack-profiles-py',
    license='MIT',
    author='Blockstack Developers',
    author_email='hello@onename.com',
    description="""Library for blockstack profile generation and validation""",
    keywords='bitcoin blockchain blockstack profile schema',
    packages=find_packages(),
    zip_safe=False,
    install_requires=[
        'cryptography>=1.2.3',
        'jsontokens>=0.0.2',
        'keylib>=0.0.5',
        'blockstack-zones>=0.1.6'
    ],
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet',
        'Topic :: Security :: Cryptography',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
