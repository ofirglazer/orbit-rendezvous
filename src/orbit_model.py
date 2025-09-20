# from random import randrange
# from copy import deepcopy
# random.seed(1)
import numpy as np
# import math
from src.config import OrbitConfig

# screen is square
# sizes are relative to the screen: -1 to 1


class Planet:

    def __init__(self, name, position, velocity, mu, color, radius_ratio):
        self.r = np.array(position, dtype=float)
        self.v = np.array(velocity, dtype=float)
        self.mu = mu
        self.name = name
        self.color = color
        self.radius_ratio = radius_ratio
        # self.period = self.calc_period() #TODO remove function and calls

    def __str__(self):
        return f"{self.name}"

    def elements_from_state(self):
        x, y = self.r
        vx, vy = self.v
        r_norm = np.linalg.norm(self.r)
        v_norm = np.linalg.norm(self.v)
        energy = v_norm ** 2 / 2 - self.mu / r_norm
        a = -self.mu / (2 * energy)
        h = x * vy - y * vx
        e = np.sqrt(1 - h ** 2 / (self.mu * a))
        return a, e, h

    def anomaly_from_state(self, e):
        x, y = self.r
        vx, vy = self.v
        # True anomaly
        theta = np.arctan2(y, x)
        # Eccentric anomaly
        E = 2 * np.arctan2(
            np.tan(theta / 2) * np.sqrt((1 - e) / (1 + e)),
            1
        )
        if E < 0:  # keep in [0, 2pi)
            E += 2 * np.pi
        # Mean anomaly
        M = E - e * np.sin(E)
        return theta, E, M

    def calc_period(self):
        # update velocity vector according to orbit radius
        return Planet.g_const * math.sqrt(self.orbit ** 3)

    def solve_kepler(self, M, e, tol=1e-10, max_iter=50):
        E = M if e < 0.8 else np.pi
        for _ in range(max_iter):
            f = E - e * np.sin(E) - M
            fprime = 1 - e * np.cos(E)
            dE = -f / fprime
            E += dE
            if abs(dE) < tol:
                break
        return E

    def advance(self, dt):
        a, e, h = self.elements_from_state()
        theta0, E0, M0 = self.anomaly_from_state(e)
        n = np.sqrt(self.mu / a ** 3)

        # advance mean anomaly
        M = M0 + n * dt
        E = self.solve_kepler(M % (2 * np.pi), e)

        # position in orbital plane
        r_norm = a * (1 - e * np.cos(E))
        x = a * (np.cos(E) - e)
        y = a * np.sqrt(1 - e ** 2) * np.sin(E)

        # scale to inertial coordinates (2D, so aligned already)
        self.r = np.array([x, y])

        # velocity from vis-viva + derivatives
        vx = -np.sin(E) * np.sqrt(self.mu * a) / r_norm
        vy = np.sqrt(1 - e ** 2) * np.cos(E) * np.sqrt(self.mu * a) / r_norm
        self.v = np.array([vx, vy])

        # print(f"{self.angle} deg, x={self.x}, y={self.y}")

    def increase_orbit(self, delta_v):
        self.orbit += delta_v
        self.period = self.calc_period()


class GameModel:

    def __init__(self, config: OrbitConfig = None):
        self.config = config or OrbitConfig()

        self.star = Planet("Star", (0.0, 0.0), (0.0, 0.0), self.config.mu, self.config.planet_color, self.config.planet_radius)
        # TODO remove Planet.g_const = self.config.g_const
        self.ships = \
            [Planet("ship1", self.config.ship_position, self.config.ship_velocity, self.config.mu, self.config.ship_color, self.config.ship_radius),
             Planet("debris", self.config.debris_position, self.config.debris_velocity, self.config.mu, self.config.debris_color, self.config.debris_radius)]
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
            # ship.calc_period()
            ship.advance(self.config.dt)
        #TODO self.collided_with_star = self.detect_collision(self.ships[0], self.star)
        #TODO self.caught_satellite = self.detect_collision(self.ships[0], self.ships[1])

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
