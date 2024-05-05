import argparse
import math
import random

from PIL import Image


def calculate_weighted_dot_product(gridX, gridY, x, y, period, dirs, perm):
    distX, distY = abs(x - gridX), abs(y - gridY)
    # The closer the distance between a point and the grid,
    # the greater the weight of that grid.
    weightX = 1 - 6 * distX**5 + 15 * distX**4 - 10 * distX**3
    weightY = 1 - 6 * distY**5 + 15 * distY**4 - 10 * distY**3
    hashed = perm[perm[int(gridX) % period] + int(gridY) % period]
    dot = (x - gridX) * dirs[hashed][0] + (y - gridY) * dirs[hashed][1]

    return weightX * weightY * dot


def create_noise(x, y, period, dirs, perm):
    intX = int(x)
    intY = int(y)

    return (
        calculate_weighted_dot_product(intX + 0, intY + 0, x, y, period, dirs, perm)
        + calculate_weighted_dot_product(intX + 1, intY + 0, x, y, period, dirs, perm)
        + calculate_weighted_dot_product(intX + 0, intY + 1, x, y, period, dirs, perm)
        + calculate_weighted_dot_product(intX + 1, intY + 1, x, y, period, dirs, perm)
    )


def calculate_octave_perline_noise(x, y, period, octs, dirs, perm):
    noise = 0
    frequency = 2
    # Add noise functions
    for octave in range(octs):
        amplitude = 0.5**octave
        frequency = 2**octave
        noise += amplitude * create_noise(
            x * frequency, y * frequency, period * frequency, dirs, perm
        )

    return noise


def create_perline_noise(size, freq, octs, seed):
    if seed:
        random.seed(314)
    perm = list(range(256))
    random.shuffle(perm)
    perm += perm
    dirs = [
        (math.cos(a * 2.0 * math.pi / 256), math.sin(a * 2.0 * math.pi / 256))
        for a in range(256)
    ]

    data = []
    for y in range(size):
        for x in range(size):
            data.append(
                calculate_octave_perline_noise(
                    x * freq, y * freq, int(size * freq), octs, dirs, perm
                )
            )

    return data


def main(size, freq, octs, random_seed):
    data = create_perline_noise(size, freq, octs, random_seed)
    im = Image.new("L", (size, size))
    im.putdata(data, size, size)
    im.save("images/perline_noise.png")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--size", type=int, default=128, help="Output 3D size")
    parser.add_argument("--octs", type=int, default=5, help="Octave number")
    parser.add_argument(
        "--set_seed", action="store_true", help="Whether to set random seed"
    )
    args = parser.parse_args()
    freq = 1 / 32.0
    main(args.size, freq, args.octs, args.set_seed)
