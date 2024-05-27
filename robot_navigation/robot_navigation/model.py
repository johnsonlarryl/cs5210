import math
from dataclasses import dataclass
import numpy as np
from typing import List

from robot_navigation.util import validate_iterations


@dataclass(frozen=True)
class Reward:
    row: int
    column: int
    value: float


@dataclass(frozen=True)
class MazeConfig:
    rows: int
    columns: int
    rewards: List[Reward]


@dataclass
class Maze:
    map: np.ndarray


@dataclass(frozen=True)
class PolicyConfig:
    maze: Maze
    iterations: int
    living_reward: int
    rewards: List[Reward]
    intended_direction: float = 0.90
    unintended_direction: float = 0.10
    discount_factor: float = 0.9
    convergence_threshold: float = 0.01

    def __post_init__(self):
        validate_iterations(self.iterations)






