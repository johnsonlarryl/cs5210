import numpy as np
from typing import Callable

from robot_navigation.model import PolicyConfig
from robot_navigation.optimizer import MazeOptimizer


def test_maze_optimizer_iteration_k_2(get_policy_config: PolicyConfig, get_maze: Callable):
    policy_config = get_policy_config(2)
    expect_maze = get_maze(2)
    result_maze = MazeOptimizer.optimize_maze(policy_config)
    result_maze = np.round(result_maze.map, 2)

    assert np.array_equal(result_maze, expect_maze.map, equal_nan=True)


def test_maze_optimizer_iteration_k_3(get_policy_config: PolicyConfig, get_maze: Callable):
    policy_config = get_policy_config(3)
    expect_maze = get_maze(3)
    result_maze = MazeOptimizer.optimize_maze(policy_config)
    result_maze = np.round(result_maze.map, 2)

    assert np.array_equal(result_maze, expect_maze.map, equal_nan=True)


def test_maze_optimizer_iteration_k_100(get_policy_config: PolicyConfig, get_maze: Callable):
    policy_config = get_policy_config(100)
    expect_maze = get_maze(100)
    result_maze = MazeOptimizer.optimize_maze(policy_config)
    result_maze = np.round(result_maze.map, 2)

    assert np.array_equal(result_maze, expect_maze.map, equal_nan=True)






