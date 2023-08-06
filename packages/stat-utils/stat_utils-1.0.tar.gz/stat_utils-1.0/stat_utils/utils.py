import numpy as np
from typing import List, Union, Tuple

def fast_hist(array: List[Union[int, float]], 
              bins: int) -> Tuple[List[int], List[float]]:
    """
    Builds bins' labels and bins' value counts for given array
    :param array: array with numeric values
    :param bins:  number of bins in result distribution
    :return: Two lists: 
             first contains value counts of each bin,
             second contains list of bins' labels
    """
    if (bins <= 0): 
        raise ValueError("bins number must be positive")
    
    array_min = np.min(array)
    step = (np.max(array) - array_min) / bins
    labels = [array_min + i*step for i in range(0, bins + 1)]
    bin_numbers = np.searchsorted(labels, array, side='right') - 1
    
    counts = np.bincount(bin_numbers)
    counts[-2] += counts[-1]
    
    return counts[:-1], labels