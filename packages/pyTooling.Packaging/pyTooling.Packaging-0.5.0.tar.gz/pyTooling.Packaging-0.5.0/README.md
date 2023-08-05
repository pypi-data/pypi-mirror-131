[![Sourcecode on GitHub](https://img.shields.io/badge/pyTooling-pyTooling.Packaging-323131.svg?logo=github&longCache=true)](https://GitHub.com/pyTooling/pyTooling.Packaging)
[![Sourcecode License](https://img.shields.io/pypi/l/pyTooling.Packaging?logo=GitHub&label=code%20license)](LICENSE.md)
[![GitHub tag (latest SemVer incl. pre-release)](https://img.shields.io/github/v/tag/pyTooling/pyTooling.Packaging?logo=GitHub&include_prereleases)](https://GitHub.com/pyTooling/pyTooling.Packaging/tags)
[![GitHub release (latest SemVer incl. including pre-releases)](https://img.shields.io/github/v/release/pyTooling/pyTooling.Packaging?logo=GitHub&include_prereleases)](https://GitHub.com/pyTooling/pyTooling.Packaging/releases/latest)
[![GitHub release date](https://img.shields.io/github/release-date/pyTooling/pyTooling.Packaging?logo=GitHub)](https://GitHub.com/pyTooling/pyTooling.Packaging/releases)
[![Dependents (via libraries.io)](https://img.shields.io/librariesio/dependents/pypi/pyTooling.Packaging?logo=librariesdotio)](https://GitHub.com/pyTooling/pyTooling.Packaging/network/dependents)  
[![GitHub Workflow - Build and Test Status](https://img.shields.io/github/workflow/status/pyTooling/pyTooling.Packaging/Unit%20Testing,%20Coverage%20Collection,%20Package,%20Release,%20Documentation%20and%20Publish?label=Pipeline&logo=GitHub%20Actions&logoColor=FFFFFF)](https://GitHub.com/pyTooling/pyTooling.Packaging/actions/workflows/Pipeline.yml)
[![Codacy - Quality](https://img.shields.io/codacy/grade/e8a1b6e33d564f82927235e17fb26e93?logo=Codacy)](https://www.codacy.com/manual/pyTooling/pyTooling.Packaging)
[![Codacy - Coverage](https://img.shields.io/codacy/coverage/e8a1b6e33d564f82927235e17fb26e93?logo=Codacy)](https://www.codacy.com/manual/pyTooling/pyTooling.Packaging)
[![Codecov - Branch Coverage](https://img.shields.io/codecov/c/github/pyTooling/pyTooling.Packaging?logo=Codecov)](https://codecov.io/gh/pyTooling/pyTooling.Packaging)
[![Libraries.io SourceRank](https://img.shields.io/librariesio/sourcerank/pypi/pyTooling.Packaging?logo=librariesdotio)](https://libraries.io/github/pyTooling/pyTooling.Packaging/sourcerank)  
[![PyPI](https://img.shields.io/pypi/v/pyTooling.Packaging?logo=PyPI&logoColor=FBE072)](https://pypi.org/project/pyTooling.Packaging/)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/pyTooling.Packaging?logo=PyPI&logoColor=FBE072)
![PyPI - Status](https://img.shields.io/pypi/status/pyTooling.Packaging?logo=PyPI&logoColor=FBE072)
[![Libraries.io status for latest release](https://img.shields.io/librariesio/release/pypi/pyTooling.Packaging?logo=librariesdotio)](https://libraries.io/github/pyTooling/pyTooling.Packaging)
[![Requires.io](https://img.shields.io/requires/github/pyTooling/pyTooling.Packaging)](https://requires.io/github/pyTooling/pyTooling.Packaging/requirements/?branch=main)  
[![Documentation License](https://img.shields.io/badge/doc%20license-CC--BY%204.0-green?logo=readthedocs)](doc/Doc-License.rst)
[![Documentation - Read Now!](https://img.shields.io/badge/doc-read%20now%20%E2%9E%9A-blueviolet?logo=readthedocs)](https://pyTooling.GitHub.io/pyTooling.Packaging)

# pyTooling.Packaging

A set of helper functions to describe a Python package for setuptools.

## Features
* Ease single-sourcing of information
  * Read and parse `README` file for `setup.py`
  * Read and parse `requirements.txt` file for `setup.py`
  * Read `__xxx__` variables from Python source code for `setup.py` and `conf.py` (Sphinx)
* Assemble parameters for Setuptools' `setup(...)`
  * Provide enhancements for GitHub hosted Python packages.


## List of Helper Functions

* `loadReadmeFile`
* `loadRequirementsFile`
* `extractVersionInformation`

## List of Package Descriptions

* `DescribePythonPackage`
* `DescribePythonPackageHostedOnGitHub`


## Contributors

* [Patrick Lehmann](https://GitHub.com/Paebbels) (Maintainer)
* [Unai Martinez-Corral](https://GitHub.com/umarcor)
* [and more...](https://GitHub.com/pyTooling/pyTooling.Packaging/graphs/contributors)


## License

This Python package (source code) licensed under [Apache License 2.0](LICENSE.md).  
The accompanying documentation is licensed under [Creative Commons - Attribution 4.0 (CC-BY 4.0)](doc/Doc-License.rst).


-------------------------

SPDX-License-Identifier: Apache-2.0
