import cmath
import math
import pngenerator as png

FILENAME = 'plots/complexlog.png'

X_MIN = -2
X_MAX = 2
Y_MIN = -2
Y_MAX = 2
RESOLUTION = 1024

BIT_DEPTH = 16

# We'll color the plot as follows
# phase         -> hue
# magnitude     -> lightness

def f(z: complex) -> complex:
    '''
    if (z ** 2 - 1) == 0:
        return complex(math.inf, math.inf)
    return z / (z**2 - 1)
    '''
    # return cmath.sinh(cmath.exp(z)) - 1
    if abs(z) == 0:
        return complex(math.inf, math.inf)
    return cmath.log(z)


def color(z: complex) -> tuple:
    c = [0.0, 0.0, 0.0]

    # We'll calculate the phase color between 0 and 1
    # Then scale by magnitude

    # polar = (magnitude, phase)
    polar = cmath.polar(z)

    # We'll want the phase to correspond to hue
    # Note, the phase is in the range [-pi, pi]
    # 0         -> red
    # 2pi/3     -> green
    # -2pi/3    -> blue

    # Note: this is a bit of a hack
    phs = polar[1] # float
    c[0] = (1 + math.cos(phs)) / 2
    c[1] = (1 + math.cos(phs + 2 * math.pi / 3)) / 2
    c[2] = (1 + math.cos(phs - 2 * math.pi / 3)) / 2

    # We'll want the magnitude to correspond to lightness
    # In the end we should have values in the range [0, 2^BIT_DEPTH - 1]
    # 0                 -> black
    # 2^BIT_DEPTH - 1   -> white

    mag = polar[0] # float

    mag = math.pow(mag, 1/8)

    for x in range(3):
        color = c[x] * mag

        if color > 1:
            color = 1
        elif color < 0:
            color = 0

        color = color * (2 ** BIT_DEPTH - 1)
        color = min(int(color), 2 ** BIT_DEPTH - 1)

        c[x] = color

    c_tuple = (c[0], c[1], c[2])
    return c_tuple

def main():
    
    png_height = (Y_MAX - Y_MIN) * RESOLUTION
    png_width = (X_MAX - X_MIN) * RESOLUTION

    plot = []

    print("Generating plot...")
    for im in range(png_height):
        row = []
        for re in range(png_width):
            x = X_MIN + re / RESOLUTION
            y = Y_MAX - im / RESOLUTION
            z = complex(x, y)
            row.append(color(f(z)))
        plot.append(row)

    print("Plot generated")

    output = png.RGB(FILENAME, plot, depth=BIT_DEPTH, compression=True)
    output.make()

if __name__ == '__main__':
    main()