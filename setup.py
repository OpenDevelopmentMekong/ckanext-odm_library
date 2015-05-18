from setuptools import setup, find_packages
import sys, os

version = '1.2.0'

setup(
    name='ckanext-odm_library',
    version=version,
    description="OD Mekong CKAN's library extension",
    long_description='''
    ''',
    classifiers=[], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
    keywords='',
    author='Alex Corbi',
    author_email='mail@lifeformapps.com',
    url='http://www.lifeformapps.com',
    license='AGPL3',
    packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
    namespace_packages=['ckanext', 'ckanext.odm_library'],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        # -*- Extra requirements: -*-
    ],
    entry_points='''
        [ckan.plugins]
        odm_library=ckanext.odm_library.plugin:OdmLibraryPlugin
    ''',
)
