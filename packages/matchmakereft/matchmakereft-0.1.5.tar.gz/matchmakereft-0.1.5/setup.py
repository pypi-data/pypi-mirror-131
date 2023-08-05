import os
from distutils.core import setup
from setuptools import find_packages
from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='matchmakereft',
    version='0.1.5',
    description='Automated matching of general models onto general effective field theories',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='Adrian Carmona, Achilleas Lazopoulos, Pablo Olgoso, Jose Santiago',
    author_email='adrian@ugr.es, lazopoulos@itp.phys.ethz.ch, pablolgoso@ugr.es, jsantiago@ugr.es', 
    url='https://ftae.ugr.es/matchmakereft/',
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    packages=find_packages(),
    install_requires=[
          'requests',
          'setuptools',
          'yolk3k',
          'colorama',
          'tqdm',
      ],
    entry_points={
    'console_scripts': [
        'matchmakereft = matchmakereft.libs.MatchMaker:MM',
        ],
    },
    license='Creative Commons Attribution-Noncommercial-Share Alike license',
    package_data = {'matchmakereft': ['core/*',
        'docs/manual.pdf',
        'docs/UpdateNotes.txt',
        'data/*',
        ]}#,
)
