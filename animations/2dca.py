# 2 Dimensional Cellular Automata
# This implementation uses a king graph from the glib module in my personal library. 
# It could be much faster, but this implementation is for educational purposes / proof of concept.

from enum import Enum
from ricklib import glib
import random
import mp4generator as mp4


FILENAME = '2dca.mp4'
FRAME_RATE = 8
ITERATIONS = 30


class SEED(Enum):
    EMPTY = 0
    RANDOM = 1

class CA2D:

    def __init__(self, width: int = 512, height: int = 512):
        self.width = width
        self.height = height
        self.data = glib.kinggraph(width, height)

        self.S = [2, 3]
        self.B = [3]

    def init_seed(self, seed: SEED = SEED.RANDOM):
        '''Initializes the seed for the 2D Cellular Automata'''

        if seed == SEED.EMPTY:
            for v in self.data.V:
                v.value = 0
        elif seed == SEED.RANDOM:
            for v in self.data.V:
                v.value = random.randint(0, 1)

    def get(self) -> object:
        return self.data

    def set_survival(self, n: list) -> None:
        '''Defines the number of live neighbors for a cell to remain alive
        n should be a list of integers from 0-8'''
        
        self.S = n

    def set_birth(self, n: list) -> None:
        '''Defines the number of live neighbors for a dead cell to become alive
        n should be a list of integers from 0-8'''

        self.B = n

    def update(self) -> None:
        '''Updates the 2D Cellular Automata'''
        new_graph = glib.kinggraph(self.width, self.height)
        for v in new_graph.V:
            v.value = 0

        for v in self.data.V:
            nbhd = self.data.nbhd(v)
            live_neighbors = 0
            for n in nbhd.V:
                live_neighbors += n.value

            if v.value == 1 and live_neighbors in self.S:
                new_graph.get_vertex(v.name).value = 1
            elif v.value == 0 and live_neighbors in self.B:
                new_graph.get_vertex(v.name).value = 1

        self.data = new_graph

    
    def frame(self) -> list:
        '''Returns the current frame of the 2D Cellular Automata'''

        frame = []
        counter = 0
        for _ in range(self.height):
            row = []
            for _ in range(self.width):
                row.append(self.data.get_vertex(counter).value)
                counter += 1
            frame.append(row)

        return frame
    


def test():
    ca = CA2D(5, 5)
    ca.init_seed()
    frame = ca.frame()
    for row in frame:
        print(row)

    print()
    ca.update()
    frame = ca.frame()
    for row in frame:
        print(row)


def main():
    ca = CA2D(25, 25)
    ca.init_seed(SEED.RANDOM)
    ca.set_survival([2, 3])
    ca.set_birth([3, 6])

    frames = []
    for f in range(ITERATIONS):
        print(f'Frame {f + 1} / {ITERATIONS}')
        frames.append(ca.frame())
        ca.update()

    frames = mp4.scale_up(frames, 20)
    frames = mp4.binary2rgb(frames)
    video = mp4.mp4('highlife.mp4', frames, FRAME_RATE)
    video.make()
    

if __name__ == '__main__':
    main()