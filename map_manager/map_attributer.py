
from skimage import exposure
import numpy as np
from map_manager.noise import toddler

# Creates equlized heatmaps from noisemaps to used for attributes in maps.

def histeq(img,  alpha=1):
    img_cdf, bin_centers = exposure.cumulative_distribution(img)
    img_eq = np.interp(img, bin_centers, img_cdf)
    img_eq = np.interp(img_eq, (0, 1), (-1, 1))
    return alpha * img_eq + (1 - alpha) * img

def attibuter():
    map = toddler(1024, 2, 20,octaves=1,persistence=0.5)
    uniform_map = histeq(map, alpha=0.33)

def average_cells(vor, data):
    size = vor.shape[0]
    count = np.max(vor)+1

    sum_ = np.zeros(count)
    count = np.zeros(count)

    for i in range(size):
        for j in range(size):
            p = vor[i, j]
            count[p] += 1
            sum_[p] += data[i, j]

    average = sum_/count
    average[count==0] = 0

