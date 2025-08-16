import pytest
from src.orbit_model import Planet, GameModel


class TestPlanet:
    def test_planet_initialization(self):
        planet = Planet("test_planet", 0.56, (255, 0, 0), 4, 45)

        # test init
        assert planet.name == "test_planet"
        assert planet.orbit == 0.56
        assert planet.color == (255, 0, 0)
        assert planet.radius_px == 4
        assert planet.angle == 45

        assert planet.x == pytest.approx(0.396, 0.01)
        assert planet.y == pytest.approx(0.396, 0.01)

    def test_planet_advancement(self):
        # test advance
        planet = Planet("test_planet", 0.56, (255, 0, 0), 4, 45)
        x = planet.x
        y = planet.y
        planet.advance()
        assert planet.x != x
        assert planet.y != y

    def test_orbit_change(self):
        # test advance
        planet = Planet("test_planet", 0.5, (255, 0, 0), 4, 0)
        prev_orbit = planet.orbit
        prev_period = planet.period
        planet.increase_orbit(True)
        assert planet.orbit > prev_orbit
        assert planet.period > prev_period

        planet.increase_orbit(False)
        planet.increase_orbit(False)  # twice decrease to be smaller than prev_
        assert planet.orbit < prev_orbit
        assert planet.period < prev_period


class TestGameModel:
    def test_gamemodel_initialization(self):

        # test init
        game = GameModel()
        assert isinstance(game.ships[0], Planet)
        assert isinstance(game.ships[1], Planet)

    def test_gamemodel_orbit_change(self):
        # test change orbit
        game = GameModel()
        prev_orbit = game.ships[0].orbit
        game.change_orbit(True)
        assert game.ships[0].orbit > prev_orbit
        game.change_orbit(False)
        game.change_orbit(False)  # twice decrease to be smaller than prev_
        assert game.ships[0].orbit < prev_orbit
