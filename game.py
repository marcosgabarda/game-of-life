import itertools
import random
import sys

import numpy as np


class GameOfLife:
    def __init__(self, size: tuple, variant: str = "23/3"):
        self.size: tuple = size
        self.variant(variant=variant)

    def __str__(self) -> str:
        """Representation of the grid."""
        # Emoji representation only for 2-dimensional grids.
        if len(self.grid.shape) == 2:
            display = ""
            for row in range(self.grid.shape[0]):
                display += " ".join(
                    [
                        self.display_cell((row, column))
                        for column in range(self.grid.shape[1])
                    ]
                )
                display += "\n"
            return f"{display}"
        # Other dimensions, the standard numpy representation
        return str(self.grid)

    def display_cell(self, cell):
        """Uses emojis to display cells."""
        return "\U00002b1b" if self.grid[cell] else "\U00002b1c"

    def variant(self, variant: str):
        """Parses the variant sting and stablish the born and survive conditions."""
        self.survive_conditions, self.born_conditions = variant.split("/")
        self.survive_conditions = tuple(map(lambda x: int(x), self.survive_conditions))
        self.born_conditions = tuple(map(lambda x: int(x), self.born_conditions))

    def zeros(self):
        """Initialize a zero life grid."""
        self.grid = np.zeros(self.size, dtype=np.bool)

    def random(self):
        """Initialize a random life grid."""
        self.grid = np.random.randint(2, size=self.size, dtype=np.bool)

    def neighbours(self, coordinates, distance=1):
        """Gets values of the neighbours of a cell."""
        dimensions = len(self.grid.shape)
        neighbours = []
        positions = itertools.product(
            [step for step in range(-distance, distance + 1)], repeat=dimensions
        )
        for position in positions:
            if position != (0,) * dimensions:
                try:
                    neighbours.append(
                        self.grid[
                            tuple(
                                [
                                    coordinates[index] + value
                                    for index, value in enumerate(position)
                                ]
                            )
                        ]
                    )
                except IndexError:
                    pass
        return np.array(neighbours)

    def survives(self, value, cell) -> bool:
        """Decides if the cell survives or not."""
        neighbours = self.neighbours(cell)
        if value and sum(neighbours) in self.survive_conditions:
            return True
        elif not value and sum(neighbours) in self.born_conditions:
            return True
        return False

    def evolve(self):
        """Creates a new gred, with the new life."""
        evolved_grid = np.zeros(self.grid.shape, dtype=np.bool)
        iterator = np.nditer(self.grid, flags=["multi_index"])
        for value in iterator:
            evolved_grid[iterator.multi_index] = self.survives(
                value, iterator.multi_index
            )
        self.grid = np.array(evolved_grid)


if __name__ == "__main__":
    """Main execution sample."""

    shape = input("Shape of the grid (int separated by spaces)?: ")
    shape = tuple(map(lambda item: int(item), shape.split(" ")))
    cycles = int(input("Number of cycles?: "))
    variant = input("Variant? [23/3]: ") or "23/3"
    game = GameOfLife(shape, variant=variant)
    game.random()
    print(game)
    for _ in range(cycles):
        game.evolve()
        print(game)
