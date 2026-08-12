from lod import LOD
class AdaptiveLOD:

    def __init__(self):

        self.lod = LOD()

    def select_level(self, camera_distance):

        # Close camera = maximum detail
        if camera_distance < 20:
            return "high"

        # Medium distance = medium detail
        elif camera_distance < 45:
            return "medium"

        # Far distance = minimum detail
        else:
            return "low"
    def generate(self, terrain, camera_distance):

        level = self.select_level(
            camera_distance
        )

        reduced = self.lod.reduce(
            terrain,
            level
        )
        return reduced, level