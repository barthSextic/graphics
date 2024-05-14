# Extension of 2d_grapher.py to include time as a third dimension

import mp4generator as mp4
import time
import math
import sys

FILENAME = "animations/elliptic.mp4"

FPS = 24.0
DT = 0.01

X_MIN = -3
X_MAX = 3
Y_MIN = -2
Y_MAX = 2
RESOLUTION = 512

NBHD = 0.064
CENTER = 0

GRAPH_COLOR = (255, 255, 255)
BG_COLOR = (46, 102, 130)

def f(x, y, t: float) -> bool:
    '''
    t: [0, 1]
    '''
    # t = (t * 8) - 4
    t = 4 * math.cos(2 * math.pi * t)
    value = x**3 + t * x - y ** 2
    value = abs(value - CENTER)

    return value < NBHD

def bool2rgb(value: bool) -> tuple:
    if value:
        return GRAPH_COLOR
    else:
        return BG_COLOR

def main():

    frame_height = int((Y_MAX - Y_MIN) * RESOLUTION)
    frame_width = int((X_MAX - X_MIN) * RESOLUTION)

    num_frames = int(1 / DT)

    frames = []

    sys_time = time.time()
    print(f"Generating {num_frames} frames with resolution {frame_width}x{frame_height}...")

    for frame_number in range(num_frames):
        frame = []
        t = frame_number * DT

        for y in range(frame_height):
            row = []

            for x in range(frame_width):
                x_val = X_MAX * x / frame_width + X_MIN * (frame_width - x) / frame_width
                y_val = Y_MAX * y / frame_height + Y_MIN * (frame_height - y) / frame_height

                row.append(bool2rgb(f(x_val, y_val, t)))

            frame.append(row)

        frames.append(frame)
    
    print(f"{sys.getsizeof(frames)} bytes worth of frames generated in {time.time() - sys_time} seconds")

    sys_time = time.time()
    print("Rendering video...")
    video = mp4.mp4(FILENAME, frames, FPS)
    video.make()
    print(f"Video rendered in {time.time() - sys_time} seconds")

if __name__ == "__main__":
    main()