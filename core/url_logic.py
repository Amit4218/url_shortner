"""
This file contains the class ShortUrl which provide all the
necessary function that the application might require.

"""

import random
from string import digits, ascii_letters


class ShortUrl:

    def __init__(self, database_actions) -> None:
        self.database_actions = database_actions

    def generate_unique_url(self, length: int = 7) -> str:
        """Generates a unique list of 7 characters by default, for unique url"""

        while True:

            unique_url = "".join(random.choices(ascii_letters + digits, k=length))

            exits = self.database_actions.check_if_generated_str_exists(unique_url)

            if not exits:
                return unique_url

        