#!/usr/bin/env python
# Learn more: https://github.com/kennethreitz/setup.py
# import os
# import sys

# from codecs import open

from setuptools import setup, find_packages
# from setuptools.command.test import test as TestCommand

# here = os.path.abspath(os.path.dirname(__file__))

# class PyTest(TestCommand):
#     user_options = [('pytest-args=', 'a', "Arguments to pass into py.test")]

#     def initialize_options(self):
#         TestCommand.initialize_options(self)
#         try:
#             from multiprocessing import cpu_count
#             self.pytest_args = ['-n', str(cpu_count()), '--boxed']
#         except (ImportError, NotImplementedError):
#             self.pytest_args = ['-n', '1', '--boxed']

#     def finalize_options(self):
#         TestCommand.finalize_options(self)
#         self.test_args = []
#         self.test_suite = True

#     def run_tests(self):
#         import pytest

#         errno = pytest.main(self.pytest_args)
#         sys.exit(errno)

# 'setup.py publish' shortcut.
# if sys.argv[-1] == 'publish':
#     os.system('python setup.py sdist bdist_wheel')
#     os.system('twine upload dist/*')
#     sys.exit()

# packages = ['requests']

# requires = [
#     'charset_normalizer~=2.0.0; python_version >= "3"',
#     'chardet>=3.0.2,<5; python_version < "3"',
#     'idna>=2.5,<3; python_version < "3"',
#     'idna>=2.5,<4; python_version >= "3"',
#     'urllib3>=1.21.1,<1.27',
#     'certifi>=2017.4.17'
# ]

install_requires = [
    "numpy",
    "pandas",
    "seaborn",
    "matplotlib",
    "leafmap",
    "ipyleaflet",
    "tqdm",
    "geopandas",
    "earthengine-api",
    "eecmip5",
    "joblib",
]

# test_requirements = [
#     'pytest-httpbin==0.0.7',
#     'pytest-cov',
#     'pytest-mock',
#     'pytest-xdist',
#     'PySocks>=1.5.6, !=1.5.7',
#     'pytest>=3'
# ]

# about = {}
# with open(os.path.join(here, 'requests', '__version__.py'), 'r', 'utf-8') as f:
#     exec(f.read(), about)

with open(file='README.md', mode='r', encoding='utf-8') as f:
    readme = f.read()

setup(
    name="climate-resilience",
    version="0.1.8",
    description="Download, Preprocessing, and Visualization code for climate resilience data.",
    long_description=readme,
    long_description_content_type="text/markdown",
    author=[
        "Satyarth Praveen",
        "Zexuan Xu",
    ],
    author_email="satyarth@lbl.gov",
    url="https://github.com/satyarth934/lbnl-climate-resilience",
    packages=find_packages(
        where="src",
    ),
#     package_data={'': ['LICENSE', 'NOTICE']},
    package_dir={"": "src"},
#     include_package_data=True,
    python_requires=">=3.6",
    install_requires=install_requires,
#     license=about['__license__'],
#     zip_safe=False,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
#     cmdclass={'test': PyTest},
#     tests_require=test_requirements,
#     extras_require={
#         'security': [],
#         'socks': ['PySocks>=1.5.6, !=1.5.7'],
#         'socks:sys_platform == "win32" and python_version == "2.7"': ['win_inet_pton'],
#         'use_chardet_on_py3': ['chardet>=3.0.2,<5']
#     },
    project_urls={
        "Bug Tracker": "https://github.com/satyarth934/lbnl-climate-resilience/issues",
#         'Documentation': 'https://requests.readthedocs.io',
        "Source": "https://github.com/satyarth934/lbnl-climate-resilience",
    },
)