"""setup file for places geocoding package"""
from setuptools import setup, find_packages
import setuptools
from pathlib import Path
from distutils.core import setup
from distutils.extension import Extension
from Cython.Build import cythonize
import numpy as np
import importlib.machinery
this_directory = Path(__file__).parent

VERSION = '0.3.1'
DESCRIPTION = 'Package for Places Geocoding API service'

extensions = [
    Extension(name='address_packet', sources=["places_geocode/app/dprk_copy/address_packet.pyx"], include_dirs=[np.get_include()]),
    Extension('certainty_search', ["places_geocode/app/dprk_copy/certainty_search.pyx"]),
    Extension('check_address_length', ['places_geocode/app/dprk_copy/check_address_length.pyx']),
    Extension('check_dups', ['places_geocode/app/dprk_copy/check_dups.pyx']),
    Extension('check_lat_long_length', ['places_geocode/app/dprk_copy/check_lat_long_length.pyx']),
    Extension('coordinate_conv_package', ['places_geocode/app/dprk_copy/coordinate_conv_package.pyx']),
    Extension('create_convex_array', ['places_geocode/app/dprk_copy/create_convex_array.pyx']),
    Extension('create_convex_elastic', ['places_geocode/app/dprk_copy/create_convex_elastic.pyx']),
    Extension('executor_unpack', ['places_geocode/app/dprk_copy/executor_unpack.pyx']),
    Extension('null_parameters', ['places_geocode/app/dprk_copy/null_parameters.pyx']),
    Extension('radius_arr', ['places_geocode/app/dprk_copy/radius_arr.pyx']),
    Extension('reverse_spreadsheet', ['places_geocode/app/dprk_copy/reverse_spreadsheet.pyx']),
    Extension('spreadsheet_c', ['places_geocode/app/dprk_copy/spreadsheet_c.pyx']),
    Extension('TFIDF_max', ['places_geocode/app/dprk_copy/TFIDF_max.pyx']),
    Extension('TFIDF_max_elastic', ['places_geocode/app/dprk_copy/TFIDF_max_elastic.pyx']),
    Extension('TFIDF_upgraded', ['places_geocode/app/dprk_copy/TFIDF_upgraded.pyx']),
    Extension('zip_coordinate', ['places_geocode/app/dprk_copy/zip_coordinate.pyx']),
    Extension('zip_coordinates_elastic', ['places_geocode/app/dprk_copy/zip_coordinates_elastic.pyx'])
]

# Setting up
setup(
    name="places_geocode",
    version=VERSION,
    author="Martin Mashalov",
    author_email="hello@places.place",
    description=DESCRIPTION,
    long_description=open('/Users/martinmashalov/Documents/places_geocoding_package/README.md').read(),
    long_description_content_type="text/markdown",
    packages=['places_geocode', 'places_geocode/app', 'places_geocode/Logs', 'places_geocode/app/models', 'places_geocode/app/CythonOperations', 'places_geocode/app/CythonOperations/places_geocode/app/dprk_copy'],
    license="MIT",
    ext_modules=cythonize(extensions,
                          build_dir="places_geocode/app/CythonOperations"),
    include_dirs=np.get_include(),
    url="https://medium.com/p/10cc24c34505/edit",
    install_requires=['pymongo', 'numpy', 'pandas', 'sklearn', 'dependency_injector', 'pydantic', 'fastapi', 'cython',
                      'state_machine'],
    keywords=['python',
              'geocoding',
              'forward geocoding',
              'reverse geocoding',
              'radius loading',
              'loading radius',
              'autocomplete',
              'places of interest',
              'POI'
              ],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "License :: Free for non-commercial use",
        "Intended Audience :: Information Technology",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)