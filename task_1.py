"""
LRU Cache Optimization for Range Sum Queries

This module provides functions to process range sum and update queries on a list of integers both with
and without an LRU (Least Recently Used) cache to optimize repeated range sum computations.

Functions:
- range_sum_no_cache(array, L, R): Compute sum of elements from L to R without caching.
- update_no_cache(array, index, value): Update element at index without affecting any cache.
- range_sum_with_cache(array, L, R): Compute sum using an LRU cache for previously computed ranges.
- update_with_cache(array, index, value): Update element at index and invalidate the cache.

"""
import random
import time
from functools import lru_cache


def range_sum_no_cache(array, L, R):
    """
    Compute the sum of elements in `array` from index L to R inclusive without using any cache.

    Parameters:
    array (List[int]): The list of integers.
    L (int): Start index (0-based).
    R (int): End index (0-based).

    Returns:
    int: Sum of array[L:R+1].
    """
    return sum(array[L:R+1])


def update_no_cache(array, index, value):
    """
    Update the element of `array` at the specified index to the new value without any cache operations.

    Parameters:
    array (List[int]): The list of integers.
    index (int): Index of the element to update (0-based).
    value (int): New value to assign.
    """
    array[index] = value


@lru_cache(maxsize=1000)
def _cached_sum(array_id, L, R):
    """
    Internal helper that computes the sum of a range and is cached based on (array_id, L, R).

    Parameters:
    array_id (int): Unique identifier of the array (use id(array)).
    L (int): Start index (0-based).
    R (int): End index (0-based).

    Returns:
    int: Sum of array[L:R+1].
    """
    # Note: relies on the global `array` variable bound in the main block.
    return sum(array[L:R+1])


def range_sum_with_cache(array, L, R):
    """
    Compute the sum of elements in `array` from index L to R inclusive, using an LRU cache
    to store and retrieve previously computed results.

    Parameters:
    array (List[int]): The list of integers.
    L (int): Start index (0-based).
    R (int): End index (0-based).

    Returns:
    int: Sum of array[L:R+1], retrieved from cache if available.
    """
    return _cached_sum(id(array), L, R)


def update_with_cache(array, index, value):
    """
    Update the element of `array` at the specified index to the new value and clear the cache
    to ensure subsequent range sums are recalculated.

    Parameters:
    array (List[int]): The list of integers.
    index (int): Index of the element to update (0-based).
    value (int): New value to assign.
    """
    array[index] = value
    _cached_sum.cache_clear()


if __name__ == "__main__":
    # Configuration
    N = 100_000  # Size of the array
    Q = 50_000   # Number of queries

    # Generate a random array of size N
    array = [random.randint(1, 100) for _ in range(N)]

    queries = []
    for _ in range(Q):
        if random.random() < 0.5:
            L = random.randint(0, N - 1)
            R = random.randint(L, N - 1)
            queries.append(('Range', L, R))
        else:
            idx = random.randint(0, N - 1)
            val = random.randint(1, 100)
            queries.append(('Update', idx, val))

    # Measure execution time without cache
    start_time_no_cache = time.time()
    for q in queries:
        if q[0] == 'Range':
            range_sum_no_cache(array, q[1], q[2])
        else:
            update_no_cache(array, q[1], q[2])
    time_no_cache = time.time() - start_time_no_cache

    # Measure execution time with LRU cache
    start_time_with_cache = time.time()
    for q in queries:
        if q[0] == 'Range':
            range_sum_with_cache(array, q[1], q[2])
        else:
            update_with_cache(array, q[1], q[2])
    time_with_cache = time.time() - start_time_with_cache

    # Output results
    print(f"Execution time without cache: {time_no_cache:.2f} seconds")
    print(f"Execution time with LRU cache: {time_with_cache:.2f} seconds")
