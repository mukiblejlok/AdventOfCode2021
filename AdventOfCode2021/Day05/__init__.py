import dataclasses
import time
from collections import Counter
from typing import Optional, List


@dataclasses.dataclass(frozen=True)
class Point:
    x: int
    y: int


@dataclasses.dataclass(frozen=True)
class Pipe:
    p0: Point
    p1: Point

    @property
    def a(self) -> float:
        if self.p0.x == self.p1.x:
            return float("inf")
        return (self.p0.y - self.p1.y) / (self.p0.x - self.p1.x)

    @property
    def is_vertical(self) -> bool:
        return self.p0.x == self.p1.x

    @property
    def is_horizontal(self) -> bool:
        return self.p0.y == self.p1.y

    @property
    def is_diagonal(self) -> bool:
        return abs(self.a) == 1.0

    def list_points(self, include_diagonal: bool = False) -> List[Point]:
        points = []
        if self.is_vertical:
            s, e = (self.p0.y, self.p1.y) if self.p1.y > self.p0.y else (self.p1.y, self.p0.y)
            points = [Point(x=self.p0.x, y=y) for y in range(s, e + 1)]
        if self.is_horizontal:
            s, e = (self.p0.x, self.p1.x) if self.p1.x > self.p0.x else (self.p1.x, self.p0.x)
            points = [Point(x=x, y=self.p0.y) for x in range(s, e + 1)]
        if include_diagonal and self.is_diagonal:
            sp, ep = (self.p0, self.p1) if self.p1.x > self.p0.x else (self.p1, self.p0)
            points = [ep]
            a = int(self.a)
            while sp != ep:
                points.append(sp)
                # sp.x is always lower than ep.x, then x is always increasing, therefore x = sp.x + 1
                # while y is moving in the direction determined by a therefore y = sp.y + a
                sp = Point(x=sp.x + 1, y=sp.y + a)
        return points


def get_pipe(pipeline: str) -> Optional[Pipe]:
    try:
        p0_str, p1_str = pipeline.split("->")
        p0x, p0y = p0_str.split(",")
        p1x, p1y = p1_str.split(",")
        return Pipe(p0=Point(x=int(p0x), y=int(p0y)), p1=Point(x=int(p1x), y=int(p1y)))
    except (ValueError, TypeError):
        return None


def load_case(path: str) -> List[Pipe]:
    pipes = []
    with open(path, "r") as f:
        for line in f.readlines():
            pipe = get_pipe(line.strip())
            if pipe:
                pipes.append(pipe)
    return pipes


if __name__ == '__main__':
    test_pipes = load_case("test.txt")
    c_test1 = Counter(point for pipe in test_pipes for point in pipe.list_points(include_diagonal=False))
    c_test2 = Counter(point for pipe in test_pipes for point in pipe.list_points(include_diagonal=True))
    assert sum(1 for value in c_test1.values() if value > 1) == 5
    assert sum(1 for value in c_test2.values() if value > 1) == 12

    pipes = load_case("data.txt")
    t = time.perf_counter()
    c_p1 = Counter(point for pipe in pipes for point in pipe.list_points(include_diagonal=False))
    result_p1 = sum(1 for value in c_p1.values() if value > 1)
    print(f"Part1: {result_p1:>8} (t: {1000*(time.perf_counter() - t):.3f} ms)")


    pipes = load_case("data.txt")
    t = time.perf_counter()
    c_p2 = Counter(point for pipe in pipes for point in pipe.list_points(include_diagonal=True))
    result_p2 = sum(1 for value in c_p2.values() if value > 1)
    print(f"Part2: {result_p2:>8} (t: {1000*(time.perf_counter() - t):.3f} ms)")
