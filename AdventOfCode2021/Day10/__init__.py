import time
from collections import deque
from typing import List, Optional, Sequence

closing_mapping = {
    "(": ")",
    "{": "}",
    "[": "]",
    "<": ">",
}

p1_score_mapping = {
    ")": 3,
    "]": 57,
    "}": 1197,
    ">": 25137,
}

p2_score_mapping = {
    ")": 1,
    "]": 2,
    "}": 3,
    ">": 4,
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
    return [closing_mapping[element] for element in d]


def count_broken_score(results) -> int:
    score = 0
    for result in results:
        score += p1_score_mapping.get(result, 0)
    return score


def count_closing_score(results) -> int:
    scores = []
    for result in results:
        if not result:
            continue
        score = 0
        for bracket in result:
            score *= 5
            score += p2_score_mapping.get(bracket, 0)
        scores.append(score)
    middle_score = sorted(scores)[len(scores) // 2]
    return middle_score


def load_case(path: str) -> List[str]:
    with open(path, "r") as f:
        return [line.strip() for line in f.readlines()]


if __name__ == '__main__':
    # Test
    test_data = load_case("test.txt")
    test_result_p1 = count_broken_score(find_broken_line(line) for line in test_data)
    assert test_result_p1 == 26397
    test_result_p2 = count_closing_score(find_closing_brackets(line) for line in test_data)
    assert test_result_p2 == 288957

    # Part 1
    data = load_case("data.txt")
    t = time.perf_counter()
    result_p1 = count_broken_score(find_broken_line(line) for line in data)
    print(f"Part1: {result_p1:>10} (t: {1000 * (time.perf_counter() - t):.3f} ms)")

    # Part 2
    t = time.perf_counter()
    result_p2 = values = count_closing_score(find_closing_brackets(line) for line in data)
    print(f"Part2: {result_p2:>10} (t: {1000 * (time.perf_counter() - t):.3f} ms)")
