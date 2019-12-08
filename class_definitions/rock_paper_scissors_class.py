import random


class RockPaperScissors:
    """
    Author: Michael Harmon
    Description: This is the rock paper scissors class that will be created when a new game starts.
    It will generated a random choice between rock paper or scissors and return it to the game.
    Last Date Modified: 12/8/2019
    """
    def __init__(self):
        self.get_random_choice()

    def get_random_choice(self):
        return random.choice(['rock', 'paper', 'scissors'])
