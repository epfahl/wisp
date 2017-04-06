from setuptools import setup, find_packages

setup(
    name='wisp',
    version='0.1',
    description='a tiny static lisp interpreter',
    url='https://github.com/epfahl/wisp',
    author='Eric Pfahl',
    packages=find_packages(),
    install_requires=['pyparsing', 'toolz'])
