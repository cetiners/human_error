import noise
import numpy as np

def toddler(size=1024, scale = 500, octaves = 20, persistence = 0.60, lacunarity = 2, mask=False):
    shape = (size,size)

    map = np.zeros(shape)

    for i in range(shape[0]):

        for j in range(shape[1]):

            map[i][j] = noise.pnoise2(i/scale, 
                                        j/scale, 
                                        octaves=octaves, 
                                        persistence=persistence, 
                                        lacunarity=lacunarity, 
                                        repeatx=size, 
                                        repeaty=size, 
                                        base=0)
    if mask:
        map = map > 0
        
    return map

def proper_map(map, size,noise_map):
    boundary_displacement = 20
    boundary_noise = np.dstack([noise_map(size, 32, 120, octaves=8), noise_map(size, 32, 250, octaves=8)])
    boundary_noise = np.indices((size, size)).T + boundary_displacement*boundary_noise
    boundary_noise = boundary_noise.clip(0, size-1).astype(np.uint32)

    blurred_vor_map = np.zeros_like(map)

    for x in range(size):
        for y in range(size):
            j, i = boundary_noise[x, y]
            blurred_vor_map[x, y] = map[i, j]