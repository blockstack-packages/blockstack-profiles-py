"""
Blockstack Profiles
==============

"""

from setuptools import setup, find_packages

setup(
    name='blockstack-profiles',
    version='0.1.1',
    url='https://github.com/blockstack/blockstack-profiles-py',
    license='MIT',
    author='Blockstack Developers',
    author_email='hello@onename.com',
    description="""Library for blockstack profile generation and validation""",
    keywords='bitcoin blockchain blockstack profile schema',
    packages=find_packages(),
    zip_safe=False,
    install_requires=[
        'jsontokens>=0.0.2',
        'keylib>=0.0.2',
        'keychain>=0.1.4',
        'zone-file>=0.1.2'
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
