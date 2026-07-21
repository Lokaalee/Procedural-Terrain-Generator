class TerrainMaterial:

    def colour(self, height):

        if height < -2:
            return [0.0, 0.2, 0.8]      # Deep water

        elif height < 0:
            return [0.2, 0.5, 1.0]      # Shallow water

        elif height < 3:
            return [0.1, 0.7, 0.2]      # Grass

        elif height < 8:
            return [0.55, 0.40, 0.20]   # Dirt

        elif height < 13:
            return [0.50, 0.50, 0.50]   # Rock

        else:
            return [1.0, 1.0, 1.0]      # Snow