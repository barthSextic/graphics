import math
import time
import pngenerator as png

FILENAME = "plots/elliptic.png"
X_MIN = -2
X_MAX = 2
Y_MIN = -2
Y_MAX = 2
RESOLUTION = 1024

NBHD = 0.064
CENTER = 0

def f(x, y):
    return y**2 - x**3 + x

def threshold_plot(plot, min, max):
    for row in plot:
        for i in range(len(row)):
            if row[i] < min or row[i] > max:
                row[i] = 0
            else:
                row[i] = 255
    return plot

def gaussian_blur(plot, sigma):
    start_time = time.time()
    print("Gaussianing...")
    # Create a 2D Gaussian kernel
    kernel = []
    for i in range(-3 * sigma, 3 * sigma + 1):
        row = []
        for j in range(-3 * sigma, 3 * sigma + 1):
            row.append(math.exp(-(i**2 + j**2) / (2 * sigma**2)))
        kernel.append(row)

    # Normalize the kernel
    kernel_sum = sum([sum(row) for row in kernel])
    kernel = [[x / kernel_sum for x in row] for row in kernel]

    # Apply the kernel to the plot
    new_plot = []
    for i in range(len(plot)):
        row = []
        for j in range(len(plot[0])):
            new_pixel = 0
            for k in range(-3 * sigma, 3 * sigma + 1):
                for l in range(-3 * sigma, 3 * sigma + 1):
                    if i + k >= 0 and i + k < len(plot) and j + l >= 0 and j + l < len(plot[0]):
                        new_pixel += plot[i + k][j + l] * kernel[k + 3 * sigma][l + 3 * sigma]
            row.append(min(int(new_pixel), 255))
        new_plot.append(row)

    end_time = time.time()
    print("Blurring done in ", end_time - start_time, " seconds")
    return new_plot

def average_blur(plot, radius):
    start_time = time.time()
    print("Averaging...")
    # Apply the kernel to the plot
    new_plot = []
    for i in range(len(plot)):
        row = []
        for j in range(len(plot[0])):
            new_pixel = 0
            count = 0
            for k in range(-radius, radius + 1):
                for l in range(-radius, radius + 1):
                    if i + k >= 0 and i + k < len(plot) and j + l >= 0 and j + l < len(plot[0]):
                        new_pixel += plot[i + k][j + l]
                        count += 1
            row.append(min(int(new_pixel / count), 255))
        new_plot.append(row)

    end_time = time.time()
    print("Averaging done in ", end_time - start_time, " seconds")
    return new_plot

def add_gridmarks(plot):
    # Note, the gridmarks will be added at each RESOLUTION pixels
    for i in range(0, len(plot), RESOLUTION):
        for j in range(0, len(plot[0]), RESOLUTION):
            plot[i][j] = 0

    return plot

def add_gridlines(plot):
    # Note, the gridlines will be added at each RESOLUTION pixels
    for i in range(0, len(plot), RESOLUTION):
        for j in range(0, len(plot[0]), RESOLUTION):
            for k in range(RESOLUTION):
                plot[i][j + k] = 0
                plot[i + k][j] = 0

    return plot

def main():

    png_height = (Y_MAX - Y_MIN) * RESOLUTION
    png_width = (X_MAX - X_MIN) * RESOLUTION

    # Each pixel will be greyscale 8-bit
    # The plot will be a list of lists of integers
    """
    [[11, 12, 13, ...],
     [21, 22, 23, ...],
     [31, 32, 33, ...],
     ...
    """
    plot = []

    for h in range(png_height):
        row = []
        for w in range(png_width):
            # Get the x and y coordinates
            x = X_MAX * w / png_width + X_MIN * (png_width - w) / png_width
            y = Y_MAX * h / png_height + Y_MIN * (png_height - h) / png_height

            row.append(f(x, y))
        plot.append(row)

    plot = threshold_plot(plot, CENTER - NBHD, CENTER + NBHD)
    plot = average_blur(plot, 1)
    plot = gaussian_blur(plot, 1)

    # plot = add_gridlines(plot)

    png_maker = png.Grayscale(FILENAME, plot)
    print(png_maker)
    png_maker.make()

if __name__ == "__main__":
    main()
