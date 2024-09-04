import rasterio
import numpy as np
from scipy.ndimage import gaussian_filter
from scipy.ndimage import uniform_filter
def smooth_dtm(dtm_file, output_file, sigma=1):
    # Load the DTM data
    with rasterio.open(dtm_file, 'r') as src:
        dtm_data = src.read(1)
        profile = src.profile

        # Apply the Gaussian filter
        #smoothed_data = gaussian_filter(dtm_data, sigma=sigma)
        # Apply the moving average filter
        smoothed_data = uniform_filter(dtm_data, size=sigma)
        # Save the smoothed DTM
        with rasterio.open(output_file, 'w', **profile) as dst:
            dst.write(smoothed_data, 1)

# Example usage
smooth_dtm(r"F:\research\lidar\test_data\Code_steps\output\ground01.tif", r"F:\research\lidar\test_data\Code_steps\output\ground01_smoothed.tif", sigma=5)
