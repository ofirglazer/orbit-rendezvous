import pygame
from orbit_model import GameModel
from orbit_controller import GameController
from orbit_view import Orbit_renderer


def main():
    """Main entry point"""
    screen_width, screen_height = 600, 600
    clock = pygame.time.Clock()
    fps = 2

    model = GameModel()
    view = Orbit_renderer(screen_width, screen_height)
    controller = GameController(model, view)

    running = True
    paused = False

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:  # Pause/unpause
                    paused = not paused
                elif event.key == pygame.K_ESCAPE:
                    running = False
            controller.handle_event(event)  # Controller processes input

        if not paused:
            controller.update()  # Controller updates Model based on game logic
            view.render(model)  # View renders the Model's state
            # Update Display and Control Frame Rate
            clock.tick(fps)


if __name__ == '__main__':
    main()
