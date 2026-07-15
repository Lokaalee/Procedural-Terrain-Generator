from terrain_generator import TerrainGenerator
from visualizer import Visualizer


def main():

    generator = TerrainGenerator()

    terrain = generator.generate()

    viewer = Visualizer()

    viewer.display(terrain)


if __name__ == "__main__":
    main()