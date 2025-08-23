import pygame

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)


class OrbitRenderer:

    def __init__(self, width=600, height=600):
        self.width = width
        self.height = height
        pygame.init()
        self.window = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Orbit Rendezvous")
        self.bg_img = pygame.image.load("stars-galaxy.jpg")

    def draw_ship(self, ship):
        x = self.width // 2 * (1 + ship.x)
        y = self.height // 2 * (1 + ship.y)
        radius = ship.radius_ratio * self.width // 2
        pygame.draw.circle(self.window, ship.color, (x, y), radius)

    def render(self, model):
        self.window.blit(self.bg_img, (0, 0))

        self.draw_ship(model.star)
        for ship in model.ships:
            self.draw_ship(ship)

        pygame.display.flip()
