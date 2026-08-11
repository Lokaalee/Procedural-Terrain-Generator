import random
import numpy as np


class StochasticTerrainAnalysis:

    def __init__(self, terrain):

        self.terrain = terrain

        self.heights = np.array([
            [
                vertex.y
                for vertex in row
            ]
            for row in terrain
        ])

        self.values = self.heights.flatten()

    def exact_statistics(self):

        mean = np.mean(self.values)
        variance = np.var(self.values)

        return mean, variance

    def monte_carlo_statistics(
        self,
        sample_count=500
    ):

        random.seed(42)

        sample = random.sample(
            list(self.values),
            min(
                sample_count,
                len(self.values)
            )
        )

        sample = np.array(sample)

        mean = np.mean(sample)
        variance = np.var(sample)

        return mean, variance

    def compare(self, sample_count=500):

        exact_mean, exact_variance = (
            self.exact_statistics()
        )

        sampled_mean, sampled_variance = (
            self.monte_carlo_statistics(
                sample_count
            )
        )

        mean_error = abs(
            sampled_mean - exact_mean
        )

        variance_error = abs(
            sampled_variance - exact_variance
        )

        # Percentage error is only meaningful
        # when the exact value is sufficiently
        # far from zero.

        if abs(exact_mean) > 1.0:
            mean_percentage_error = (
                mean_error /
                abs(exact_mean)
            ) * 100
        else:
            mean_percentage_error = None

        variance_percentage_error = (
            variance_error /
            max(abs(exact_variance), 1e-9)
        ) * 100

        return {
            "sample_count": sample_count,
            "exact_mean": exact_mean,
            "sampled_mean": sampled_mean,
            "mean_error": mean_error,
            "mean_percentage_error":
                mean_percentage_error,
            "exact_variance": exact_variance,
            "sampled_variance": sampled_variance,
            "variance_error": variance_error,
            "variance_percentage_error":
                variance_percentage_error
        }

