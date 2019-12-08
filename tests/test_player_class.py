import unittest
from class_definitions.player_class import Player


class MyTestCase(unittest.TestCase):
    def setUp(self):
        self.player = Player("Michael", "Harmon", "Gamer10")

    def tearDown(self):
        del self.player

    def test_object_created_required_attributes(self):
        player = Player('Michael', 'Harmon', 'Gamer10')
        assert player.get_first_name() == 'Michael'
        assert player.get_last_name() == 'Harmon'
        assert player.get_gamer_name() == 'Gamer10'
        assert player.get_games_won() == 0

    def test_object_created_optional_attributes(self):
        player = Player('Michael', 'Harmon', 'Gamer10', 10)
        assert player.get_first_name() == 'Michael'
        assert player.get_last_name() == 'Harmon'
        assert player.get_gamer_name() == 'Gamer10'
        assert player.get_games_won() == 10

    def test_object_not_created_error_first_name(self):
        with self.assertRaises(ValueError):
            player = Player('Michael12', 'Harmon', 'Gamer10')

    def test_object_not_created_error_last_name(self):
        with self.assertRaises(ValueError):
            player = Player('Michael', 'Harmon01', 'Gamer10')

    def test_object_not_created_error_gamer_name(self):
        with self.assertRaises(ValueError):
            player = Player('Michael', 'Harmon01', '')


if __name__ == '__main__':
    unittest.main()
