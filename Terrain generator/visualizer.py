import matplotlib.pyplot as plt
import numpy as np
import math

from renderer import Renderer
from quadtree import Rectangle # ADDED IMPORT

class Visualizer:
    def display(self, terrain, quadtree): # Updated to accept the quadtree
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
        
        # We execute the renderer to ensure your lighting logic still runs properly, 
        # but we rely on matplotlib's colormap for the unstructured QuadTree mesh
        renderer = Renderer()
        colours = renderer.build_colours(X, Y, Z)

        # --- NEW QUADTREE CULLING HOOK ---
        # Define a "Camera View" box. 
        # We are telling the QuadTree we only want to render a 30x30 chunk 
        # positioned at the coordinates (30, 30) on the map.
        camera_view = Rectangle(30, 30, 15, 15) 
        visible_points = quadtree.query(camera_view)

        # Preparimg lists for the culled points
        opt_x = []
        opt_y = []
        opt_z = []

        # Apply our scaling and rotation transformations to the optimized points
        for p in visible_points:
            orig_x, orig_y, orig_z = p[0], p[1], p[2]
            
            sx = orig_x * 1.2
            sz = orig_z * 1.2
            
            new_x = sx * math.cos(angle) - sz * math.sin(angle)
            new_z = sx * math.sin(angle) + sz * math.cos(angle)
            
            opt_x.append(new_x)
            opt_y.append(new_z)
            opt_z.append(orig_y)

        # Plot the optimized mesh using trisurf (which handles 1D arrays of culled points)
        surface = ax.plot_trisurf(
            opt_x, 
            opt_y, 
            opt_z, 
            cmap='terrain', 
            linewidth=0.1, 
            antialiased=True,
            edgecolor='black'
        )
        # ---------------------------------

        # Camera
        ax.view_init(elev=30, azim=45)
        ax.set_title("QuadTree Optimized Terrain (Milestone 4)")
        ax.set_xlabel("X")
        ax.set_ylabel("Z")
        ax.set_zlabel("Height")

        plt.show()
