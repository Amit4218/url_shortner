"""
This file contains the class ShortUrl which provide all the
necessary function that the application might require.

"""

import random
from string import digits, ascii_letters
from config import database_actions


class ShortUrl:

    def generate_unique_url(self, length: int = 7) -> str:
        """Generates a unique list of 7 characters by default, for unique url"""

        while True:

            unique_url = "".join(random.choices(ascii_letters + digits, k=length))

            exits = database_actions.check_if_generated_str_exists(unique_url)

            if not exits:
                return unique_url


url_actions = ShortUrl()
