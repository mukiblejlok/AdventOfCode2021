import time
from collections import defaultdict
from typing import List


class Graph:
    def __init__(self, raw_edges: List[str]):
        self._vertices, self._edges = self.initialize_graph(raw_edges)

    def __getitem__(self, item):
        return self._edges[item]

    @property
    def vertices(self):
        return self._vertices

    @staticmethod
    def initialize_graph(raw_edges):
        vertices = []
        edges = defaultdict(list)
        for edge in raw_edges:
            x, y = edge.split("-")
            if x not in vertices:
                vertices.append(x)
            if y not in vertices:
                vertices.append(y)
            edges[x].append((x, y))
            edges[y].append((y, x))
        return vertices, edges


def load_case(path: str) -> Graph:
    with open(path, "r") as f:
        lines = [line.strip() for line in f.readlines()]
    g = Graph(raw_edges=lines)
    return g


def is_small(name: str) -> bool:
    return not name.isupper()


def count_paths_in_graph(graph: Graph, start: str = "start", end: str = "end", only_once: bool = True) -> int:
    visited_vertices = defaultdict(int)

    def search_vertex(name: str, score: int = 0) -> int:
        # If we have reached end point then the score is updated
        if name == end:
            return score + 1

        if only_once and is_small(name):
            if visited_vertices[name] >= 1:
                return score
            # Add small cave to visited
            # We only need to keep track of small cave, since the big one can be visited any number of times
            visited_vertices[name] += 1

        if not only_once and is_small(name):
            visited_vertices[name] += 1
            # There is more than 1 small cave visited twice
            # or there is a small cave visited more then twice
            lvv = list(visited_vertices.values())
            if lvv.count(2) > 1 or max(lvv) > 2:
                visited_vertices[name] -= 1
                return score

        # Explore all the neighbour caves other than the start cave
        for _, neighbour_name in graph[name]:
            if neighbour_name != start:
                score = search_vertex(neighbour_name, score=score)
        # Remove small cave from visited
        if is_small(name):
            visited_vertices[name] -= 1
        return score

    return search_vertex(name=start, score=0)


if __name__ == '__main__':
    # Test
    test_graph = load_case("test.txt")
    test_result_p1 = count_paths_in_graph(test_graph, only_once=True)
    assert test_result_p1 == 10, test_result_p1
    test_result_p2 = count_paths_in_graph(test_graph, only_once=False)
    assert test_result_p2 == 36, test_result_p2

    # Part 1
    data = load_case("data.txt")
    t = time.perf_counter()
    result_p1 = count_paths_in_graph(data, only_once=True)
    print(f"Part1: {result_p1:>6} (t: {1000 * (time.perf_counter() - t):.3f} ms)")

    # Part 2
    data = load_case("data.txt")
    t = time.perf_counter()
    result_p2 = count_paths_in_graph(data, only_once=False)
    print(f"Part2: {result_p2:>6} (t: {1000 * (time.perf_counter() - t):.3f} ms)")
