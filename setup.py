"""
Blockstack Profiles
==============

"""

from setuptools import setup, find_packages

setup(
    name='blockstack-schema',
    version='0.1.2',
    url='https://github.com/blockstack/blockstack-schema-py',
    license='MIT',
    author='Blockstack Developers',
    author_email='hello@onename.com',
    description="""Library for blockstack schema + profile generation and validation""",
    keywords='bitcoin blockchain blockstack',
    packages=find_packages(),
    zip_safe=False,
    install_requires=[
        'jwtpy==0.1.0',
        'keychain==0.1.4',
        'pybitcoin==0.9.8'
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
