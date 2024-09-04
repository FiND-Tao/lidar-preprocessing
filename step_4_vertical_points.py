import open3d as o3d
import numpy as np

def extract_vertical_plane(pcd, threshold=0.1):
    """
    Extract points that belong to a vertical plane from a point cloud.

    Parameters:
    - pcd: open3d.geometry.PointCloud object
    - threshold: angle in degrees for considering a normal as vertical

    Returns:
    - vertical_pcd: Extracted vertical plane as an open3d.geometry.PointCloud object
    """
    
    # Estimate normals
    pcd.estimate_normals(search_param=o3d.geometry.KDTreeSearchParamHybrid(radius=0.1, max_nn=30))
    
    # Extract points whose normals are close to the vertical direction (0, 0, 1)
    normals = np.asarray(pcd.normals)
    verticality = np.abs(normals[:, 2])  # Vertical component of normals
    #mask = verticality < np.cos(np.radians(90 - threshold))
    mask = verticality < threshold
    
    return pcd.select_by_index(np.where(mask)[0])

# Load your point cloud
pcd = o3d.io.read_point_cloud(r"F:\research\lidar\test_data\Code_steps\output\point_cloud_normalized.ply")

# Extract the vertical plane
vertical_pcd = extract_vertical_plane(pcd)

# Visualize the extracted vertical plane
#o3d.visualization.draw_geometries([vertical_pcd])



# Save the extracted vertical plane to a PLY file
output_path = r"F:\research\lidar\test_data\Code_steps\output\vertical_plane_extracted.ply"
o3d.io.write_point_cloud(output_path, vertical_pcd)

# If you need to save in another format, simply change the file extension:
# For example, to save as a .pcd file:
# o3d.io.write_point_cloud("path_to_save.pcd", vertical_pcd)