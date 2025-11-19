"""
This file contains the class ShortUrl which provide all the
necessary function that the application might require.

"""

import random
from string import digits, ascii_letters


class ShortUrl:

    def generate_unique_url(self, length: int = 7) -> str:
        """Generates a unique list of characters, for unique url

        ### Args:
            - length (int, optional): \n
            length of the string wish to be generated. Defaults to 7.
        """

        unique_url = ""

        character_list = random.choices(ascii_letters + digits, k=length)
        for char in character_list:
            unique_url += char

        return unique_url
