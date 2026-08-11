import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

from renderer import Renderer
from adaptive_lod import AdaptiveLOD


class TerrainAnimation:

    def __init__(self, X, Y, Z):

        self.X = X
        self.Y = Y
        self.original_Z = Z.copy()

        self.renderer = Renderer()
        self.adaptive_lod = AdaptiveLOD()

        self.fig = plt.figure(
            figsize=(11, 8)
        )

        self.ax = self.fig.add_subplot(
            111,
            projection="3d"
        )

        # =====================================
        # CAMERA ANIMATION
        # =====================================

        self.start_angle = 20
        self.end_angle = 125

        self.front_frames = 80

        # Camera distance changes over time
        self.near_distance = 15
        self.far_distance = 60

        # Camera height
        self.camera_height = 30

        # =====================================
        # WATER
        # =====================================

        self.sea_level = 0

        # Track current LOD
        self.previous_level = None

    # ==========================================
    # ANIMATION UPDATE
    # ==========================================

    def update(self, frame):

        self.ax.clear()

        # =====================================
        # CAMERA ANGLE
        # =====================================

        progress = (
            frame / self.front_frames
        )

        angle = (
            self.start_angle
            + (
                self.end_angle
                - self.start_angle
            ) * progress
        )

        # Convert angle to radians
        theta = np.radians(angle)

        # =====================================
        # ACTUAL CAMERA DISTANCE
        # =====================================

        # Move closer and farther from terrain
        distance_progress = (
            0.5
            + 0.5 * np.sin(
                progress * 2 * np.pi
            )
        )

        camera_distance = (
            self.near_distance
            + (
                self.far_distance
                - self.near_distance
            ) * distance_progress
        )

        # Actual camera position
        camera_x = (
            camera_distance * np.cos(theta)
        )

        camera_y = (
            camera_distance * np.sin(theta)
        )

        camera_z = self.camera_height

        # =====================================
        # ADAPTIVE LOD
        # =====================================

        # Create terrain from original geometry
        terrain = []

        rows, cols = self.original_Z.shape

        for i in range(rows):

            row = []

            for j in range(cols):

                from vertex import Vertex

                row.append(
                    Vertex(
                        self.X[i, j],
                        self.original_Z[i, j],
                        self.Y[i, j]
                    )
                )

            terrain.append(row)

        # Select LOD according to REAL camera distance
        reduced_terrain, level = (
            self.adaptive_lod.generate(
                terrain,
                camera_distance
            )
        )

        # =====================================
        # EXTRACT REDUCED TERRAIN
        # =====================================

        reduced_rows = len(reduced_terrain)
        reduced_cols = len(reduced_terrain[0])

        X = np.zeros(
            (reduced_rows, reduced_cols)
        )

        Y = np.zeros(
            (reduced_rows, reduced_cols)
        )

        Z = np.zeros(
            (reduced_rows, reduced_cols)
        )

        for i in range(reduced_rows):

            for j in range(reduced_cols):

                vertex = reduced_terrain[i][j]

                X[i, j] = vertex.x
                Y[i, j] = vertex.z
                Z[i, j] = vertex.y

        # =====================================
        # WATER ANIMATION
        # =====================================

        time = frame * 0.12

        water = Z < self.sea_level

        wave = (
            0.15
            * np.sin(
                X * 0.5 + time
            )
            * np.cos(
                Y * 0.5 + time
            )
        )

        Z[water] += wave[water]

        # =====================================
        # LIGHTING
        # =====================================

        colours = (
            self.renderer.build_colours(
                X,
                Y,
                Z
            )
        )

        # =====================================
        # RENDER TERRAIN
        # =====================================

        self.ax.plot_surface(
            X,
            Y,
            Z,
            facecolors=colours,
            edgecolor="none",
            linewidth=0,
            antialiased=True,
            shade=False
        )

        # =====================================
        # CAMERA VIEW
        # =====================================

        self.ax.view_init(
            elev=30,
            azim=angle
        )

        # =====================================
        # DISPLAY INFORMATION
        # =====================================

        point_count = (
            reduced_rows * reduced_cols
        )

        original_points = (
            rows * cols
        )

        reduction = (
            1
            - point_count / original_points
        ) * 100

        self.ax.set_title(
            "Procedural Terrain - "
            f"Adaptive LOD: {level.upper()} | "
            f"Distance: {camera_distance:.1f} | "
            f"Points: {point_count}"
        )

        self.ax.set_xlabel("X")
        self.ax.set_ylabel("Z")
        self.ax.set_zlabel("Height")

        # =====================================
        # CONSOLE LOD CHANGE
        # =====================================

        if level != self.previous_level:

            print(
                f"LOD changed to {level.upper()} | "
                f"Camera distance: "
                f"{camera_distance:.1f} | "
                f"Points: {point_count} | "
                f"Reduction: {reduction:.2f}%"
            )

            self.previous_level = level

        return self.ax,

    # ==========================================
    # START ANIMATION
    # ==========================================

    def play(self):

        animation = FuncAnimation(
            self.fig,
            self.update,
            frames=self.front_frames + 1,
            interval=100,
            repeat=True,
            blit=False
        )

        plt.show()