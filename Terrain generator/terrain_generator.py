import math
import random
from vertex import Vertex


class TerrainGenerator:

    def __init__(self, width=60, depth=60, supersample=2):

        self.width = width
        self.depth = depth
        self.supersample = supersample

        random.seed(42)


    def generate(self):

        terrain = []

        # Generate terrain at higher resolution
        high_width = self.width * self.supersample
        high_depth = self.depth * self.supersample


        for z in range(high_depth):

            row = []

            for x in range(high_width):

                # Scale coordinates back to original terrain size
                sx = x / self.supersample
                sz = z / self.supersample


                # Large mountain ranges
                large = (
                    math.sin(sx * 0.05) * 4 +
                    math.cos(sz * 0.05) * 4 +
                    math.sin((sx + sz) * 0.04) * 3 +
                    math.cos((sx - sz) * 0.04) * 3
                )


                # Medium hills
                medium = (
                    math.sin((sx + sz) * 0.18) * 2.5 +
                    math.cos((sx - sz) * 0.15) * 2
                )


                # Rolling hills
                small = (
                    math.sin(sx * 0.45) * 0.8 +
                    math.cos(sz * 0.42) * 0.8
                )


                # Fine terrain detail
                detail = (
                    math.sin(sx * 1.1) * 0.3 +
                    math.cos(sz * 1.2) * 0.3
                )


                # Final height calculation
                height = (
                    (large * 1.2)
                    + medium
                    + small
                    + detail
                    - 1.5
                )


                row.append(Vertex(sx, height, sz))

            terrain.append(row)


        # Reduce high-resolution terrain
        # using averaging to perform supersampling
        return self.downsample(terrain)



    def downsample(self, terrain):

        factor = self.supersample

        result = []


        for z in range(0, len(terrain), factor):

            row = []


            for x in range(0, len(terrain[0]), factor):

                total_height = 0
                count = 0


                # Average neighbouring samples
                for dz in range(factor):

                    for dx in range(factor):

                        if (
                            z + dz < len(terrain)
                            and x + dx < len(terrain[0])
                        ):

                            total_height += terrain[z + dz][x + dx].y
                            count += 1


                average_height = total_height / count


                row.append(
                    Vertex(
                        terrain[z][x].x,
                        average_height,
                        terrain[z][x].z
                    )
                )


            result.append(row)


        return result