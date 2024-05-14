# Simple MP4 encoder for transforming a list of lists of lists of tuples into an MP4 video.

# Example input for an mp4 with n frames and 2 x 2 pixels per frame:

"""
data =  [
            [ 
                [(r11_1, g11_1, b11_1), (r12_1, g12_1, b12_1)],
                [(r21_1, g21_1, b21_1), (r22_1, g22_1, b22_1)]
            ],

            [
                [(r11_2, g11_2, b11_2), (r12_2, g12_2, b12_2)],
                [(r21_2, g21_2, b21_2), (r22_2, g22_2, b22_2)]
            ]

            .
            .
            .

            [
                [(r11_n, g11_n, b11_n), (r12_n, g12_n, b12_n)],
                [(r21_n, g21_n, b21_n), (r22_n, g22_n, b22_n)]
            ]

        ]
"""

# pip install opencv-python
import cv2
import numpy as np

class mp4:

    def __init__(self, filename: str, data: list, fps: float = 24.0):
        self.filename = filename
        self.fps = fps
        self.data = data
        self.height = len(data[0])
        self.width = len(data[0][0])

    def make(self):
        frames = np.array(self.data, ndmin=3)
        print(frames.shape)

        fourcc = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')
        out = cv2.VideoWriter(self.filename, fourcc, self.fps, (self.width, self.height))
        
        print(f'File opened: {out.isOpened()}')

        for frame in frames:
            # We'll convert the np array to hex BGR format
            # \0xBBGGRR
            frame = np.array(frame).astype(np.uint8)
            frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
            out.write(frame)

        out.release()
        cv2.destroyAllWindows()

def test_rgb():
    import math

    w = 512
    h = 256
    frames = 1000
    data = []

    for f in range(frames):
        frame = []
        for i in range(h):
            row = []
            for j in range(w):
                c = [1.0, 1.0, 1.0]
                phs = float(j) / float(w) * 2.0 * math.pi
                c[0] = (1 + math.cos(phs)) / 2
                c[1] = (1 + math.cos(phs + 2 * math.pi / 3)) / 2
                c[2] = (1 + math.cos(phs - 2 * math.pi / 3)) / 2

                mag = float(f) / float(frames)
                mag = 1.0 - 2 * abs(mag - 0.5)

                for x in range(3):
                    c[x] = c[x] * mag * 255
                    c[x] = min(int(c[x]), 255)

                row.append((c[0], c[1], c[2]))
            frame.append(row)
        data.append(frame)

    f = mp4('test.mp4', data, fps = 60.0)
    f.make()