import os

from setuptools import setup, find_packages, Extension


bitap_extension = Extension(
    'lhc.misc.bitap',
    ['lib/bitap/bitapmodule.cpp', 'lib/bitap/bitap.cpp'],
    include_dirs=['lib/bitap'])

with open('README.rst', encoding='utf-8') if os.path.exists('README.rst') else \
        open('README.md', encoding='utf-8') as fileobj:
    long_description = fileobj.read()

setup(
    name='lhc-python',
    version='2.5.0',
    author='Liam H. Childs',
    author_email='liam.h.childs@gmail.com',
    packages=find_packages(exclude=['docs', 'test*']),
    scripts=[],
    url='https://github.com/childsish/lhc-python',
    license='LICENSE.txt',
    description='My python library of classes and functions that help me work',
    long_description=long_description,
    long_description_content_type='text/markdown',
    install_requires=['sortedcontainers >= 2.1.0', 'numpy >= 1.18.1', 'pysam >= 0.15.4'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Science/Research',
        'Topic :: Scientific/Engineering :: Bio-Informatics'],
    ext_modules=[bitap_extension],
    include_package_data=True,
    package_data={'': ['data/gc.prt', 'Emolwt.dat']},
)
