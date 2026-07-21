import numpy as np

from lighting import PhongLighting
from material import TerrainMaterial


class Renderer:

    def __init__(self):

        self.light = PhongLighting()
        self.material = TerrainMaterial()

    def build_colours(self, X, Y, Z):

        rows, cols = Z.shape

        colours = np.zeros((rows, cols, 3))

        dx, dz = np.gradient(Z)

        for i in range(rows):

            for j in range(cols):

                normal = np.array([
                    -dx[i, j],
                    1,
                    -dz[i, j]
                ])

                intensity = self.light.calculate_intensity(normal)

                base = np.array(
                    self.material.colour(Z[i, j])
                )

                colours[i, j] = np.clip(
                    base * intensity,
                    0,
                    1
                )

        return colours