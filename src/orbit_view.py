import pygame

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)


class Orbit_renderer:

    def __init__(self, width=600, height=600):
        self.width = width
        self.height = height
        pygame.init()
        self.window = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Orbit Rendezvous")
        self.bg_img = pygame.image.load("stars-galaxy.jpg")

    def draw_ship(self, ship):
        pygame.draw.circle(self.window, ship.color, (ship.x, ship.y), ship.radius_px)

    def render(self, model):
        self.window.fill(BLACK)  # TODO remove and see if it shows background correctly
        self.window.blit(self.bg_img, (0, 0))

        self.draw_ship(model.star)
        for ship in model.ships:
            self.draw_ship(ship)

        pygame.display.flip()

    def draw(self):
        pygame.draw.circle(self.window, self.color, (int(self.width / 2 + self.x_km / SCALE - self.radius_px / 2),
                                             int(self.height / 2 + self.y_km / SCALE - self.radius_px / 2)), self.radius_px)
        self.window.blit(self.bg_img, (0, 0))
        for planet in planets:
            planet.draw()
