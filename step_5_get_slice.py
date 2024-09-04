import numpy as np
from pyntcloud import PyntCloud
import random
import seaborn as sns
import pyvista as pv
from sklearn.cluster import DBSCAN
import pandas as pd
# 1. Load the point cloud
cloud = PyntCloud.from_file(r"F:\research\lidar\test_data\Code_steps\output\vertical_plane_extracted.ply")
points = cloud.points[["x", "y", "z"]].values

# 2. Filter points based on Z-coordinate
threshold_min = [ 0.5+i for i in range(20)]
threshold_max = 9
for i,threshold in enumerate(threshold_min):
    selected_indices = np.where((points[:, 2] > threshold) & (points[:, 2] < threshold+1))[0]
    filtered_points = points[selected_indices]

    # 3. Create a new PyntCloud with the filtered points
    filtered_cloud = PyntCloud(pd.DataFrame(filtered_points, columns=['x', 'y', 'z']))

    # Save filtered point cloud
    output_path = r"F:\research\lidar\test_data\Code_steps\output\point_slice\slice_{}.ply".format(i)
    filtered_cloud.to_file(output_path)