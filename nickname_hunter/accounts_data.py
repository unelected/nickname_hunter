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
Loads account credentials and tracked user data from a JSON file.

This module defines the AccountsData class, which provides methods for
loading entertainer accounts and tracked user IDs from a local "data.json" file.
These data are used to sign in and monitor nickname availability in the bot system.

Typical usage example:
    data = AccountsData()
    data.get_accounts()
    print(data.entertainers)
"""
import json

from typing import Any


class AccountsData:
    """
    Stores and loads account data used for nickname management.

    Attributes:
        entertainers: A list of credentials used to sign in and occupy nicknames.
        trackeds: A list of user IDs whose nicknames should be monitored.
    """
    def __init__(self) -> None:
        """
        Initialize the AccountsData instance with empty attributes.
        """
        self.entertainers: list[list[str]]
        self.trackeds: list[list[str]]

    def get_accounts(self) -> None:
        """
        Load entertainer and tracked account data from a JSON file.

        This method reads the "data.json" file and sets the following attributes
        """
        with open("data.json", encoding = "utf-8") as f:
            data: dict[str, Any] = json.load(f)

        self.entertainers = data["entertainers"]
        # data from accounts that should be occupied by nicknames.

        self.trackeds = data["trackeds"]
        # ids of users that should be occupied.
