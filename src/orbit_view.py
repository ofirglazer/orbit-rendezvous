import pygame
from src.config import OrbitConfig
from math import cos, sin

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)


class OrbitRenderer:

    def __init__(self, config: OrbitConfig = None):
        self.config = config or OrbitConfig()

        self.width = self.config.screen_width
        self.height = self.config.screen_height
        pygame.init()
        self.window = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Orbit Rendezvous")
        self.bg_img = pygame.image.load("stars-galaxy.jpg")

    def draw_epochs(self, ship):
        # apoapsis
        apsis, apsis_angle = ship.apoapsis()
        apo_x = self.width // 2 * (1 + apsis * cos(apsis_angle) / self.config.world_radius)
        apo_y = self.width // 2 * (1 + apsis * sin(apsis_angle) / self.config.world_radius)
        pygame.draw.circle(self.window, self.config.epochs_color, (apo_x, apo_y),
                           self.config.epochs_radius * self.width // 2)
        # periapsis
        apsis, apsis_angle = ship.periapsis()
        apo_x = self.width // 2 * (1 + apsis * cos(apsis_angle) / self.config.world_radius)
        apo_y = self.width // 2 * (1 + apsis * sin(apsis_angle) / self.config.world_radius)
        pygame.draw.circle(self.window, self.config.epochs_color, (apo_x, apo_y),
                           self.config.epochs_radius * self.width // 2)

    def draw_ship(self, ship):
        if ship.name == 'Star':
            r = [0.0, 0.0]
        else:
            r, v = ship.get_state()
        x = self.width // 2 * (1 + r[0] / self.config.world_radius)
        y = self.height // 2 * (1 + r[1] / self.config.world_radius)
        radius = ship.radius_ratio * self.width // 2
        pygame.draw.circle(self.window, ship.color, (x, y), radius)
        if ship.name == 'ship1':
            self.draw_epochs(ship)

    def render(self, model):
        self.window.blit(self.bg_img, (0, 0))

        self.draw_ship(model.star)
        for ship in model.ships:
            self.draw_ship(ship)

        pygame.display.flip()
