# Copyright (c) 2024 ZS
# Copyright (c) 2025 unelected
#
# This file is part of the project and is licensed under the MIT License.
# See the LICENSE file in the root of this repository for full license text.

"""Bot automation for nickname tracking and claiming in Zafia Online.

This module defines the Bot class which connects to the Zafia Online service, monitors
a list of tracked accounts, and uses predefined entertainer accounts to claim nicknames
as they become available.

Typical usage example:
    bot = Bot()
    asyncio.run(bot.main_function())
"""
import asyncio
import logging

from zafiaonline.structures import PacketDataKeys
from zafiaonline.main import Client

from accounts_data import AccountsData


# Script powered by zakovskiy && forked by unelected
class Bot:
    """
    A bot that manages account tracking and nickname claiming.

    This class handles connecting to a service, monitoring user accounts for nickname 
    changes, and automatically signing in with predefined entertainer accounts to 
    claim nicknames as needed.

    Attributes:
        main (Client): The main client used for connection and user operations.
        _accounts_data (AccountsData): Manages loaded account data, including entertainers and tracked accounts.
        _entertainers (list[list[str]]): A list of available entertainer accounts in the format [email, password].
        _trackeds (list[list[str]]): A list of tracked user accounts for monitoring.
    """
    def __init__(self):
        """Initializes the bot with client and account data."""
        self.main: Client = Client()
        self._accounts_data: AccountsData = AccountsData()
        self._accounts_data.get_accounts()
        self._entertainers: list[list[str]] = self._accounts_data.entertainers
        self._trackeds: list[list[str]] = self._accounts_data.trackeds

    async def main_function(self, sleep_time: float = .5) -> None:
        """
        Continuously monitors and processes tracked accounts.

        Establishes a connection via the main client, then enters an infinite loop
        where it periodically checks tracked accounts and handles updates.
        A delay is applied between each iteration to control execution frequency.

        Args:
            sleep_time (float): Delay in seconds between account checks. Defaults to 0.5.

        Raises:
            Exception: Propagates any unexpected exceptions from `check_accounts()`
                if not handled internally.
        """
        await self.main.create_connection()
        while True:
            await self.check_accounts()
            await asyncio.sleep(sleep_time)

    async def check_accounts(self, sleep_time: int = 2) -> None:
        """
        Checks and processes tracked accounts for nickname changes.

        Iterates through the list of tracked accounts. For each account, attempts to
        retrieve its current state and nickname. If a new nickname is detected or
        differs from the stored one, it triggers the nickname entry process and updates
        or removes the tracked entry accordingly.

        Args:
            sleep_time (int): Delay in seconds between processing each account.
                Defaults to 2.

        Raises:
            AttributeError: If `get_account()` returns None.
            Exception: Propagates exceptions related to malformed account data.
        """
        for i in range(len(self._trackeds)):
            try:
                tracked: list[str] = self._trackeds[i]
            except Exception as e:
                logging.error(f"ошибка {e}")
                continue
            account: dict | None = await self.get_account(tracked)
            if account is None:
                raise AttributeError("account is None")

            try:

                presearched_nickname: str | None = account.get(PacketDataKeys.USER, None)
                if presearched_nickname is not None:
                    searched_nickname: str | None = presearched_nickname[PacketDataKeys.USERNAME] or None
                else:
                    continue

            except Exception as e:
                logging.critical(f"username in account does not exist, {e}")
                raise

            if tracked[1] == "" and searched_nickname is not None:
                self._trackeds[i][1] = searched_nickname
                logging.info(f"nickname: {searched_nickname}")
                logging.info('~set nickname')

            elif searched_nickname != tracked[1]: # if nickname is not old nickname
                await self.enter_nickname(tracked[1])
                del self._trackeds[i]
            await asyncio.sleep(sleep_time)
        self._trackeds[:] = [trackeded for trackeded in self._trackeds if trackeded is not None]

    async def fetch_user(self, user_id: str) -> dict | None:
        """
        Fetches user data by user ID.

        Sends an asynchronous request to retrieve user data using the given `user_id`.
        If a ValueError occurs during the request, delegates handling to
        `handle_search_error()`.

        Args:
            user_id (str): The ID of the user to fetch.

        Returns:
            dict | None: The user data if found, otherwise None.
        """
        try:
            return await self.main.get_user(user_id)
        except (ValueError) as e:
            return await self.handle_search_error(e)

    async def handle_search_error(self, error: Exception, sleep_time: int = 10) -> None:
        """
        Handles an error that occurred during user search.

        Logs the error message, waits for a specified amount of time, and then returns None.

        Args:
            error (Exception): The exception raised during the user search.
            sleep_time (int, optional): Time to wait before retrying. Defaults to 10 seconds.

        Returns:
            None
        """
        logging.error(f"Ошибка при поиске игрока: {error}")
        await asyncio.sleep(sleep_time)
        return None

    async def get_account(self, tracked: list[str]) -> dict | None:
        """
        Retrieves a user account based on the tracked data.

        Checks if the `tracked` list is not empty, then requests the user
        data from the API using the user ID. If the list is empty or the
        request fails, returns None.

        Args:
            tracked (list[str]): A list containing the user ID and possibly other data.

        Returns:
            dict | None: A dictionary with account data if found, otherwise None.
        """
        if not tracked:
            logging.error("Список tracked пуст, невозможно получить пользователя")
            return None

        return await self.fetch_user(tracked[0])


    async def sign_in_with_entertainer(self, index: int) -> None:
        """
        Signs in using an entertainer account from the list by index.

        If the `index` is valid and the `entertainers` list is not empty,
        this method signs in with the specified account and removes it from
        the list to avoid reuse.

        Args:
            index (int): The index of the account in the entertainers list.
        """
        if not self._entertainers:
            logging.error("Нет доступных учетных записей")
            return

        if 0 <= index <= len(self._entertainers):
            await self.main.sign_in(self._entertainers[index][0], self._entertainers[index][1])
            del self._entertainers[index]
        else:
            logging.error("Попытка входа с несуществующей учетной записью")

    async def set_nickname(self, nickname: str) -> None:
        """
        Sets the user's nickname and logs the action.

        Args:
            nickname (str): The nickname to assign to the user.
        """
        await self.main.username_set(nickname)
        logging.info(f"Заняли ник {nickname}")

    async def enter_nickname(self, nickname: str, 
                             priority: bool = False,
                             priority_nickname: str = "") -> None:
        """
        Signs in with a selected entertainer account and sets the given nickname.

        If priority is enabled and the given nickname matches the priority nickname,
        a specific entertainer account is used. Otherwise, a default account is selected.

        Args:
            nickname (str): The nickname to be claimed.
            priority (bool, optional): Whether to prioritize a specific nickname. Defaults to False.
            priority_nickname (str, optional): The nickname to prioritize. Defaults to an empty string.
        """
        if priority and priority_nickname:
            if nickname == priority_nickname:
                index: int = 0
            else:
                index: int = 1
        else:
            index: int = 0

        await self.sign_in_with_entertainer(index)
        await self.set_nickname(nickname)


if __name__ == "__main__":
    logging.basicConfig(level = logging.INFO,
                        format = "%(asctime)s - %(levelname)s - %(message)s",
                        datefmt = "%H:%M:%S")
    bot: Bot = Bot()

    try:
        asyncio.run(bot.main_function(.5))
    except KeyboardInterrupt:
        logging.info("успешный выход из программы")
