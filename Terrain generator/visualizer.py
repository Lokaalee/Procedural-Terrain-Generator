import matplotlib.pyplot as plt
import numpy as np
import math

from renderer import Renderer


class Visualizer:

    def display(self, terrain):

        rows = len(terrain)
        cols = len(terrain[0])

        X = np.zeros((rows, cols))
        Y = np.zeros((rows, cols))
        Z = np.zeros((rows, cols))

        angle = math.radians(20)

        for i in range(rows):

            for j in range(cols):

                vertex = terrain[i][j]

                x = vertex.x * 1.2
                y = vertex.y
                z = vertex.z * 1.2

                new_x = (
                    x * math.cos(angle)
                    - z * math.sin(angle)
                )

                new_z = (
                    x * math.sin(angle)
                    + z * math.cos(angle)
                )

                X[i][j] = new_x
                Y[i][j] = new_z
                Z[i][j] = y

        renderer = Renderer()

        colours = renderer.build_colours(
            X,
            Y,
            Z
        )

        fig = plt.figure(
            figsize=(11, 8)
        )

        ax = fig.add_subplot(
            111,
            projection="3d"
        )

        ax.plot_surface(
            X,
            Y,
            Z,
            facecolors=colours,
            edgecolor="none",
            linewidth=0,
            antialiased=True,
            shade=False
        )

        ax.view_init(
            elev=30,
            azim=45
        )

        ax.set_title(
            "Procedural Terrain Generator"
        )

        ax.set_xlabel("X")
        ax.set_ylabel("Z")
        ax.set_zlabel("Height")

        plt.show()