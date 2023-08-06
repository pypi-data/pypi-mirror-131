from setuptools import setup, find_packages
import codecs
import os

VERSION = '0.0.1'
DESCRIPTION = 'basic ex package'
LONG_DESCRIPTION = 'stfu long'

# Setting up
setup(
    name="Ex12pack",
    version=VERSION,
    author="Omry",
    author_email="pinhas592@gmail.com",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description="long_description",
    packages=find_packages(),
    install_requires=[],
    keywords=['python', 'video', 'stream', 'video stream', 'camera stream', 'sockets'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)