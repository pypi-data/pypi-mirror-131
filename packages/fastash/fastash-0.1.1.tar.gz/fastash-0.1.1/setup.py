#!/usr/bin/env python3

# Set this to True to enable building extensions using Cython.
# Set it to False to build extensions from the C file (that
# was previously created using Cython).
# Set it to 'auto' to build with Cython if available, otherwise
# from the C file.
USE_CYTHON = 'auto'

import sys

import numpy

from setuptools import setup
from setuptools import Extension

__version__ = "0.1.1"

if USE_CYTHON:
    try:
        from Cython.Distutils import build_ext
    except ImportError:
        if USE_CYTHON=='auto':
            USE_CYTHON=False
        else:
            raise

cmdclass = { }
ext_modules = [ ]

if USE_CYTHON:
    ext_modules += [
        Extension("fastash.ashfunc",
                  sources=["cython/ashfunc.pyx"],
                  include_dirs=[numpy.get_include()],
                  language="c++",
                  ),
    ]
    cmdclass.update({ 'build_ext': build_ext })
else:
    ext_modules += [
        Extension("fastash.ashfunc", 
                  sources=["cython/ashfunc.cpp"],
                  include_dirs=[numpy.get_include()],
                  language="c++"),
    ]

setup(
    name='fastash',
    version=__version__,
    description='Fast Averages Shifted Histogram',
    author='François-Rémi Mazy',
    author_email='francois-remi.mazy@inria.fr',
    url='https://gitlab.inria.fr/fmazy/fastash',
    packages=[ 'fastash', ],
    package_dir={
        'fastash' : 'fastash',
    },
    cmdclass = cmdclass,
    ext_modules=ext_modules,
    install_requires=[
            'numpy>=1.19.2',
        ],

    long_description=open('README.md').read(),

    license="BSD 3-Clause License",
    classifiers=[
        'Development Status :: 1 - Planning',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Cython',
        'Topic :: Scientific/Engineering :: Mathematics',
    ],
    keywords='averaged shifted histograms kde ash density estimation kernel',
)

