import time
from collections import deque
from typing import List, Optional

closing_mapping = {
    "(": ")",
    "{": "}",
    "[": "]",
    "<": ">",
}

score_mapping = {
    ")": 3,
    "]": 57,
    "}": 1197,
    ">": 25137,
}


def find_broken_line(line: str) -> Optional[str]:
    d = deque()
    for char in line:
        if char in closing_mapping.keys():
            d.appendleft(char)
            continue
        expected_closing_char = closing_mapping[d.popleft()]
        if expected_closing_char != char:
            return char
    return None


def find_closing_brackets(line: str) -> Optional[List[str]]:
    d = deque()
    for char in line:
        if char in closing_mapping.keys():
            d.appendleft(char)
            continue
        expected_closing_char = closing_mapping[d.popleft()]
        if expected_closing_char != char:
            return None
    return list(closing_mapping[element] for element in d)


def count_broken_score(results: List[Optional[str]]) -> int:
    score = 0
    for result in results:
        score += score_mapping.get(result, 0)
    return score


def count_closing_score(brackets: List[str]) -> int:
    score = 0
    for result in results:
        score += score_mapping.get(result, 0)
    return score



def load_case(path: str) -> List[str]:
    with open(path, "r") as f:
        return [line.strip() for line in f.readlines()]


if __name__ == '__main__':
    # Test
    test_data = load_case("test.txt")
    test_result_p1 = count_broken_score(find_broken_line(line) for line in test_data)
    assert test_result_p1 == 26397
    # test_sizes = sorted([get_basin_size(test_data, point) for point in np.argwhere(test_min_values)], reverse=True)
    for line in test_data:
        print(find_closing_brackets(line))
    # test_result_p2 = test_sizes[0] * test_sizes[1] * test_sizes[2]
    # assert test_result_p2 == 288957

    # Part 1
    data = load_case("data.txt")
    t = time.perf_counter()
    result_p1 = count_broken_score(find_broken_line(line) for line in data)
    print(f"Part1: {result_p1:>8} (t: {1000 * (time.perf_counter() - t):.3f} ms)")

    # Part 2
    t = time.perf_counter()
    # basin_sizes = sorted([get_basin_size(data, location) for location in np.argwhere(min_values)], reverse=True)
    # result_p2 = basin_sizes[0] * basin_sizes[1] * basin_sizes[2]
    # print(f"Part2: {result_p2:>8} (t: {1000 * (time.perf_counter() - t):.3f} ms)")
