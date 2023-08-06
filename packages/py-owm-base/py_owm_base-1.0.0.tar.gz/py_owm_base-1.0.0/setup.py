from setuptools import setup, find_packages
import codecs
import os

# Setting up
setup(
    name="py_owm_base",
    version='1.0.0',
    author="Yura Ghazaryan",
    author_email="ghazaryanyura98@gmail.com",
    url='https://github.com/GhazaryanYura/open-weather-maps',
    license='MIT',
    description='A basic package.',
    long_description = 'This package send requests, return json file. And working with him.',
    packages = find_packages(),
    keywords=['python'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)