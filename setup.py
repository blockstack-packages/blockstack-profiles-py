"""
Blockstack Profiles
==============

"""

from setuptools import setup, find_packages

setup(
    name='blockstack-profiles',
    version='0.0.2',
    url='https://github.com/blockstack/blockstack-profiles-py',
    license='MIT',
    author='Blockstack Developers',
    author_email='hello@onename.com',
    description="""Library for blockstack profile generation""",
    keywords='bitcoin blockchain blockstack',
    packages=find_packages(),
    zip_safe=False,
    install_requires=[
        'PyJWT==1.4.0',
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
