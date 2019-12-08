
class Player:
    """
    Author: Michael Harmon
    Description: This is the player class that will be created when the player enters
    their information into the GUI.
    Last Date Modified: 12/8/2019
    """

    def __init__(self, first_name, last_name, gamer_name, games_won=0):
        valid_name_characters = set("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'-")
        if not (valid_name_characters.issuperset(first_name) and valid_name_characters.issuperset(last_name)):
            raise ValueError
        if gamer_name == '':
            raise ValueError
        self._first_name = first_name
        self._last_name = last_name
        self._gamer_name = gamer_name
        self._games_won = games_won

    # getters
    def get_first_name(self):
        return self._first_name

    def get_last_name(self):
        return self._last_name

    def get_gamer_name(self):
        return self._gamer_name

    def get_games_won(self):
        return self._games_won

    # setters
    def set_first_name(self, first_name):
        self._first_name = first_name

    def set_last_name(self, last_name):
        self._last_name = last_name

    def set_gamer_name(self, gamer_name):
        self._gamer_name = gamer_name

    def set_games_won(self, games_won):
        self._games_won = games_won
