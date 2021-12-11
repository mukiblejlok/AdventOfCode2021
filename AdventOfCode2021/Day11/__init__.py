import time
from typing import Tuple

import numpy as np


def update_data(data: np.ndarray) -> Tuple[np.ndarray, int]:
    # Add 1 to all points
    data += 1
    visited_points = set()
    keep_going = True
    while keep_going:
        keep_going = False
        # We want to check all points greater than 9 ...
        points_to_visit = np.argwhere(data > 9)
        for ix, iy in points_to_visit:
            if (ix, iy) in visited_points:
                # ... but we skip already visited points
                continue
            # and only if there is at least one unvisited point it is worth to keep going
            keep_going = True
            # Add 1 to all neighbours
            data[max(0, ix - 1):min(data.shape[0], ix + 2), max(0, iy - 1):min(data.shape[1], iy + 2)] += 1
            # the indexing above includes the point itself and since we should only add 1 to neighbours
            # we need to remove 1 from the point itself
            data[ix, iy] -= 1
            # Finally we update the list of visited points
            visited_points.add((ix, iy))
    # Score is the number of points greater than 9
    score = int(np.sum(data > 9))
    # Reset points greater than 9
    data[data > 9] = 0
    return data, score


def simulate_steps(data, steps) -> int:
    score = 0
    for _ in range(steps):
        data, step_score = update_data(data)
        score += step_score
    return score


def find_synchronized_step(data, max_steps=1000) -> int:
    for i in range(max_steps):
        data, _ = update_data(data)
        # Synchronized step is when all values are equal to zero
        if np.all(data == 0):
            return i + 1
    raise ValueError(f"Unable to find synchronized step after {max_steps} steps")


def load_case(path: str) -> np.ndarray:
    with open(path, "r") as f:
        lines = [[int(digit.strip()) for digit in line.strip()] for line in f.readlines()]
        ar = np.array(lines)
    return ar


if __name__ == '__main__':
    # Test
    test_data = load_case("test.txt")
    test_result_p1 = simulate_steps(test_data, 100)
    assert test_result_p1 == 1656
    test_data = load_case("test.txt")
    test_result_p2 = find_synchronized_step(test_data)
    assert test_result_p2 == 195, test_result_p2

    # Part 1
    data = load_case("data.txt")
    t = time.perf_counter()
    result_p1 = simulate_steps(data, 100)
    print(f"Part1: {result_p1:>6} (t: {1000 * (time.perf_counter() - t):.3f} ms)")

    # Part 2
    data = load_case("data.txt")
    t = time.perf_counter()
    result_p2 = find_synchronized_step(data)
    print(f"Part2: {result_p2:>6} (t: {1000 * (time.perf_counter() - t):.3f} ms)")
