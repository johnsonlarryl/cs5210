import math
import numpy as np
import pytest
from typing import Callable

from robot_navigation.generator import MazeGenerator
from robot_navigation.model import Maze, MazeConfig, PolicyConfig, Reward


@pytest.fixture
def get_maze() -> Callable:
    mazes = {1: np.array([[0.0, 0.0, 0.0, 1.0],
                          [0.0, np.nan, 0.0, -1.0],
                          [0.0, 0.0, 0.0, 0.0]]),
             2: np.array([[0.0, 0.0, 0.72, 1.0],
                          [0.0, np.nan, 0.0, -1.0],
                          [0.0, 0.0, 0.0, 0.0]]),
             3: np.array([[0.0, 0.52, 0.78, 1.0],
                          [0.0, np.nan, 0.43, -1.0],
                          [0.0, 0.0, 0.0, 0.0]]),
             100: np.array([[0.64, 0.74, 0.85, 1.0],
                           [0.57, np.nan, 0.57, -1.0],
                           [0.49, 0.43, 0.48, 0.28]])
             }

    def maze_func(k: int):
        return Maze(map=mazes[k])

    return maze_func


@pytest.fixture
def get_policy_config(get_maze: Callable) -> PolicyConfig:
    def policy_config_func(k: int):
        positive_exit_reward = Reward(row=0, column=3, value=1.0)
        negative_exit_reward = Reward(row=1, column=3, value=-1.0)
        obstacle = Reward(row=1, column=1, value=np.nan)
        rewards = [positive_exit_reward, negative_exit_reward, obstacle]
        maze_config = MazeConfig(rows=3, columns=4, rewards=rewards)

        maze = MazeGenerator.generate_maze(maze_config)

        return PolicyConfig(maze=maze,
                            rewards=rewards,
                            iterations=k,
                            living_reward=0,
                            intended_direction=0.80,
                            unintended_direction=0.10,
                            convergence_threshold=math.pow(10, -16))

    return policy_config_func
