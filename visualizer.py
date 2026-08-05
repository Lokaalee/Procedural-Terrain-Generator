import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import numpy as np
import math
import random
import time

from renderer import Renderer
from Quadtree import Rectangle # ADDED IMPORT

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

        # Save the original terrain heights
        original_opt_z = opt_z.copy()

        
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
        ax.set_title("QuadTree Optimized Terrain (Milestone 5)")
        ax.set_xlabel("X")
        ax.set_ylabel("Z")
        ax.set_zlabel("Height")

        
        # Create fog particles above terrain
        fog_x = []
        fog_y = []
        fog_z = []

        for i in range(100):
          index = random.randint(0, len(opt_x)-1)

          fog_x.append(opt_x[index])
          fog_y.append(opt_y[index])

          # place particles slightly above terrain height
          fog_z.append(original_opt_z[index] + random.uniform(2, 5))



        def animate(frame):
           
           start_time = time.time()
           # Clear the previous frame
           ax.clear()

           # Create new animated heights
           animated_z = []

           

           for i, height in enumerate(original_opt_z):
             
              wave = math.sin(frame * 0.05 + i * 0.1)
              animated_z.append(height + wave * 0.3)
    
           print("Animated heights:", len(animated_z))
           # Draw the terrain
           print(len(opt_x), len(opt_y), len(animated_z))
           ax.plot_trisurf(
             opt_x,
             opt_y,
             animated_z,
             cmap='terrain',
             linewidth=0.1,
             antialiased=True,
             edgecolor='black'
         )

            # Draw fog particles
           ax.scatter(
                fog_x,
                fog_y,
                fog_z,
                s=5,
                alpha=0.5
            )
 
        # Rotate the camera
           ax.view_init(elev=30, azim=frame)

           ax.set_title("QuadTree Optimized Terrain (Milestone 5)")
           ax.set_xlabel("X")
           ax.set_ylabel("Z")
           ax.set_zlabel("Height")



           frame_time = time.time() - start_time
           fps = 1 / frame_time

           print("FPS:", round(fps, 2))




           return []

        
        self.ani = FuncAnimation(
           fig,
           animate,
           frames=360,
           interval=50,
           blit=False,
           repeat=True
)  

        plt.show()
