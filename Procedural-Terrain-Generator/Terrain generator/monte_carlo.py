import random
import math


class MonteCarloSampler:

    def sample(self, terrain, samples=500):

        rows = len(terrain)
        cols = len(terrain[0])

        selected = []

        for _ in range(samples):

            i = random.randrange(rows)
            j = random.randrange(cols)

            selected.append(
                terrain[i][j]
            )

        return selected

    def estimate_average_height(
        self,
        terrain,
        samples=500
    ):

        selected = self.sample(
            terrain,
            samples
        )

        total = sum(
            vertex.y
            for vertex in selected
        )

        return total / len(selected)

    def exact_average_height(self, terrain):

        values = [
            vertex.y
            for row in terrain
            for vertex in row
        ]

        return sum(values) / len(values)

    def error(self, terrain, samples=500):

        exact = self.exact_average_height(
            terrain
        )

        estimate = self.estimate_average_height(
            terrain,
            samples
        )

        return abs(
            exact - estimate
        )