# Extension of 2d_grapher.py to include time as a third dimension

import mp4generator as mp4
import time
import math
import sys

FILENAME = "animations/circles.mp4"

FPS = 24.0
DT = 0.0025

X_MIN = -1
X_MAX = 1
Y_MIN = -0.6
Y_MAX = 0.6
RESOLUTION = 512
NBHD = 0.005
CENTER = 0

GRAPH_COLOR = (255, 255, 255)
BG_COLOR = (46, 102, 130)

def f(x, y, t: float) -> bool:
    '''
    t: [0, 1]
    '''
    # t = (t * 8) - 4
    # t = math.cos(2 * math.pi * t)
    t = 1 - math.cos(math.pi * t) * math.cos(math.pi * t)

    k = 1 + int((t / DT))
    sum = 0

    for n in range(1, k + 1):
        sum += (math.pow(-1, n+1) * math.sin(2 * math.pi * n * x)) / (math.pi * n)

    value = sum - y
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

        if frame_number % 50 == 0:
            print(f"Frame {frame_number}/{num_frames}")

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