import time
from typing import Tuple, List

import numpy as np


def load_case(path: str) -> Tuple[np.ndarray, List[Tuple[str, int]]]:
    with open(path, "r") as f:
        points = []
        folds = []
        add_points = True
        for line in f.readlines():
            if not line.strip():
                add_points = False
                continue
            if add_points:
                x, y = (int(x) for x in line.strip().split(","))
                points.append((x, y))
            else:
                # skip "fold along "
                d, v = line.strip()[11:].split("=")
                folds.append((d, int(v)))
        sheet = np.zeros((max(p[1] for p in points) + 1, max(p[0] for p in points) + 1)).astype(bool)
        for x, y in points:
            sheet[y, x] = True
    return sheet, folds


def fold(ar: np.ndarray, axis: str, line: int) -> np.ndarray:
    f1 = slice(None, line, 1)
    f2 = slice(None, line, -1)
    return ar[f1, :] + ar[f2, :] if axis == "y" else ar[:, f1] + ar[:, f2]


def pprint_data(ar: np.ndarray) -> None:
    for row in ar:
        line = "".join("█" if e else " " for e in row)
        print(line)


if __name__ == '__main__':
    # Test
    test_sheet, test_folds = load_case("test.txt")
    # Fold once
    folded_test_sheet = fold(test_sheet, *test_folds[0])
    test_result_p1 = np.sum(folded_test_sheet).astype(int)
    assert test_result_p1 == 17, test_result_p1
    # Fold all
    test_sheet, test_folds = load_case("test.txt")
    for a, l in test_folds:
        test_sheet = fold(test_sheet, a, l)
    pprint_data(test_sheet)

    # Part 1
    data_sheet, data_folds = load_case("data.txt")
    t = time.perf_counter()
    # Fold once
    folded_sheet = fold(data_sheet, *data_folds[0])
    result_p1 = np.sum(folded_sheet).astype(int)
    print(f"Part1: {result_p1:>8} (t: {1000 * (time.perf_counter() - t):.3f} ms)")

    # Part 2
    data_sheet, data_folds = load_case("data.txt")
    t = time.perf_counter()
    for a, l in data_folds:
        data_sheet = fold(data_sheet, a, l)
    result_p2 = "BLHFJPJF"
    print(f"Part2: {result_p2:>8} (t: {1000 * (time.perf_counter() - t):.3f} ms)")
    pprint_data(data_sheet)
