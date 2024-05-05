import argparse

import matplotlib.pyplot as plt
import numpy as np
from matplotlib import cm
from matplotlib.colors import LightSource

from create_perline_noise import create_perline_noise


def main(size, freq, octs, random_seed):
    data = create_perline_noise(size, freq, octs, random_seed)
    x = np.linspace(0, size - 1, size)
    y = np.linspace(0, size - 1, size)
    x, y = np.meshgrid(x, y)
    z = np.reshape(data, (size, size))

    fig, ax = plt.subplots(subplot_kw=dict(projection="3d"))
    ls = LightSource(270, 45)
    # To use a custom hillshading mode, override the built-in shading and pass
    # in the rgb colors of the shaded surface calculated from "shade".
    rgb = ls.shade(z, cmap=cm.gist_earth, vert_exag=0.1, blend_mode="soft")
    surf = ax.plot_surface(
        x,
        y,
        z,
        rstride=1,
        cstride=1,
        facecolors=rgb,
        linewidth=0,
        antialiased=False,
        shade=False,
    )
    ax.set_title("Mountain made by perline noise")

    plt.show()


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
