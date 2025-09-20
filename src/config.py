from dataclasses import dataclass
from typing import Tuple
import numpy as np


@dataclass
class OrbitConfig:
    """Configuration for orbit rendezvous game"""

    # Display
    screen_width: int = 600
    screen_height: int = 600
    fps: int = 10

    # Physics
    mu = 3.986e14  # Earth gravity parameter (m^3/s^2) μ=GM
    # satellite at circular LEO at 7000 km
    debris_position = np.array([7000e3, 0.0])
    debris_velocity = np.array([0.0, 7546.0])
    # ship at circular LEO at 9000 km
    ship_position = np.array([4000e3, 0.0])
    ship_velocity = np.array([0.0, 9982.0])
    dt = 100  # index parameter of orbit speed

    # Visual
    planet_radius: float = 0.08  # ratio of screen size of [-1, 1]
    ship_radius: float = 0.02  # ratio of screen size of [-1, 1]
    debris_radius: float = 0.02  # ratio of screen size of [-1, 1]
    epochs_radius: float = 0.01  # ratio of screen size of [-1, 1]

    planet_color: Tuple[int, int, int] = (255, 204, 51)  # Yellow
    ship_color: Tuple[int, int, int] = (56, 56, 200)  # Blueish
    debris_color: Tuple[int, int, int] = (230, 100, 100)  # Reddish
    epochs_color: Tuple[int, int, int] = (0, 255, 0)  # Green

    world_radius = 10000e3  # display in each direction

    # Controls
    delta_v: float = 100
    paused: bool = False
