import dataclasses
import time
from typing import List, TypeVar, Generic, Optional, Tuple
import heapq
import matplotlib.pyplot as plt
import matplotlib.cm as cm

T = TypeVar("T")


@dataclasses.dataclass()
class Point:
    x: int
    y: int
    d: int

    def __lt__(self, other):
        return self.d < other.d

    def __eq__(self, other):
        return self.d == other.d


class PriorityQueue(Generic[T]):
    def __init__(self):
        self._list: List[T] = []

    @property
    def empty(self):
        return not self._list

    def push(self, item: T) -> None:
        heapq.heappush(self._list, item)

    def pop(self) -> T:
        return heapq.heappop(self._list)

    def __repr__(self):
        return repr(self._list)


def load_case(path: str) -> List[List[int]]:
    with open(path, "r") as f:
        data = [[int(e) for e in line.strip()] for line in f.readlines()]
    return data


def multiply_data(data: List[List[int]], factor: int = 2) -> List[List[int]]:
    new_data = []
    for fy in range(factor):
        for row in data:
            new_row = []
            for fx in range(factor):
                new_row += [((element-1 + fx + fy) % 9 + 1) for element in row]
            new_data.append(new_row)
    return new_data


def get_available_points(data, point: Point):
    # LEFT
    if point.x + 1 < len(data[0]):
        yield point.x + 1, point.y
    # DOWN
    if point.y + 1 < len(data):
        yield point.x, point.y + 1
    # RIGHT
    if point.x > 0:
        yield point.x - 1, point.y
    # TOP
    if point.y > 0:
        yield point.x, point.y - 1


def find_shortest_path(
        data: List[List[int]],
        start_point: Tuple = None,
        end_point: Tuple = None,
) -> Tuple[Optional[int], List[Tuple[int]]]:
    sx, sy = start_point if start_point else (0, 0)
    ex, ey = end_point if end_point else (len(data[0]) - 1, len(data) - 1)

    distances = {}
    path_dict = {}
    distances[(sx, sy)] = 0
    pq = PriorityQueue()

    pq.push(Point(sx, sy, 0))
    while not pq.empty:
        c = pq.pop()
        distance_to_current_point = distances.get((c.x, c.y))
        for nx, ny in get_available_points(data, c):
            distance_to_next_point = distances.get((nx, ny))
            total_distance = data[ny][nx] + distance_to_current_point
            if distance_to_next_point is None or distance_to_next_point > total_distance:
                distances[(nx, ny)] = total_distance
                path_dict[(nx, ny)] = (c.x, c.y)
                pq.push(Point(nx, ny, total_distance))

    end_path = [(ex, ey)]
    e = path_dict[(ex, ey)]
    end_path.append(e)
    while e[0] != sx or e[1] != sy:
        e = path_dict[(e[0], e[1])]
        end_path.append(e)

    return distances[(ex, ey)], end_path[::-1]


def plot_path(data, path):
    plt.imshow(data, cmap=cm.Reds)
    plt.plot(*path[0], "bo", linestyle="none")
    plt.plot(*path[-1], "b<", linestyle="none")
    for p0, p1 in zip(path, path[1:]):
        plt.plot([p0[0], p1[0]], [p0[1], p1[1]], "b")
    plt.show()


if __name__ == '__main__':
    # Test
    test_data = load_case("test.txt")
    # print(test_data)
    test_result_p1, test_end_path = find_shortest_path(test_data)
    plot_path(test_data, test_end_path)
    assert test_result_p1 == 40, test_result_p1

    test_data_2 = multiply_data(test_data, factor=5)
    test_result_p2, test_end_path_2 = find_shortest_path(test_data_2)
    assert test_result_p2 == 315, test_result_p2
    plot_path(test_data_2, test_end_path_2)

    # Part 1
    data = load_case("data.txt")
    t = time.perf_counter()
    result_p1, end_path = find_shortest_path(data)
    print(f"Part1: {result_p1:>6} (t: {1000 * (time.perf_counter() - t):.3f} ms)")
    plot_path(data, end_path)

    # Part 2
    data_2 = multiply_data(data, factor=5)
    t = time.perf_counter()
    result_p2, end_path_2 = find_shortest_path(data_2)
    print(f"Part2: {result_p2:>6} (t: {1000 * (time.perf_counter() - t):.3f} ms)")
    plot_path(data_2, end_path_2)
