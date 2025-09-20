import pygame

from src.orbit_model import GameModel
from src.orbit_view import OrbitRenderer
from src.config import OrbitConfig


class OrbitController:
    """Handles user input and coordinates between model and view."""

    def __init__(self, config: OrbitConfig = None):

        self.config = config or OrbitConfig()
        self.model = GameModel(self.config)
        self.view = OrbitRenderer(self.config)
        self.clock = pygame.time.Clock()
        self.fps = 10
        self.running = True
        self.paused = self.config.paused

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

            # Handle input
            self.handle_events()

            if not self.paused:

                # Update game logic
                self.model.update()

                # Render
                self.view.render(self.model)

                # exit conditions
                if self.model.collided_with_star:
                    self.running = False
                    print("Collided with star, game over")
                if self.model.caught_satellite:
                    self.running = False
                    print("Caught the satellite, you win")

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
