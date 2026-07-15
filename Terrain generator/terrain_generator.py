import math
import random
from vertex import Vertex


class TerrainGenerator:

    def __init__(self, width=60, depth=60):

        self.width = width
        self.depth = depth

        random.seed(42)

    def generate(self):

        terrain = []

        for z in range(self.depth):

            row = []

            for x in range(self.width):

                # Large mountain ranges
                large = (
    math.sin(x * 0.05) * 4 +
    math.cos(z * 0.05) * 4 +
    math.sin((x + z) * 0.04) * 3 +
    math.cos((x - z) * 0.04) * 3
)

                # Medium hills
                medium = (
                    math.sin((x + z) * 0.18) * 2.5 +
                    math.cos((x - z) * 0.15) * 2
                )

                # Rolling hills
                small = (
                    math.sin(x * 0.45) * 0.8 +
                    math.cos(z * 0.42) * 0.8
                )

                # Fine terrain detail
                detail = (
                    math.sin(x * 1.1) * 0.3 +
                    math.cos(z * 1.2) * 0.3
                )

                # Final terrain height
                height = (large * 1.2) + medium + small + detail

                row.append(Vertex(x, height, z))

            terrain.append(row)

        return terrain
