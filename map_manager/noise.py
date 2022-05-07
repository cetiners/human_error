from re import T
import noise
import numpy as np

def toddler(size, res=32, seed=200,  octaves = 8, persistence=0.6, lacunarity = 2, mask=False):
    scale = size/res

    if mask:
        scale, seed, octaves  = 1024 , 0 , 8

    scale = size/res

    map = np.array([[noise.snoise3(
            (x+0.1)/scale,
            y/scale,
            seed,
            octaves=octaves,
            persistence=persistence,
            lacunarity=lacunarity
        )
        for x in range(size)]
        for y in range(size)
    ])

    if mask:
        map = map > 0
        
    return map




def blurry_lines(map, vol = 8):

    noise = np.dstack([toddler(size=map.shape[0], seed=200, octaves=8), toddler(map.shape[0], octaves=8,seed=200)])
    noise = np.indices((map.shape[0], map.shape[0])).T + vol * noise
    noise = noise.clip(0, map.shape[0]-1).astype(np.uint32)

    blurred = np.zeros_like(map)

    for x in range(map.shape[0]):
        for y in range(map.shape[0]):
            j, i = noise[x, y]
            blurred[x, y] = map[i, j]

    return blurred


