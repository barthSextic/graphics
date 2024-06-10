# Vector Field Animation Maker
# Plots df/dx and df/dy

# Heavily inspired by https://anvaka.github.io/fieldplay/

import random
import math
import mp4generator as mp4
import pngenerator as png

FILENAME = 'vector_field.mp4'
FPS = 24.0
NUM_FRAMES = 100

X_MIN = -10
X_MAX = 10
Y_MIN = -10
Y_MAX = 10
RESOLUTION = 500

WEIGHT = 100

MIN_LIFESPAN = 24
MAX_LIFESPAN = 100
MAX_NUM_PARTICLES = 1000

WIDTH = RESOLUTION * (X_MAX - X_MIN)
HEIGHT = RESOLUTION * (Y_MAX - Y_MIN)

BIT_DEPTH = 8
MAX_BRIGHTNESS = 2 ** BIT_DEPTH - 1

BG_COLOR = (0, 0, 0)
P_STATIC_COLOR = (MAX_BRIGHTNESS, MAX_BRIGHTNESS, MAX_BRIGHTNESS)


class vector:

    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y
        self.magnitude = math.sqrt(self.x ** 2 + self.y ** 2)

    def __add__(self, other):
        return vector(self.x + other.x, self.y + other.y)
    
    def __mul__(self, scalar: float):
        return vector(self.x * scalar, self.y * scalar)
    
    def __truediv__(self, scalar: float):
        return vector(self.x / scalar, self.y / scalar)

    def __repr__(self):
        return f'({self.x}, {self.y})'
    
    def __str__(self):
        return self.__repr__()
    
    def __iter__(self):
        yield self.x
        yield self.y


# ______________________________________________________________________________________________________________________

def velocity(pos: tuple) -> vector:
    x, y = pos 

    x = math.cos(y)
    y = math.sin(x)

    return vector(x, y)

# ______________________________________________________________________________________________________________________


def vecpos2pixelpos(vecpos: tuple) -> tuple:
    x, y = vecpos

    px = int((x - X_MIN) * RESOLUTION)
    py = int((y - Y_MIN) * RESOLUTION)

    return (px, py)

def pixelpos2vecpos(pixelpos: tuple) -> tuple:
    px, py = pixelpos

    x = px / RESOLUTION + X_MIN
    y = py / RESOLUTION + Y_MIN

    return (x, y)


class particle:

    def __init__(self) -> None:
        self.pos = (random.uniform(X_MIN, X_MAX), random.uniform(Y_MIN, Y_MAX))
        self.lifespan = random.randint(MIN_LIFESPAN, MAX_LIFESPAN)
        self.age = 0
        self.color = P_STATIC_COLOR

    def update(self) -> None:
        self.age += 1
        if self.age >= self.lifespan:
            self.__init__()
        else:
            v = velocity(self.pos) / WEIGHT
            x, y = self.pos

            x += v.x
            y += v.y

            self.pos = (x, y)

    def draw(self, frame: list) -> list:
        px, py = vecpos2pixelpos(self.pos)
        if 0 <= px < WIDTH and 0 <= py < HEIGHT:
            frame[py][px] = self.color
        
        return frame


def make_field() -> list:
    field = []
    for y in range(HEIGHT):
        row = []
        for x in range(WIDTH):
            pos = pixelpos2vecpos((x, y))
            v = velocity(pos)
            row.append(v)
        field.append(row)

    return field

def export_field(field: list) -> None:
    data = []
    for row in field:
        row_data = []
        for v in row:
            theta = math.atan2(v.y, v.x)
            color = png.angle2rgb(theta)
            row_data.append(color)
        data.append(row_data)

    png.RGB('vector_field.png', data, depth = BIT_DEPTH).make()


def main() -> None:
    field = make_field()
    frames = []
    particles = [particle() for _ in range(MAX_NUM_PARTICLES)]

    for _ in range(NUM_FRAMES):

        if _ % NUM_FRAMES // 10 == 0:
            print(f'{_ / NUM_FRAMES * 1000}%')

        frame = [[BG_COLOR for _ in range(WIDTH)] for _ in range(HEIGHT)]

        for p in particles:
            p.update()
            frame = p.draw(frame)

        frames.append(frame)

    print('100%')
    export_field(field)
    mp4.mp4(FILENAME, frames, FPS).make()


if __name__ == '__main__':
    main()