import time
from typing import List, Callable


def load_case(path: str) -> List[int]:
    with open(path, "r") as f:
        return [int(x) for x in f.readline().split(",")]


def distance_p1(x, y):
    return abs(x - y)


def distance_p2(x, y):
    # Thanks to Gauss, sum(range(n + 1)) can be simplified to: n * n (n + 1) // 2
    n = abs(x - y)
    return n * (n + 1) // 2


def half_point(left: int, right: int) -> int:
    return (right - left) // 2 + left


def find_closest_point(numbers: List, distance_func: Callable):
    """
    Simple approach would check all points between min and max in numbers list. This will be O(n) complexity.
    But it looks that the cost function has only one (global) minimum,
    so the bisect algorithm can be used to find the optimum. This reduces complexity to O(log n).

    # Simple Solution:
    for point in range(min(numbers), max(numbers)):
        distance = sum(distance_func(point, p) for p in numbers)
        if distance < min_distance:
            min_distance = distance
            closest_point = point
    return min_distance, closest_point
    """

    left_limit, right_limit = min(numbers), max(numbers)
    mid_point = half_point(left_limit, right_limit)
    while True:
        left_point = half_point(left_limit, mid_point)
        right_point = half_point(mid_point, right_limit)
        left_distance = sum(distance_func(left_point, p) for p in numbers)
        right_distance = sum(distance_func(right_point, p) for p in numbers)
        if left_distance < right_distance:
            right_limit = mid_point
            mid_point = left_point
        elif left_distance > right_distance:
            left_limit = mid_point
            mid_point = right_point
        else:
            return left_distance, left_point


if __name__ == '__main__':
    test_case = load_case("test.txt")
    min_distance_t1, _ = find_closest_point(test_case, distance_func=distance_p1)
    min_distance_t2, _ = find_closest_point(test_case, distance_func=distance_p2)
    assert min_distance_t1 == 37
    assert min_distance_t2 == 168

    # Part 1
    data = load_case("data.txt")
    t = time.perf_counter()
    min_distance_p1, best_point_p1 = find_closest_point(data, distance_func=distance_p1)
    print(f"Part1: {min_distance_p1:>10} (p: {best_point_p1}, t: {time.perf_counter() - t:.3f})")

    # Part 2
    t = time.perf_counter()
    min_distance_p2, best_point_p2 = find_closest_point(data, distance_func=distance_p2)
    print(f"Part2: {min_distance_p2:>10} (p: {best_point_p2}, t: {time.perf_counter() - t:.3f})")
