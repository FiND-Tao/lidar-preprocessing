#%%
import numpy as np
import CSF
from pyntcloud import PyntCloud
import pandas as pd
# Read PLY file using PyntCloud
cloud = PyntCloud.from_file(r'F:\research\lidar\test_data\Code_steps\output\handhold_point_subset_no_outlier.ply')
#cloud = PyntCloud.from_file(r'D:\SmallPlot\Smallplot_merged_2_subset.ply')
#cloud = PyntCloud.from_file(r'D:\downsample\003.downsample.ply')
#cloud = PyntCloud.from_file(r'D:\SmallPlot\003_binary.ply')
#cloud = PyntCloud.from_file(r'F:\research\lidar\test_data\Code_steps\output\handhold_point_subset_no_outlier.ply')

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

# Create new PyntCloud from ground points
ground_cloud = PyntCloud(pd.DataFrame(ground_xyz, columns=['x', 'y', 'z']))
#ground_cloud.to_file(r"F:\research\lidar\test_data\Code_steps\output\ground_points.ply")
ground_cloud.to_file(r"F:\research\lidar\test_data\Code_steps\output\ground_points_hongxiang.ply")


# %%
