# main.py - Entry point of the application
"""
Orbit Rendezvous game
===============================

This is an orbit rendezvous game, inspired by Sinclair ZX81 classic game.

MVC Architecture:
- Model (orbit_model.py): Contains game state, logic, and data structures
- View (orbit_view.py): Handles all rendering and visual presentation
- Controller (orbit_controller.py): Manages input handling and coordinates model/view
- Main (main.py): Entry point that initializes and starts the game

To run: python main.py

Controls:
- Menu: SPACE to start, Q to quit
- Game: UP and DOWN arrow keys increase or decrease orbit, SPACE to pause, ESC for quit
"""
# TODO limited maneuvers
# TODO random initial orbits
from orbit_controller import OrbitController


def main():
    """Main entry point"""
    print(__doc__)

    controller = OrbitController()
    controller.run()


if __name__ == "__main__":
    main()
