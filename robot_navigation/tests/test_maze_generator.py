import numpy as np
from typing import Callable

from robot_navigation.generator import MazeGenerator
from robot_navigation.model import MazeConfig, Reward


def test_generate_maze(get_maze: Callable):
    expect_maze = get_maze(1)
    positive_exit_reward = Reward(row=0, column=3, value=1.0)
    negative_exit_reward = Reward(row=1, column=3, value=-1.0)
    obstacle = Reward(row=1, column=1, value=np.nan)
    rewards = [positive_exit_reward, negative_exit_reward, obstacle]
    config = MazeConfig(rows=3, columns=4, rewards=rewards)

    result_maze = MazeGenerator.generate_maze(config)

    assert np.array_equal(result_maze.map, expect_maze.map, equal_nan=True)

