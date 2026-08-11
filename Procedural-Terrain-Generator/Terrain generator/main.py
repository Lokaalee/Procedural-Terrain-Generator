import numpy as np

from terrain_generator import TerrainGenerator
from animation import TerrainAnimation


def main():

    generator = TerrainGenerator()

    terrain = generator.generate()

    rows = len(terrain)
    cols = len(terrain[0])

    X = np.zeros((rows, cols))
    Y = np.zeros((rows, cols))
    Z = np.zeros((rows, cols))

    for i in range(rows):
        for j in range(cols):

            vertex = terrain[i][j]

            X[i][j] = vertex.x * 1.2
            Y[i][j] = vertex.z * 1.2
            Z[i][j] = vertex.y

    animation = TerrainAnimation(
        X,
        Y,
        Z
    )

    animation.play()


if __name__ == "__main__":
    main()