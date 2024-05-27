import numpy as np
from matplotlib.axes import Axes
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from matplotlib.colors import LinearSegmentedColormap
from typing import List

from robot_navigation.generator import Maze, MazeGenerator
from robot_navigation.model import MazeConfig, PolicyConfig
from robot_navigation.optimizer import MazeOptimizer


class MazeVisualizer:
    @staticmethod
    def visualize_map_iterations(maze_config: MazeConfig,
                      living_reward: int,
                      intended_direction: float,
                      unintended_direction: float,
                      k: List[int],
                      chart_per_row: int = 4) -> None:

        n_charts = len(k)
        viz_rows = n_charts // chart_per_row if n_charts % chart_per_row == 0 else n_charts // chart_per_row + 1
        viz_columns = min(n_charts, chart_per_row)

        fig, axes = plt.subplots(viz_rows, viz_columns, figsize=(5 * viz_columns, 5 * viz_rows))

        if n_charts == 1:
            axes = [axes]
        else:
            axes = axes.flatten()

        i = 0

        for idx, ax in enumerate(axes[:n_charts]):
            maze = MazeGenerator.generate_maze(maze_config)

            if i == 0:
                k_i = 1
            elif i > 0:
                k_i = k[i]
                policy_config = PolicyConfig(maze=maze,
                                             rewards=maze_config.rewards,
                                             iterations=k_i,
                                             living_reward=living_reward,
                                             intended_direction=intended_direction,
                                             unintended_direction=unintended_direction)
                maze = MazeOptimizer.optimize_maze(policy_config)

            MazeVisualizer._generate_chart(maze, k_i, ax)
            i += 1

        plt.show()

    @staticmethod
    def _generate_chart(maze: Maze, k: int, ax: Axes) -> None:
        maze_map = maze.map
        colors = ["red", "green", "darkgreen"]
        boundaries = [np.nanmin(maze_map), 0, 0.5, np.nanmax(maze_map)]
        cmap = mcolors.LinearSegmentedColormap.from_list("", colors)
        cmap.set_bad("grey")  # nans

        maze_map = maze.map
        norm = mcolors.BoundaryNorm(boundaries, cmap.N, clip=True)

        cax = ax.imshow(maze_map, cmap=cmap, norm=norm)
        ax.set_title(f"k={k}")
        plt.colorbar(cax)

        for (row, column), probability in np.ndenumerate(maze_map):
            if not np.isnan(probability):
                ax.text(column, row, f"{probability:.2f}", ha="center", va="center", color="white")






