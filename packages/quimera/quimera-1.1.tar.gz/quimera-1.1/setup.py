from setuptools import setup, find_packages
import codecs
import os

VERSION = '1.1'
DESCRIPTION = 'Pentesting Tool Kit'
LONG_DESCRIPTION = 'Pentesting and OSINT Tool Kit for Ethical Hacking'

# Setting up
setup(
    name="quimera",
    version=VERSION,
    author="Mauricio Rossi (MRossiDEV)",
    author_email="<mrossiph@gmail.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=[],
    keywords=['python', 'wifi', 'osint', 'hacking', 'network'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)