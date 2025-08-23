import pygame

from src.orbit_model import GameModel
from src.orbit_view import OrbitRenderer


class OrbitController:
    """Handles user input and coordinates between model and view."""

    def __init__(self, screen_width=600, screen_height=600):

        self.model = GameModel()
        self.view = OrbitRenderer(screen_width, screen_height)
        self.clock = pygame.time.Clock()
        self.fps = 10
        self.running = True
        self.paused = False

    def handle_events(self):
        """Process all pygame events"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:  # toggle Pause/unpause
                    self.paused = not self.paused
                elif event.key == pygame.K_ESCAPE:
                    self.running = False
                elif event.key == pygame.K_DOWN:
                    self.model.change_orbit(False)
                elif event.key == pygame.K_UP:
                    self.model.change_orbit(True)

    def run(self):
        """Main game loop."""

        while self.running:
            if not self.paused:

                # Handle input
                self.handle_events()

                # Update game logic
                self.model.update()

                # Render
                self.view.render(self.model)

                self.clock.tick(self.fps)
        self.cleanup()

    @staticmethod
    def cleanup():
        """Clean up resources."""
        pygame.quit()
        print("Game ended")


if __name__ == '__main__':
    width = 600
    height = 400
    radius = 10
    # main(num_particles=num_particles, width=width, height=height, gravity=gravity, radius=radius)
