import random
import math
from PIL import Image


def calculate_weighted_gradient(gridX, gridY, x, y, period, dirs, perm):
    distX, distY = abs(x - gridX), abs(y - gridY)
    # The closer the distance between a point and the grid,
    # the greater the weight of that grid.
    polyX = 1 - 6 * distX**5 + 15 * distX**4 - 10 * distX**3
    polyY = 1 - 6 * distY**5 + 15 * distY**4 - 10 * distY**3
    hashed = perm[perm[int(gridX) % period] + int(gridY) % period]
    grad = (x - gridX) * dirs[hashed][0] + (y - gridY) * dirs[hashed][1]

    return polyX * polyY * grad


def create_noise(x, y, period, dirs, perm):
    intX = int(x)
    intY = int(y)

    return (
        calculate_weighted_gradient(intX + 0, intY + 0, x, y, period, dirs, perm)
        + calculate_weighted_gradient(intX + 1, intY + 0, x, y, period, dirs, perm)
        + calculate_weighted_gradient(intX + 0, intY + 1, x, y, period, dirs, perm)
        + calculate_weighted_gradient(intX + 1, intY + 1, x, y, period, dirs, perm)
    )


def calculate_octave_perline_noise(x, y, period, octs, dirs, perm):
    val = 0
    persistence = 0.8
    amplitude = 1
    frequency = 1
    # Add noise functions
    for octave in range(octs):
        amplitude *= persistence
        frequency = 2**octave
        val += amplitude * create_noise(
            x * frequency, y * frequency, period * frequency, dirs, perm
        )

    return val


def main():
    random.seed(314)
    perm = list(range(256))
    random.shuffle(perm)
    perm += perm
    dirs = [
        (math.cos(a * 2.0 * math.pi / 256), math.sin(a * 2.0 * math.pi / 256))
        for a in range(256)
    ]

    size = 128
    freq = 1 / 32.0
    octs = 5
    data = []
    for y in range(size):
        for x in range(size):
            data.append(
                calculate_octave_perline_noise(
                    x * freq, y * freq, int(size * freq), octs, dirs, perm
                )
            )

    im = Image.new("L", (size, size))
    im.putdata(data, 128, 128)
    print(data)
    # TODO: Add 3D terrian data
    im.save("noise.png")


if __name__ == "__main__":
    main()
