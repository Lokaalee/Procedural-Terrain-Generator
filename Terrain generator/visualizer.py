import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
import math


class Visualizer:

    def display(self, terrain):

        rows = len(terrain)
        cols = len(terrain[0])

        X = np.zeros((rows, cols))
        Y = np.zeros((rows, cols))
        Z = np.zeros((rows, cols))

        # Rotation angle (degrees)
        angle = math.radians(20)

        for i in range(rows):
            for j in range(cols):

                vertex = terrain[i][j]

               
                # Model Transformation
                

                # Scale
                x = vertex.x * 1.2
                y = vertex.y
                z = vertex.z * 1.2

                # Rotate around the Y-axis
                new_x = x * math.cos(angle) - z * math.sin(angle)
                new_z = x * math.sin(angle) + z * math.cos(angle)

                X[i][j] = new_x
                Y[i][j] = new_z
                Z[i][j] = y

        fig = plt.figure(figsize=(11, 8))
        ax = fig.add_subplot(111, projection="3d")

        # Terrain
        surface = ax.plot_surface(
            X,
            Y,
            Z,
            cmap="terrain",
            edgecolor="none",
            antialiased=True
        )

        # Camera
       
        ax.view_init(
            elev=30,
            azim=45
        )

        ax.set_title("Procedural Terrain Generator (3D)")
        ax.set_xlabel("X")
        ax.set_ylabel("Z")
        ax.set_zlabel("Height")

        fig.colorbar(
            surface,
            shrink=0.6,
            label="Height"
        )

        plt.show()