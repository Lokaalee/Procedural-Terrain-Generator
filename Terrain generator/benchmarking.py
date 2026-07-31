import time
import math
import matplotlib.pyplot as plt
from terrain_generator import TerrainGenerator
from quadtree import Rectangle

def run_visual_benchmark():
    print("Generating 40,000 vertices for visual benchmark...")
    generator = TerrainGenerator(width=100, depth=100, supersample=2)
    terrain_2d_array, quadtree = generator.generate()
    
    rows = len(terrain_2d_array)
    cols = len(terrain_2d_array[0])
    angle = math.radians(20)

    # jaribio la 1: Brute-Force ---
    start_time_before = time.perf_counter()
    processed_count_before = 0
    for i in range(rows):
        for j in range(cols):
            vertex = terrain_2d_array[i][j]
            x = vertex.x * 1.2
            y = vertex.y
            z = vertex.z * 1.2
            new_x = x * math.cos(angle) - z * math.sin(angle)
            new_z = x * math.sin(angle) + z * math.cos(angle)
            processed_count_before += 1
            
    time_before = time.perf_counter() - start_time_before

    #  jaribio la pili: QuadTree ---
    start_time_after = time.perf_counter()
    camera_view = Rectangle(50, 50, 15, 15) 
    visible_points = quadtree.query(camera_view)
    
    processed_count_after = 0
    for p in visible_points:
        orig_x, orig_z = p[0], p[2]
        sx = orig_x * 1.2
        sz = orig_z * 1.2
        new_x = sx * math.cos(angle) - sz * math.sin(angle)
        new_z = sx * math.sin(angle) + sz * math.cos(angle)
        processed_count_after += 1

    time_after = time.perf_counter() - start_time_after

    # --- Plotting results (matokeo) visuals (matplot)---
    print("Generating visualization...")
    
    methods = ['Brute-Force\n(40,000 vertices)', f'QuadTree Culling\n({processed_count_after} vertices)']
    times = [time_before, time_after]
    
    fig, ax = plt.subplots(figsize=(8, 6))
    
    # barchart(nyekundu for slow, green for fast)
    bars = ax.bar(methods, times, color=['#e74c3c', '#2ecc71'])
    
    ax.set_ylabel('Execution Time (Seconds)')
    ax.set_title('Milestone 4: Pipeline Optimization Benchmark')
    
    # Adding the exact time numbers on top of the bars
    for bar in bars:
        yval = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2, yval + (max(times)*0.02), 
                f'{yval:.5f}s', ha='center', va='bottom', fontweight='bold')
        
    # Calculating performance multiplier
    improvement = time_before / time_after if time_after > 0 else 0
    
    # Adding a text box with the conclusion
    textstr = f"Conclusion: QuadTree is {improvement:.1f}x faster"
    props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)
    ax.text(0.5, 0.85, textstr, transform=ax.transAxes, fontsize=12,
            verticalalignment='top', horizontalalignment='center', bbox=props)

    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    run_visual_benchmark()



