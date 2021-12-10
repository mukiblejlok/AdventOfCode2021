import time
from typing import List, Tuple
from collections import deque
import numpy as np


def load_case(path: str) -> np.ndarray:
    with open(path, "r") as f:
        lines = [[int(digit.strip()) for digit in line.strip()] for line in f.readlines()]
        ar = np.array(lines)
    return ar


def find_2d_mins(data: np.ndarray) -> np.ndarray:
    border_val = 9
    # add borders with high values
    bd = np.ones((data.shape[0] + 2, data.shape[1] + 2)) * border_val
    bd[1:-1, 1:-1] = data
    # if point is smaller then the left right top and bottom point then it is considered a minimum point
    #            LEFT                    RIGHT                  BOTTOM                     TOP
    m = (data < bd[1:-1, :-2]) & (data < bd[1:-1, 2:]) & (data < bd[:-2, 1:-1]) & (data < bd[2:, 1:-1])
    return m


def get_basin_size(data: np.ndarray, point: Tuple[int, int]) -> int:
    minx, miny, maxx, maxy = 0, 0, data.shape[0] - 1, data.shape[1] - 1
    points_to_visit = deque([point])
    visited_points = set()
    size = 0
    while points_to_visit:
        # Take next point for analysis
        px, py = points_to_visit.pop()
        # Check if it is a part of basin or if it was already checked
        if (px, py) in visited_points or data[px, py] >= 9:
            continue
        # Since it is a part of basin update the size and visited points
        size += 1
        visited_points.add((px, py))
        # Calculate neighbour points
        lp = max(minx, px - 1), py
        rp = min(maxx, px + 1), py
        bp = px, max(miny, py - 1)
        tp = px, min(maxy, py + 1)
        # And add them to 'points_to_visit' it they were not already visited
        for new_point in (lp, rp, bp, tp):
            if new_point not in visited_points:
                points_to_visit.append(new_point)
    return size


def sum_risks(values: List[int]) -> int:
    return sum(x + 1 for x in values)


if __name__ == '__main__':
    # Test
    test_data = load_case("test.txt")
    test_min_values = find_2d_mins(test_data)
    test_result_p1 = sum_risks(test_data[test_min_values])
    assert test_result_p1 == 15
    test_sizes = sorted([get_basin_size(test_data, point) for point in np.argwhere(test_min_values)], reverse=True)
    test_result_p2 = test_sizes[0] * test_sizes[1] * test_sizes[2]
    assert test_result_p2 == 1134

    # Part 1
    data = load_case("data.txt")
    t = time.perf_counter()
    min_values = find_2d_mins(data)
    result_p1 = sum_risks(data[min_values])
    print(f"Part1: {result_p1:>8} (t: {1000 * (time.perf_counter() - t):.3f} ms)")

    # Part 2
    t = time.perf_counter()
    basin_sizes = sorted([get_basin_size(data, location) for location in np.argwhere(min_values)], reverse=True)
    result_p2 = basin_sizes[0] * basin_sizes[1] * basin_sizes[2]
    print(f"Part2: {result_p2:>8} (t: {1000 * (time.perf_counter() - t):.3f} ms)")
