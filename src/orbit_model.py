# from random import randrange
# from copy import deepcopy
# random.seed(1)
import math

TIMESTEP = 1
# screen is square
# sizes are relative to the screen: -1 to 1


class Planet:
    g_const = 1  # arbitrary gravity constant

    def __init__(self, name, orbit, color, radius_px, init_angle):
        self.name = name
        self.orbit = orbit
        self.color = color
        self.radius_px = radius_px
        self.angle = init_angle
        self.x = orbit * math.cos(math.radians(self.angle))
        self.y = orbit * math.sin(math.radians(self.angle))
        self.period = self.calc_period()

    def __str__(self):
        return f"{self.name}"

    def calc_period(self):
        # update velocity vector according to orbit radius
        return Planet.g_const * math.sqrt(self.orbit ** 3)

    def advance(self):
        self.angle = (self.angle + TIMESTEP / self.period * 360) % 360
        self.x = self.orbit * math.cos(math.radians(self.angle))
        self.y = self.orbit * math.sin(math.radians(self.angle))
        # print(f"{self.angle} deg, x={self.x}, y={self.y}")

    def increase_orbit(self, is_increase):
        orbit_step = 0.05
        if is_increase:
            self.orbit += orbit_step
        else:
            self.orbit -= orbit_step
        self.period = self.calc_period()


class GameModel:

    def __init__(self):
        self.star = Planet("Star", 0, (255, 204, 51), 5, 0)
        Planet.g_const = 100
        self.ships = \
            [Planet("ship1", 0.6, (56, 56, 56), 1, 0),
             Planet("debris", 0.3, (230, 230, 230), 2, 90)]
        # TODO random initial orbits

    def change_orbit(self, is_increase):
        self.ships[0].increase_orbit(is_increase)

    def update(self):
        for ship in self.ships:
            ship.calc_period()
            ship.advance()

    def reset(self):
        pass


if __name__ == '__main__':
    model = GameModel()
    for _ in range(100):
        model.update()
        print(model.ships[0].angle)
