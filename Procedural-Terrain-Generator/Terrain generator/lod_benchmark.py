import time

from terrain_generator import TerrainGenerator
from adaptive_lod import AdaptiveLOD


def benchmark(width, depth, camera_distance):

    print()
    print("=" * 55)
    print(f"Terrain: {width} x {depth}")
    print(f"Camera distance: {camera_distance}")
    print("=" * 55)

    generator = TerrainGenerator(width, depth)

    # =====================================
    # ORIGINAL TERRAIN
    # =====================================

    start = time.perf_counter()

    terrain = generator.generate_fast()

    original_time = (
        time.perf_counter() - start
    )

    original_points = (
        len(terrain) *
        len(terrain[0])
    )

    # =====================================
    # ADAPTIVE LOD
    # =====================================

    lod = AdaptiveLOD()

    start = time.perf_counter()

    reduced, level = lod.generate(
        terrain,
        camera_distance
    )

    lod_time = (
        time.perf_counter() - start
    )

    reduced_points = (
        len(reduced) *
        len(reduced[0])
    )

    # =====================================
    # CALCULATE RESULTS
    # =====================================

    reduction = (
        (original_points - reduced_points)
        / original_points
    ) * 100

    print()
    print("Original points: ", original_points)
    print("LOD points:      ", reduced_points)
    print("Selected LOD:    ", level)

    print()
    print(
        f"Generation time: "
        f"{original_time:.6f} seconds"
    )

    print(
        f"LOD processing:  "
        f"{lod_time:.6f} seconds"
    )

    print(
        f"Geometry reduction: "
        f"{reduction:.2f}%"
    )


def main():

    benchmark(30, 30, 10)
    benchmark(60, 60, 30)
    benchmark(120, 120, 60)


if __name__ == "__main__":
    main()