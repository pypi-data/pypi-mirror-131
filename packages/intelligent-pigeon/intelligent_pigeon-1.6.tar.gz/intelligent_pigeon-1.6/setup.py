from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

VERSION = '1.6'
DESCRIPTION = 'Intelligent Pigeon is a program made for IOT, by which you can detect Object from a Image and send to a server'

with open('requirement.txt','r') as f:
    required = f.read().splitlines()

# Setting up
setup(
    name="intelligent_pigeon",
    version=VERSION,
    author="Ujjwal Kar",
    url="https://github.com/ujjwalkar0/intelligent_pigeon",
    author_email="ujjwalkar21@gmail.com",
    description=DESCRIPTION,
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    install_requires = required,
    data_files=[('yolov4-custom.cfg')],
    keywords=['YoLo','Object Detector','Artificial Intelligence','Internet of Things'],
    classifiers=[
        # "Development Status :: 1 - Planning",
        # "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        # "Operating System :: Microsoft :: Windows",
    ],
    python_requires='>=3.6',
    py_modules=['intelligent_pigeon'],
    scripts=['bin/pigeon'],
)
