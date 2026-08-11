class TerrainMaterial:

    def colour(self, height):

        if height < -2:
            return [0.02, 0.20, 0.80]      # Deep water

        elif height < 0:
            return [0.20, 0.55, 1.00]      # Shallow water

        elif height < 3:
            return [0.80, 0.72, 0.45]      # Sand

        elif height < 7:
            return [0.15, 0.60, 0.20]      # Grass

        elif height < 11:
            return [0.50, 0.35, 0.18]      # Dirt

        elif height < 15:
            return [0.45, 0.45, 0.45]      # Rock

        else:
            return [1.0, 1.0, 1.0]         # Snow