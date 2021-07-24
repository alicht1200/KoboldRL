import random
import numpy as np
from typing import Tuple

class MazeCorridors:

    def __init__(self, width: int, height: int):
        self.width, self.height = width , height
        self.tiles = np.full((width,height), fill_value= 0, order="F")

    def generate_maze(self) -> None:
        x = random.randint(1, self.width - 2)
        y = random.randint(1, self.height - 2)
        self.tiles[x][y] = 1
        open_cells = [(x, y)]

        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        while open_cells:
            x, y = random.choice(open_cells)

            random.shuffle(directions)
            for dx, dy in directions:
                if (x + dx > 0) and (x + dx < self.width - 1) and (y + dy > 0) and (y + dy < self.height - 1):
                    if self.are_neighbors_blocked(x=x + dx, y=y + dy, direction=(dx, dy)):
                        open_cells.append((x + dx, y + dy))
                        self.tiles[x + dx][y + dy] = 0
                        break
            else:
                open_cells.remove((x, y))


    def are_neighbors_blocked(self, x, y, direction: Tuple[int, int])-> bool:
        (prev_x, prev_y) = direction
        (prev_x, prev_y) = (x - prev_x, y - prev_y)
        for curr_y in range(y - 1, y + 2):
            for curr_x in range(x - 1, x + 2):
                if not self.tiles[curr_x][curr_y] and ((curr_x != prev_x != x) or (curr_y != prev_y != y)):
                    return False
        return True

    def remove_dead_ends(self, prob: int =100) -> list[Tuple[int, int]]:
            dead_ends = []
            for x in range(self.width):
                for y in range(self.height):
                    if random.randint(0, 99) < prob:
                        self.remove_corridor(x=x, y=y)
                    else:
                        if self.tiles[x][y] and self.count_neighbors(x=x, y=y) < 2:
                            dead_ends.append((x, y))
            return dead_ends

    def count_neighbors(self, x: int, y: int)-> int:
        neighbors = 0
        neighbor_list = [(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)]
        for n_x, n_y in neighbor_list:
            if (0 < n_y < self.height and 0 < n_x < self.width) and \
                    self.tiles[n_x][n_y]:
                neighbors += 1

        return neighbors


    def remove_corridor(self, x: int, y: int):
        if not self.tiles[x][y].blocked and self.count_neighbors(x=x, y=y) < 2:
            neighbor = self.find_a_neighbor(x=x, y=y)
            self.tiles[x][y] = 0
            if neighbor:
                (new_x, new_y) = neighbor
                self.remove_corridor(new_x, new_y)

    def find_a_neighbor(self, x, y):
        neighbor_list = [(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)]
        for neighbor in neighbor_list:
            if (0 < neighbor[1] < self.height and 0 < neighbor[0] < self.width) and \
                    (self.tiles[neighbor[0]][neighbor[1]]):
                return neighbor
        else:
            return None