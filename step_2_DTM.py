import numpy as np
import rasterio
from rasterio.transform import from_origin
from laspy.file import File
import laspy
from scipy.interpolate import griddata
from pyntcloud import PyntCloud

def fill_nodata(arr, nodata_value=-9999):
    """
    Fill no-data values in a 2D numpy array using interpolation.
    
    Parameters:
    - arr: 2D numpy array with no-data values.
    - nodata_value: Value representing no-data in the array.
    
    Returns:
    - Filled 2D numpy array.
    """
    
    # Create coordinate arrays
    x = np.arange(0, arr.shape[1])
    y = np.arange(0, arr.shape[0])
    xx, yy = np.meshgrid(x, y)
    
    # Mask for valid data points
    valid_mask = ~np.isnan(arr) if np.isnan(nodata_value) else arr != nodata_value
    
    # Mask for no-data points
    nodata_mask = np.isnan(arr) if np.isnan(nodata_value) else arr == nodata_value
    
    # Coordinates and values of known (valid) points
    coords_known = np.array((xx[valid_mask], yy[valid_mask])).T
    values_known = arr[valid_mask]
    
    # Coordinates of unknown (no-data) points
    coords_unknown = np.array((xx[nodata_mask], yy[nodata_mask])).T
    
    # Interpolate
    arr[nodata_mask] = griddata(coords_known, values_known, coords_unknown, method='nearest')
    
    return arr

def rasterize_las(ply_file, output_raster, resolution=0.5):
    # Read LAS file with laspy
    cloud = PyntCloud.from_file(ply_file)
    
    # Extract X, Y, and Z coordinates
    x = cloud.xyz[:, 0]
    y = cloud.xyz[:, 1]
    z = cloud.xyz[:, 2]
    
    # Create a grid to rasterize into
    x_min, y_min = np.floor([x.min(), y.min()])
    x_max, y_max = np.ceil([x.max(), y.max()])
    x_count = int((x_max - x_min) / resolution)
    y_count = int((y_max - y_min) / resolution)
    
    # Create an empty array for the DEM
    dem = np.zeros((y_count, x_count), dtype=np.float32) - 9999  # Using -9999 as a nodata value
    
    # Convert point coordinates to grid coordinates
    i = ((x - x_min) / resolution).astype(int)
    j = ((y_max - y) / resolution).astype(int)  # Note the inversion for y
    
    # Update the DEM with Z values
    for x, y, z_val in zip(i, j, z):
        if dem[y, x] < z_val:  # Take the maximum Z value if there's a conflict
            dem[y, x] = z_val
    dem_filled=fill_nodata(dem)
    # Save the DEM as a raster
    transform = from_origin(x_min, y_max, resolution, resolution)
    with rasterio.open(output_raster, 'w', driver='GTiff', height=dem.shape[0], 
                       width=dem.shape[1], count=1, dtype=dem.dtype, crs='EPSG:4326', 
                       transform=transform, nodata=-9999) as dst:
        dst.write(dem_filled, 1)

# Example usage
rasterize_las(r"F:\research\lidar\test_data\Code_steps\output\ground_points.ply", r"F:\research\lidar\test_data\Code_steps\output\ground01.tif")