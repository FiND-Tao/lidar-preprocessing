#%%
import numpy as np
from scipy.ndimage.morphology import grey_opening
from pyntcloud import PyntCloud
import pandas as pd
import CSF
def approximate_pmf(points, cell_size=1, initial_threshold=0.5, max_threshold=1.0, increment=0.2):
    """
    Approximate Progressive Morphological Filter

    :param points: Nx3 numpy array of XYZ coordinates
    :param cell_size: Size of grid cell
    :param initial_threshold: Initial height threshold
    :param max_threshold: Maximum height threshold
    :param increment: Threshold increment value
    :return: Boolean array of the same length as points. True for ground points, False for non-ground points.
    """
    
    # Create a 2D grid and initialize with a large value (e.g., +inf)
    grid_x = np.arange(points[:, 0].min(), points[:, 0].max(), cell_size)
    grid_y = np.arange(points[:, 1].min(), points[:, 1].max(), cell_size)
    ground_surface = np.full((len(grid_y), len(grid_x)), np.inf)
    
    # Sort points by Z
    sorted_indices = np.argsort(points[:, 2])
    sorted_points = points[sorted_indices]
    
    threshold = initial_threshold
    while threshold <= max_threshold:
        for pt in sorted_points:
            i = int((pt[0] - points[:, 0].min()) / cell_size)
            j = int((pt[1] - points[:, 1].min()) / cell_size)

            # If the point is close enough to the current ground surface, update the ground surface
            if pt[2] - ground_surface[j, i] < threshold:
                ground_surface[j, i] = pt[2]

        # Morphological opening to update the ground surface
        ground_surface = grey_opening(ground_surface, size=(3, 3))

        threshold += increment

    # Classify points as ground or non-ground based on the final ground surface
    ground_labels = np.zeros(len(points), dtype=bool)
    for idx, pt in enumerate(points):
        i = int((pt[0] - points[:, 0].min()) / cell_size)
        j = int((pt[1] - points[:, 1].min()) / cell_size)
        
        if pt[2] - ground_surface[j, i] < threshold:
            ground_labels[idx] = True
    ground_points = points[ground_labels]
    non_ground_points = points[~ground_labels]

    return ground_points, non_ground_points

# Read PLY file using PyntCloud
cloud = PyntCloud.from_file(r'F:\research\lidar\test_data\Code_steps\output\handhold_point_subset_no_outlier.ply')
xyz = cloud.xyz

csf = CSF.CSF()

# Parameter settings
csf.params.bSloopSmooth = False
csf.params.cloth_resolution = 0.1
# More details about parameter: http://ramm.bnu.edu.cn/projects/CSF/download/

csf.setPointCloud(xyz)
ground = CSF.VecInt()  # A list to indicate the index of ground points after calculation
non_ground = CSF.VecInt()  # A list to indicate the index of non-ground points after calculation
csf.do_filtering(ground, non_ground)  # Do actual filtering.

# Extract ground points
ground_points = np.array(ground)
ground_xyz = xyz[ground_points]


#cloud = PyntCloud.from_file(r'F:\research\lidar\test_data\Code_steps\output\handhold_point_subset_no_outlier.ply')
#xyz = cloud.xyz
ground_points_, non_ground_points_=approximate_pmf(ground_xyz)
# Create new PyntCloud from ground points
ground_cloud = PyntCloud(pd.DataFrame(ground_points_, columns=['x', 'y', 'z']))
ground_cloud.to_file(r"F:\research\lidar\test_data\Code_steps\output\ground_points_pmf.ply")

# %%
