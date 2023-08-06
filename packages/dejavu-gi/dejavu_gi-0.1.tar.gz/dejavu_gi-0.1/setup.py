from setuptools import setup, Extension
from setuptools.command.install import install
from distutils.core import setup, Extension
import subprocess
import os

class CustomInstall(install):
    def run(self):
        install.run(self)


module = Extension('dejavu_gi.libdejavu_api',
                   sources = ['./src/dejavu_gi/dejavu_api_impl.cpp', './src/dejavu_gi/schreier_shared.cpp',
                   	       './src/dejavu_gi/utility.cpp', './src/dejavu_gi/schreier_sequential.cpp',
                   	       './src/dejavu_gi/refinement.cpp', './src/dejavu_gi/naurng.cpp',
                   	       './src/dejavu_gi/parser.cpp', './src/dejavu_gi/invariant.cpp',],
                   include_dirs = ['./src/dejavu_gi/'],
                   extra_compile_args=[],
                   extra_link_args=[])

setup(
    name='dejavu_gi',
    version='0.1',
    packages=['dejavu_gi'],
    install_requires=[
    ],
    cmdclass={'install': CustomInstall},
    include_package_data=True,
    ext_modules=[module],
)
