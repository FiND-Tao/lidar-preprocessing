import open3d as o3d

def remove_outliers(input_file, output_file, nb_neighbors=20, std_ratio=2.0):
    """
    Remove outliers using the Statistical Outlier Removal (SOR) method.
    
    Parameters:
    - input_file: path to the input point cloud file
    - output_file: path to save the cleaned point cloud file
    - nb_neighbors: number of neighbors to use for mean distance estimation
    - std_ratio: standard deviation ratio for outlier removal
    """

    # Load point cloud
    pcd = o3d.io.read_point_cloud(input_file,format='ply')
    # Apply the SOR filter
    cleaned_pcd, ind = pcd.remove_statistical_outlier(nb_neighbors=nb_neighbors,
                                                      std_ratio=std_ratio)
    
    # Optionally visualize the inliers and outliers
    # inliers = pcd.select_by_index(ind)
    # outliers = pcd.select_by_index(ind, invert=True)
    # o3d.visualization.draw_geometries([inliers, outliers])

    # Save cleaned point cloud
    o3d.io.write_point_cloud(output_file, cleaned_pcd)

# Example usage:
remove_outliers(r'F:\research\lidar\test_data\Code_steps\data\handhold_point_subset.ply', r'F:\research\lidar\test_data\Code_steps\output\handhold_point_subset_no_outlier.ply')