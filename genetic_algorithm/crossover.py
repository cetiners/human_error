

def coordinate_xo(parent_1, parent_2):

    """
    Takes two individual coordinate points as parents. Takes one coordinate axis from each to create two offsprings.
    """

    child_1 = [parent_1[0],parent_2[1]]
    child_2 = [parent_2[0],parent_1[1]]

    return child_1,child_2

def partially_mapped_xo(parent_1,parent_2):
    """
    Takes a "pack" of world encounters, 
    """
    pass
