from enum import Enum
import random
from ricklib import pngenerator as png

# Create 1D Cellular Automata with every possible rule (0-255)

DIR = 'plots/1D_CA/'

DEFAULT_WIDTH = 512
DEFAULT_HEIGHT = 512

class SEED_TYPE(Enum):
    RANDOM = 0
    CENTER = 1
    LEFT = 2
    RIGHT = 3

class CA:

    def __init__(self, rule: int, width: int = DEFAULT_WIDTH, height: int = DEFAULT_HEIGHT, seed_type: SEED_TYPE = SEED_TYPE.RANDOM):
        # Initialize the Cellular Automata
        # rule: integer from 0-255 defining the rule

        if rule < 0 or rule > 255 or not isinstance(rule, int):
            raise ValueError('Rule must be an integer from 0-255')

        self.rule = rule
        self.width = width
        self.height = height
        self.data = []
        self.seed_type = seed_type

    def _rule(self, left: int, center: int, right: int):
        # Apply the rule to the current cell
        return (self.rule >> (left * 4 + center * 2 + right)) & 1

    def _init_seed(self):
        seed = [0] * self.width
        if self.seed_type == SEED_TYPE.RANDOM:
            seed = [random.randint(0, 1) for _ in range(self.width)]
        elif self.seed_type == SEED_TYPE.CENTER:
            seed = [0] * self.width
            seed[self.width // 2] = 1
        elif self.seed_type == SEED_TYPE.LEFT:
            seed = [0] * self.width
            seed[0] = 1
        elif self.seed_type == SEED_TYPE.RIGHT:
            seed = [0] * self.width
            seed[-1] = 1
        return seed
    
    def _next_row(self, row: list):
        new_row = []

        new_row.append(self._rule(0, row[0], row[1]))

        for i in range(1, len(row) - 1):
            left = row[i - 1]
            center = row[i]
            right = row[i + 1]
            new_row.append(self._rule(left, center, right))

        new_row.append(self._rule(row[-2], row[-1], 0))

        return new_row

    def generate(self):
        # Generate the Cellular Automata
        self.data = [self._init_seed()]

        for _ in range(self.height - 1):
            self.data.append(self._next_row(self.data[-1]))

        # We'll scale the data so that 1 -> 255 and 0 -> 0
        for i in range(len(self.data)):
            for j in range(len(self.data[i])):
                self.data[i][j] *= 255

        return self.data
    
    def save(self, filename: str):
        # Save the Cellular Automata as a PNG
        png.Grayscale(filename, self.data).make()


def test():
    rule = 30
    ca = CA(rule, seed_type=SEED_TYPE.RIGHT)
    ca.generate()
    ca.save(f'{DIR}{rule}_{ca.seed_type.name}.png')


def main():

    width = 511
    height = 511

    for rule in range(256):
        for seed_type in SEED_TYPE:
            ca = CA(rule, width, height, seed_type)
            ca.generate()
            ca.save(f'{DIR}{rule}_{seed_type.name}.png')


if __name__ == '__main__':
    main()