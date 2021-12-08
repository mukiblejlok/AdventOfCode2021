import time
from collections import defaultdict
from itertools import chain
from typing import Tuple, List

INITIAL_MAPPING = {2: 1, 3: 7, 4: 4, 7: 8}


def count_easy_ones(values):
    return sum((1 for value in values if len(value) in INITIAL_MAPPING))


def guess_mapping(values):
    # Part one, guess the obvious ones
    guesses = {}
    by_length = defaultdict(list)
    for value in values:
        sv = set(value)
        lv = len(value)
        if lv in INITIAL_MAPPING:
            guesses[INITIAL_MAPPING[lv]] = sv
        elif sv not in by_length[lv]:
            by_length[lv].append(sv)

    # Deduct the others
    # Find 6 - the only six segments' one that include delta 8 - 1
    s8m1 = guesses[8] - guesses[1]
    guesses[6] = [x for x in by_length[6] if s8m1.issubset(x)][0]
    by_length[6].remove(guesses[6])
    # Find 5 - the only five segments' one that is a subset of 6
    guesses[5] = [x for x in by_length[5] if x.issubset(guesses[6])][0]
    by_length[5].remove(guesses[5])
    # Find 9 - the only six segments' one that differs with 5 by only one segment
    guesses[9] = [x for x in by_length[6] if len(x - guesses[5]) == 1][0]
    by_length[6].remove(guesses[9])
    # Find 3 - the only five segments' one that is superset of 1
    guesses[3] = [x for x in by_length[5] if x.issuperset(guesses[1])][0]
    by_length[5].remove(guesses[3])
    # Find 2 - remaining five segments' one
    guesses[2] = by_length[5].pop(0)
    # Find 0 - remaining six segments' ones
    guesses[0] = by_length[6].pop(0)

    # Swap keys and values so it's easier to look it up
    mapping = {frozenset(v): k for k, v in guesses.items()}
    return mapping


def get_correct_output(in_code: str, out_code: str):
    code_mapping = guess_mapping(in_code + out_code)
    # Ugly way of building number out of digit by concatenating string
    # code = int("".join([str(code_mapping[frozenset(c)]) for c in out_code]))
    # Version without using string
    code = sum(code_mapping[frozenset(c)] * (10 ** i) for i, c in enumerate(out_code[::-1]))
    return code


def load_case(path: str) -> List[Tuple[str, str]]:
    output = []
    with open(path, "r") as f:
        for line in f.readlines():
            in_str, out_str = line.strip().split(" | ")
            output.append((in_str.strip().split(), out_str.strip().split()))
    return output


if __name__ == '__main__':
    # Test
    test_codes = load_case("test.txt")
    test_result_p1 = count_easy_ones(chain(*(b for a, b in test_codes)))
    test_result_p2 = sum((get_correct_output(*c) for c in test_codes))
    assert test_result_p1 == 26
    assert test_result_p2 == 61229

    # Part 1
    codes = load_case("data.txt")
    t = time.perf_counter()
    result_p1 = count_easy_ones(chain(*(b for a, b in codes)))
    print(f"Part1: {result_p1:>6} (t: {1000 * (time.perf_counter() - t):.3f} ms)")

    # Part 2
    t = time.perf_counter()
    result_p2 = sum((get_correct_output(*iocode) for iocode in codes))
    print(f"Part2: {result_p2:>6} (t: {1000 * (time.perf_counter() - t):.3f} ms)")
