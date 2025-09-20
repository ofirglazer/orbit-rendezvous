from dataclasses import dataclass
from typing import Tuple


@dataclass
class OrbitConfig:
    """Configuration for orbit rendezvous game"""

    # Display
    screen_width: int = 600
    screen_height: int = 600
    fps: int = 10

    # Physics
    g_const = 1  # arbitrary gravity constant
    dt = 0.5  # index parameter of orbit speed
    ship_orbit = 0.6
    debris_orbit = 0.5

    # Visual
    planet_radius: float = 0.08  # ratio of screen size of [-1, 1]
    ship_radius: float = 0.02  # ratio of screen size of [-1, 1]
    debris_radius: float = 0.02  # ratio of screen size of [-1, 1]

    planet_color: Tuple[int, int, int] = (255, 204, 51)  # Yellow
    ship_color: Tuple[int, int, int] = (56, 56, 200)  # Blueish
    debris_color: Tuple[int, int, int] = (230, 100, 100)  # Reddish

    # Controls
    orbit_change_step: float = 0.05
    paused: bool = False
