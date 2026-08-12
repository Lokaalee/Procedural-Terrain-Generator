import time

from terrain_generator import TerrainGenerator
from stochastic_analysis import StochasticTerrainAnalysis


def benchmark_generation(width, depth):

    print()
    print("=" * 50)
    print(f"Terrain size: {width} x {depth}")
    print("=" * 50)

    generator = TerrainGenerator(width, depth)

    # Original generation
    start = time.perf_counter()

    generator.generate()

    original_time = time.perf_counter() - start

    # Optimized generation
    start = time.perf_counter()

    optimized = generator.generate_fast()

    optimized_time = time.perf_counter() - start

    # Performance results
    speedup = original_time / optimized_time

    improvement = (
        (original_time - optimized_time)
        / original_time
    ) * 100

    print(f"Original time:  {original_time:.6f} seconds")
    print(f"Optimized time: {optimized_time:.6f} seconds")
    print(f"Speedup:        {speedup:.2f}x")
    print(f"Improvement:    {improvement:.2f}%")

    # Monte Carlo analysis
    analysis = StochasticTerrainAnalysis(optimized)

    print()
    print("Monte Carlo Sampling Analysis")
    print("-" * 40)

    sample_sizes = [100, 500, 1000, 2000]

    for sample_size in sample_sizes:

        result = analysis.compare(sample_size)

        print()
        print(f"Sample size: {result['sample_count']}")

        print(
            f"Mean error: "
            f"{result['mean_error']:.6f}"
        )

        if result["mean_percentage_error"] is not None:

            print(
                f"Mean error (%): "
                f"{result['mean_percentage_error']:.4f}%"
            )

        else:

            print(
                "Mean percentage error: "
                "Not meaningful because exact mean "
                "is close to zero"
            )

        print(
            f"Variance error: "
            f"{result['variance_error']:.6f}"
        )

        print(
            f"Variance error (%): "
            f"{result['variance_percentage_error']:.4f}%"
        )


def main():

    benchmark_generation(30, 30)
    benchmark_generation(60, 60)
    benchmark_generation(120, 120)


if __name__ == "__main__":
    main()