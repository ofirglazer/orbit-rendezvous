# from random import randrange
# from copy import deepcopy
# random.seed(1)
import math
from src.config import OrbitConfig

# screen is square
# sizes are relative to the screen: -1 to 1


class Planet:
    g_const = 1  # init arbitrary gravity constant

    def __init__(self, name, orbit, color, radius_ratio, init_angle):
        self.name = name
        self.orbit = orbit
        self.color = color
        self.radius_ratio = radius_ratio
        self.angle = init_angle
        self.x = orbit * math.cos(math.radians(self.angle))
        self.y = orbit * math.sin(math.radians(self.angle))
        self.period = self.calc_period()

    def __str__(self):
        return f"{self.name}"

    def calc_period(self):
        # update velocity vector according to orbit radius
        return Planet.g_const * math.sqrt(self.orbit ** 3)

    def advance(self, dt):
        self.angle = (self.angle + dt / self.period * 360) % 360
        self.x = self.orbit * math.cos(math.radians(self.angle))
        self.y = self.orbit * math.sin(math.radians(self.angle))
        # print(f"{self.angle} deg, x={self.x}, y={self.y}")

    def increase_orbit(self, delta_v):
        self.orbit += delta_v
        self.period = self.calc_period()


class GameModel:

    def __init__(self, config: OrbitConfig = None):
        self.config = config or OrbitConfig()

        self.star = Planet("Star", 0, self.config.planet_color, self.config.planet_radius, 0)
        Planet.g_const = 100
        self.ships = \
            [Planet("ship1", self.config.ship_orbit, self.config.ship_color, self.config.ship_radius, 0),
             Planet("debris", self.config.debris_orbit, self.config.debris_color, self.config.debris_radius, 90)]
        self.collided_with_star = False
        self.caught_satellite = False
        # TODO random initial orbits

    def change_orbit(self, is_increase):
        if is_increase:
            self.ships[0].increase_orbit(self.config.orbit_change_step)
        else:
            self.ships[0].increase_orbit(-self.config.orbit_change_step)

    def update(self):
        for ship in self.ships:
            ship.calc_period()
            ship.advance(self.config.dt)
        self.collided_with_star = self.detect_collision(self.ships[0], self.star)
        self.caught_satellite = self.detect_collision(self.ships[0], self.ships[1])

    def detect_collision(self, ship1, ship2):
        is_collision = ((ship1.x - ship2.x) ** 2 + (ship1.y - ship2.y) ** 2 <=
                        (ship1.radius_ratio + ship2.radius_ratio) ** 2)
        return is_collision

    def reset(self):
        pass


if __name__ == '__main__':
    model = GameModel()
    for _ in range(100):
        model.update()
        print(model.ships[0].angle)
