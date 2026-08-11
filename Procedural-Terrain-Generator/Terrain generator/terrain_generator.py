import math
import random
import numpy as np
from vertex import Vertex


class TerrainGenerator:

    def __init__(self, width=60, depth=60):

        self.width = width
        self.depth = depth
        self.sea_level = 0

        random.seed(42)

    # ==========================================
    # ORIGINAL VERSION
    # ==========================================

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

                # Terrain height
                height = (
                    (large * 1.2)
                    + medium
                    + small
                    + detail
                )

                # Central lake depression
                lake_x = self.width / 2
                lake_z = self.depth / 2

                distance = math.sqrt(
                    (x - lake_x) ** 2 +
                    (z - lake_z) ** 2
                )

                lake_radius = 10

                if distance < lake_radius:

                    lake_depth = (
                        (lake_radius - distance) * 1.2
                    )

                    height -= lake_depth

                row.append(
                    Vertex(x, height, z)
                )

            terrain.append(row)

        return terrain

    # ==========================================
    # OPTIMIZED NUMPY VERSION
    # ==========================================

    def generate_fast(self):

        x = np.arange(
            self.width,
            dtype=float
        )

        z = np.arange(
            self.depth,
            dtype=float
        )

        X, Z = np.meshgrid(
            x,
            z
        )

        # Large mountain ranges
        large = (
            np.sin(X * 0.05) * 4 +
            np.cos(Z * 0.05) * 4 +
            np.sin((X + Z) * 0.04) * 3 +
            np.cos((X - Z) * 0.04) * 3
        )

        # Medium hills
        medium = (
            np.sin((X + Z) * 0.18) * 2.5 +
            np.cos((X - Z) * 0.15) * 2
        )

        # Rolling hills
        small = (
            np.sin(X * 0.45) * 0.8 +
            np.cos(Z * 0.42) * 0.8
        )

        # Fine terrain detail
        detail = (
            np.sin(X * 1.1) * 0.3 +
            np.cos(Z * 1.2) * 0.3
        )

        # Terrain height
        heights = (
            (large * 1.2)
            + medium
            + small
            + detail
        )

        # Central lake depression
        lake_x = self.width / 2
        lake_z = self.depth / 2

        distance = np.sqrt(
            (X - lake_x) ** 2 +
            (Z - lake_z) ** 2
        )

        lake_radius = 10

        lake_mask = distance < lake_radius

        lake_depth = (
            (lake_radius - distance) * 1.2
        )

        heights[lake_mask] -= (
            lake_depth[lake_mask]
        )

        # Convert NumPy result to Vertex objects
        terrain = []

        for z_index in range(self.depth):

            row = []

            for x_index in range(self.width):

                row.append(
                    Vertex(
                        x_index,
                        heights[z_index, x_index],
                        z_index
                    )
                )

            terrain.append(row)

        return terrain
