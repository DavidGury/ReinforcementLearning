import numpy as np
import numpy.typing as npt
from typing import Any
import re
from enum import Enum


class AutoNumber(Enum):
    def __new__(cls, *args):
        value = len(cls.__members__)
        obj = object.__new__(cls)
        obj._value_ = value
        return obj


def rand_wtd_index(array: npt.NDArray[int], alter_inplace: bool = False):
    """
    Takes 1-d array of integers (in most use cases, this array will represent remaining quantities of items
    Using those quantities as weights, returns a randomly selected index ("choosing" an item in the array)
    """
    dims = len(array.shape)
    if dims != 1:
        print(f'Func rand_weighted_index requires 1d array.  Array given is shape {dims}.')
    rng = np.random.randint(low=1, high=100, size=array.shape, dtype=np.uint8)

    pick = np.argmax(array*rng)

    if alter_inplace:
        array[pick] -= 1

    return pick


def make_even_lengths(board_conns):
    """
    Given a 2d list (list of lists)
    Fills out sublists with repeats of their last index to make
    their length equal to the longest-length sublist
    """
    conn_lists = board_conns.copy()
    maxconns = max(map(len,conn_lists))
    for t in range(len(conn_lists)):
        while len(conn_lists[t]) < maxconns:
            conn_lists[t].append(conn_lists[t][-1])
    return conn_lists


array_isinstance = np.vectorize(lambda element, dtype: isinstance(element, dtype))
conv_obj2attr = np.vectorize(lambda obj, attr_str: getattr(obj, attr_str, 0))


def array_elements_within_range(array: npt.NDArray[int | np.uint8 | Any], low: int, high: int):
    """
    Returns truth array, where elements are found True if (low <= element < high)
    """
    return np.where(
        np.logical_and(
            array >= low,
            array < high))


if __name__ == '__main__':
    ...


