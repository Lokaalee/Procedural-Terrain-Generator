import math
import random
import matplotlib.pyplot as plt

def generate_poisson_disk_samples(width, height, min_radius, max_candidates=30):
    """
    Generates naturally distributed points using stochastic candidate sampling.
    """
    # The grid cell size is r / sqrt(2) to ensure each cell holds at most one point
    cell_size = min_radius / math.sqrt(2)
    
    grid_width = int(math.ceil(width / cell_size))
    grid_height = int(math.ceil(height / cell_size))
    
    # Initialize background grid with -1 (empty)
    grid = [[-1 for _ in range(grid_height)] for _ in range(grid_width)]
    
    points = []
    active_list = []
    
    #  Selecting the initial Monte Carlo seed point
    start_x = random.uniform(0, width)
    start_y = random.uniform(0, height)
    points.append((start_x, start_y))
    active_list.append(0)
    grid[int(start_x / cell_size)][int(start_y / cell_size)] = 0
    
    # Processing the active list
    while active_list:
        # Picking a random active point to expand from
        idx = random.randint(0, len(active_list) - 1)
        active_idx = active_list[idx]
        current_point = points[active_idx]
        
        found_valid_candidate = False
        
        # Generating stochastic candidates around the active point
        for _ in range(max_candidates):
            angle = random.uniform(0, 2 * math.pi)
            # Distance is between r and 2r
            radius = random.uniform(min_radius, 2 * min_radius) 
            
            candidate_x = current_point[0] + radius * math.cos(angle)
            candidate_y = current_point[1] + radius * math.sin(angle)
            
            # Check boundary conditions
            if 0 <= candidate_x < width and 0 <= candidate_y < height:
                grid_x = int(candidate_x / cell_size)
                grid_y = int(candidate_y / cell_size)
                
                too_close = False
                
                # Check spatial variance against neighboring grid cells
                search_min_x = max(0, grid_x - 2)
                search_max_x = min(grid_width - 1, grid_x + 2)
                search_min_y = max(0, grid_y - 2)
                search_max_y = min(grid_height - 1, grid_y + 2)
                
                for i in range(search_min_x, search_max_x + 1):
                    for j in range(search_min_y, search_max_y + 1):
                        neighbor_idx = grid[i][j]
                        if neighbor_idx != -1:
                            neighbor = points[neighbor_idx]
                            # Calculate Euclidean distance
                            dist = math.hypot(candidate_x - neighbor[0], candidate_y - neighbor[1])
                            if dist < min_radius:
                                too_close = True
                                break
                    if too_close:
                        break
                        
                # If the candidate passes the rejection test, accept it
                if not too_close:
                    points.append((candidate_x, candidate_y))
                    new_idx = len(points) - 1
                    active_list.append(new_idx)
                    grid[grid_x][grid_y] = new_idx
                    found_valid_candidate = True
                    break 
                    
        # If no valid candidates were found, retire the active point
        if not found_valid_candidate:
            active_list.pop(idx)
            
    return points

def visualize_sampling():
    print("Running stochastic sampling generation...")
    
    # Parameters for the terrain scale
    terrain_size = 100
    min_distance_between_objects = 5
    
    # Running the algorithm
    sampled_points = generate_poisson_disk_samples(terrain_size, terrain_size, min_distance_between_objects)
    
    print(f"Generated {len(sampled_points)} naturally distributed points.")
    
    # Extracting X and Y coordinates for plotting
    x_coords = [p[0] for p in sampled_points]
    y_coords = [p[1] for p in sampled_points]
    
    # Plotting the results for the milestone report
    plt.figure(figsize=(8, 8))
    plt.scatter(x_coords, y_coords, color='#27ae60', s=30, alpha=0.8, edgecolor='black')
    
    plt.title("Milestone 4: Stochastic Method (Poisson Disk Sampling)")
    plt.xlabel("Terrain X Axis")
    plt.ylabel("Terrain Z Axis")
    
    # Adding an explanatory text box
    props = dict(boxstyle='round', facecolor='white', alpha=0.9)
    plt.text(0.05, 0.95, f"Total Points: {len(sampled_points)}\nMin Distance: {min_distance_between_objects}", 
             transform=plt.gca().transAxes, fontsize=12, verticalalignment='top', bbox=props)
             
    plt.grid(True, linestyle='--', alpha=0.5)
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    visualize_sampling()