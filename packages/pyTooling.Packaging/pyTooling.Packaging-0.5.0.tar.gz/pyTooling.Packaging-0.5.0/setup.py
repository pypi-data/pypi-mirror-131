# =============================================================================
#             _____           _ _               ____            _               _
#  _ __  _   |_   _|__   ___ | (_)_ __   __ _  |  _ \ __ _  ___| | ____ _  __ _(_)_ __   __ _
# | '_ \| | | || |/ _ \ / _ \| | | '_ \ / _` | | |_) / _` |/ __| |/ / _` |/ _` | | '_ \ / _` |
# | |_) | |_| || | (_) | (_) | | | | | | (_| |_|  __/ (_| | (__|   < (_| | (_| | | | | | (_| |
# | .__/ \__, ||_|\___/ \___/|_|_|_| |_|\__, (_)_|   \__,_|\___|_|\_\__,_|\__, |_|_| |_|\__, |
# |_|    |___/                          |___/                             |___/         |___/
# =============================================================================
# Authors:            Patrick Lehmann
#
# Package installer:  A set of helpers to implement a text user interface (TUI) in a terminal.
#
# License:
# ============================================================================
# Copyright 2021-2021 Patrick Lehmann - Bötzingen, Germany
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#		http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# SPDX-License-Identifier: Apache-2.0
# ============================================================================
#
from os.path import abspath
from sys     import path as sys_path

sys_path.insert(0, abspath('./pyTooling'))

from pathlib    import Path
from Packaging  import DescribePythonPackageHostedOnGitHub


gitHubNamespace =        "pyTooling"
packageName =            "pyTooling.Packaging"
packageDirectory =       packageName.replace('.', '/')
packageInformationFile = Path(f"{packageDirectory}/__init__.py")
pythonVersions =         ["3.8", "3.9", "3.10"]

DescribePythonPackageHostedOnGitHub(
	packageName=packageName,
	description="A set of helper functions to describe a Python package for setuptools.",
	gitHubNamespace=gitHubNamespace,
	sourceFileWithVersion=packageInformationFile,
	developmentStatus="beta",
	pythonVersions=pythonVersions
)
