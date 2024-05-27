import copy
import numpy as np
from typing import Tuple

from robot_navigation.model import Maze, PolicyConfig
from robot_navigation.util import validate_iterations


class MazeOptimizer:
    @staticmethod
    def optimize_maze(policy_config: PolicyConfig) -> Maze:
        old_maze = policy_config.maze
        new_maze = copy.deepcopy(policy_config.maze)
        validate_iterations(policy_config.iterations)

        i = 2

        while MazeOptimizer.can_continue_processing(i, policy_config):
            for row in range(old_maze.map.shape[0]):
                for column in range(old_maze.map.shape[1]):
                    if MazeOptimizer.is_valid_state(policy_config, row, column):
                        left, right, up, down = MazeOptimizer.get_states(old_maze.map, row, column)
                        u_prime = policy_config.living_reward + \
                            (policy_config.discount_factor *
                             max(policy_config.intended_direction * up + policy_config.unintended_direction * left + policy_config.unintended_direction * right,  # up
                                 policy_config.intended_direction * left + policy_config.unintended_direction * up + policy_config.unintended_direction * down,  # left
                                 policy_config.intended_direction * down + policy_config.unintended_direction * left + policy_config.unintended_direction * right,  # down
                                 policy_config.intended_direction * right + policy_config.unintended_direction * up + policy_config.unintended_direction * down))  # right

                        new_maze.map[row][column] = u_prime

            if abs(np.nansum(new_maze.map) - np.nansum(old_maze.map)) < policy_config.convergence_threshold:
                return new_maze
            else:
                old_maze = new_maze
                new_maze = copy.deepcopy(old_maze)
                i += 1

        return new_maze

    @staticmethod
    def can_continue_processing(i: int, policy_config: PolicyConfig) -> bool:
        return i < policy_config.iterations + 1

    @staticmethod
    def is_valid_state(policy_config: PolicyConfig,
                       row: int,
                       column: int) -> bool:
        rewards = policy_config.rewards

        for reward in rewards:
            if reward.row == row and reward.column == column:
                return False

        return True

    @staticmethod
    def get_states(maze_map: np.ndarray,
                   row: int,
                   column: int) -> Tuple[float, float, float, float]:
        left = MazeOptimizer.get_left_state(maze_map, row, column)
        right = MazeOptimizer.get_right_state(maze_map, row, column)
        up = MazeOptimizer.get_up_state(maze_map, row, column)
        down = MazeOptimizer.get_down_state(maze_map, row, column)

        return left, right, up, down

    @staticmethod
    def get_up_state(maze_map: np.ndarray,
                     row: int,
                     column: int) -> float:
        next_row = row - 1
        next_column = column

        if (row > 0) and (not MazeOptimizer.is_obstacle(maze_map, next_row, next_column)):
            return maze_map[next_row][next_column]
        else:
            return MazeOptimizer.get_current_state(maze_map, row, column)

    @staticmethod
    def get_down_state(maze_map: np.ndarray,
                       row: int,
                       column: int) -> float:
        next_row = row + 1
        next_column = column

        if (row < maze_map.shape[0] - 1) and (not MazeOptimizer.is_obstacle(maze_map, next_row, next_column)):
            return maze_map[next_row, next_column]
        else:
            return MazeOptimizer.get_current_state(maze_map, row, column)

    @staticmethod
    def get_left_state(maze_map: np.ndarray,
                       row: int,
                       column: int) -> float:
        next_row = row
        next_column = column - 1

        if (column > 0) and (not MazeOptimizer.is_obstacle(maze_map, next_row, next_column)):
            return maze_map[next_row, next_column]
        else:
            return MazeOptimizer.get_current_state(maze_map, row, column)

    @staticmethod
    def get_right_state(maze_map: np.ndarray,
                        row: int,
                        column: int) -> float:
        next_row = row
        next_column = column + 1

        if (column < maze_map.shape[1] - 1) and (not MazeOptimizer.is_obstacle(maze_map, next_row, next_column)):
            return maze_map[next_row, next_column]
        else:
            return MazeOptimizer.get_current_state(maze_map, row, column)

    @staticmethod
    def is_obstacle(maze_map: np.ndarray,
                    row: int,
                    column: int) -> bool:
        return np.isnan(MazeOptimizer.get_current_state(maze_map, row, column))

    @staticmethod
    def get_current_state(maze_map: np.ndarray,
                          row: int,
                          column: int) -> float:
        return maze_map[row][column]




