from terrain_generator import TerrainGenerator
from visualizer import Visualizer

def main():
    print("Generating terrain and building QuadTree Acceleration Structure...")
    generator = TerrainGenerator()
    
    # Capturing both the 2D array and the QuadTree
    terrain, quadtree = generator.generate()

    viewer = Visualizer()
    print("Rendering optimized view...")
    
    # Passing both variables into the display function
    viewer.display(terrain, quadtree)

if __name__ == "__main__":
    main()
