from setuptools import setup, find_packages
import sys, os

version = '0.1'

setup(
    name='ckanext-galileo',
    version=version,
    description="This plugin logs all requests to the Galileo analytics platform.  Requires a Galileo service token.",
    long_description='''
    ''',
    classifiers=[], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
    keywords='galileo analytics',
    author='Brock Anderson',
    author_email='brock@bandersgeo.ca',
    url='',
    license='',
    packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
    namespace_packages=['ckanext', 'ckanext.galileo'],
    include_package_data=True,
    zip_safe=False,
    install_requires=['mashape-analytics'],
    entry_points='''
        [ckan.plugins]
        galileo=ckanext.galileo.plugin:GalileoPlugin
    ''',
)
