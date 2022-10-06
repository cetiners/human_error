import noise
import numpy as np
import random

def toddler(size, res=32, seed=124,  octaves = 10, persistence=0.8, lacunarity = 2, mask=False):

    """
    Generate a random map using Perlin noise.
    """
    seed = random.randint(1,9999)
    scale = size/res

    if mask:
        scale, seed, octaves  = 1024 , seed , 8

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
        seed = random.randint(1,100)
        for idx, i in enumerate(map):
            map[idx][map[idx] > -0.12 ] = 1
            map[idx][map[idx] <= -0.12] = 0
        
    return map




def blurry_lines(map, vol = 8):
    """
    Blur the lines of a map.
    """

    noise = np.dstack([toddler(size=map.shape[0], seed=200, octaves=8), toddler(map.shape[0], octaves=8,seed=200)])
    noise = np.indices((map.shape[0], map.shape[0])).T + vol * noise
    noise = noise.clip(0, map.shape[0]-1).astype(np.uint32)

    blurred = np.zeros_like(map)

    for x in range(map.shape[0]):
        for y in range(map.shape[0]):
            j, i = noise[x, y]
            blurred[x, y] = map[i, j]

    return blurred


def ranger(map_name,map_1_range):

    r = view_noises[map_name]["interval"]
    r_b = []
    min_val = map_1_range[1]
    max_val = map_1_range[0]

    inc = (max_val-min_val)/r

    for i in range(1,r):
        r_b.append(min_val + (inc*i))
    return r_b


