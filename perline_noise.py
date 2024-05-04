import random
import math
from PIL import Image

random.seed(314)
perm = list(range(256))
random.shuffle(perm)
perm += perm
dirs = [
    (math.cos(a * 2.0 * math.pi / 256), math.sin(a * 2.0 * math.pi / 256))
    for a in range(256)
]


def noise(x, y, per):
    def surflet(gridX, gridY):
        distX, distY = abs(x - gridX), abs(y - gridY)
        polyX = 1 - 6 * distX**5 + 15 * distX**4 - 10 * distX**3
        polyY = 1 - 6 * distY**5 + 15 * distY**4 - 10 * distY**3
        hashed = perm[perm[int(gridX) % per] + int(gridY) % per]
        grad = (x - gridX) * dirs[hashed][0] + (y - gridY) * dirs[hashed][1]
        return polyX * polyY * grad

    intX, intY = int(x), int(y)
    return (
        surflet(intX + 0, intY + 0)
        + surflet(intX + 1, intY + 0)
        + surflet(intX + 0, intY + 1)
        + surflet(intX + 1, intY + 1)
    )


def calculate_octave_perline_noise(x, y, per, octs):
    val = 0
    persistence = 0.8
    amplitude = 1
    frequency = 1
    for octave in range(octs):
        amplitude *= persistence
        frequency = 2**octave
        val += amplitude * noise(x * frequency, y * frequency, per * frequency)

    return val


def main():
    size, freq, octs, data = 128, 1 / 32.0, 4, []
    for y in range(size):
        for x in range(size):
            data.append(
                calculate_octave_perline_noise(
                    x * freq, y * freq, int(size * freq), octs
                )
            )

    im = Image.new("L", (size, size))
    im.putdata(data, 128, 128)
    im.save("noise.png")


if __name__ == "__main__":
    main()
