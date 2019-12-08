import unittest
from class_definitions.rock_paper_scissors_class import RockPaperScissors


class MyTestCase(unittest.TestCase):
    def setUp(self):
        self.game = RockPaperScissors()

    def tearDown(self):
        del self.game

    def test_object_created(self):
        game = RockPaperScissors()
        assert game.get_random_choice() == 'rock' or 'paper' or 'scissors'


if __name__ == '__main__':
    unittest.main()
