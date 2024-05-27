import numpy as np
from typing import List

from robot_navigation.model import Maze, MazeConfig


class MazeGenerator:
    @staticmethod
    def generate_maze(maze_config: MazeConfig) -> Maze:
        maze_array = MazeGenerator._init_maze(maze_config.rows, maze_config.columns)

        for reward in maze_config.rewards:
            maze_array[reward.row][reward.column] = reward.value

        maze = Maze(map=np.array(maze_array))

        return maze

    @staticmethod
    def _init_maze(rows: int, columns: int) -> List[List[float]]:
        return [[0 for _ in range(columns)] for _ in range(rows)]
