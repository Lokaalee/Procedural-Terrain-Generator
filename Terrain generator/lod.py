class LOD:

    def __init__(self):

        self.levels = {
            "high": 1,
            "medium": 2,
            "low": 4
        }

    def reduce(self, terrain, level="high"):

        step = self.levels[level]

        return [
            row[::step]
            for row in terrain[::step]
        ]