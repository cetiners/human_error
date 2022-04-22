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