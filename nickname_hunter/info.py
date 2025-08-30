# Project: nickname_hunter
# License: GNU Affero General Public License v3.0 only
#
# This file is part of the nickname_hunter project.
#
# Copyright (C) 2025 unelected
#
# This program is free software: you can redistribute it and/or modify it under
# the terms of the GNU Affero General Public License as published by the Free Software
# Foundation, version 3.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program. If not, see <https://www.gnu.org/licenses/>.
#
# See the LICENSE file in the root of this repository for the full license text.

"""
Provides utilities for displaying project information.

This module contains helper functions to render the ASCII art logo
using pyfiglet, retrieve the project version from version.py, and
print both in a formatted way.

Typical Usage Example:
    from utils.info import get_info
    get_info()
"""
import importlib.util
import pyfiglet

from pathlib import Path
from importlib.machinery import ModuleSpec
from types import ModuleType


def get_info() -> None:
    """
    Display project logo and version information.

    Retrieves the ASCII logo string via get_logo() and attempts to load
    the version.py module via get_version(). The collected data is then
    passed to print_data() for formatted output.

    Returns:
        None: This function does not return a value. It prints information
        to the console.
    """
    logo: str = get_logo()
    module: str | None = get_version()
    print_data(logo, module)
    return None

def get_version() -> str | None:
    """
    Retrieve the project version from version.py.

    Loads and executes the version.py module dynamically using
    mod importlib. If the module contains a __version__ attribute,
    its value is returned. Otherwise, None is returned.

    Returns:
        str | None: The version string if found, otherwise None.
    """
    version_file = Path("./version.py")
    spec: ModuleSpec | None = importlib.util.spec_from_file_location("version", version_file)
    if isinstance(spec, ModuleSpec) and spec.loader:
        module: ModuleType = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return getattr(module, "__version__", None)
    return None

def get_logo() -> str:
    """
    Return the ASCII art logo of the project.

    Renders the text Nickname Hunter using the slant font
    from the pyfiglet library.

    Returns:
        str: Generated ASCII art logo.
    """
    ascii_banner: str = pyfiglet.figlet_format("Nickname Hunter", font = "slant")
    return ascii_banner

def print_data(logo: str, version: str | None) -> None:
    """Print the project logo and version information.

    If a version string is provided, it is printed below the logo.
    Otherwise, only the logo is printed.

    Args:
        logo (str): The ASCII art logo of the project.
        version (str | None): The project version string, or None if
        unavailable.

    Returns:
        None: This function prints output to the console and does not return a value.
    """
    if isinstance(version, str):
        print(f"{logo}\nversion: {version}")
    else:
        print(logo)
    print(f"\n")
    return None
