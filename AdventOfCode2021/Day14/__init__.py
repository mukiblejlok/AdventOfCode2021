import time
from collections import Counter
from functools import lru_cache
from typing import Tuple, Dict


def load_case(path: str) -> Tuple[str, Dict]:
    with open(path, "r") as f:
        initial_polymer = f.readline().strip()
        # skip one line
        f.readline()
        # Read rules
        rules_dict = {}
        for line in f.readlines():
            m, a = line.strip().split(" -> ")
            rules_dict[m] = a
    return initial_polymer, rules_dict


def grow_polymer_naive(polymer: str, rules: Dict) -> str:
    elements_of_new_polymer = []
    for e0, e1 in zip(polymer, polymer[1:]):
        elements = f"{e0}{e1}"
        middle_element = rules.get(elements)
        new_element = f"{e0}{middle_element}" if middle_element else e0
        elements_of_new_polymer.append(new_element)
    elements_of_new_polymer.append(polymer[-1])
    new_polymer = "".join(elements_of_new_polymer)
    return new_polymer


def count_polymer(initial_polymer: str, rules: Dict, steps: int) -> Counter:

    # Recursive function following the grow of a single pair
    # and returning a counter after provided number of steps
    @lru_cache(maxsize=None)
    def count_pair(pair: str, step: int) -> Counter:
        # Recursion exit step
        if step >= steps or pair not in rules:
            return Counter()
        # Update step number
        step += 1
        c0, c1 = pair
        # Get middle Element
        middle_element = rules.get(pair)
        # Initialize counter with middle element
        c = Counter(middle_element)
        # Recursively count for left & right pairs
        left_pair_count = count_pair(pair=f"{c0}{middle_element}", step=step)
        right_pair_count = count_pair(pair=f"{middle_element}{c1}", step=step)
        # Update counter and return it
        c.update(left_pair_count)
        c.update(right_pair_count)
        return c

    total_counter = Counter(initial_polymer)
    for e0, e1 in zip(initial_polymer, initial_polymer[1:]):
        # Update total counter for every pair in initial polymer
        pair_count = count_pair(pair=f"{e0}{e1}", step=0)
        total_counter.update(pair_count)

    return total_counter


def count_score(polymer_counter: Counter) -> int:
    mc = polymer_counter.most_common()
    # Most common count minus least common count
    score = mc[0][1] - mc[-1][1]
    return score


if __name__ == '__main__':
    # Test
    test_polymer, test_rules = load_case("test.txt")
    test_result_p1 = count_score(polymer_counter=count_polymer(test_polymer, test_rules, 10))
    assert test_result_p1 == 1588, test_result_p1

    test_polymer, test_rules = load_case("test.txt")
    test_result_p2 = count_score(polymer_counter=count_polymer(test_polymer, test_rules, 40))
    assert test_result_p2 == 2188189693529, test_result_p2

    # Part 1
    polymer, rules = load_case("data.txt")
    t = time.perf_counter()
    result_p1 = count_score(polymer_counter=count_polymer(polymer, rules, 10))
    print(f"Part1: {result_p1:>15} (t: {1000 * (time.perf_counter() - t):.3f} ms)")

    # Part 2
    polymer, rules = load_case("data.txt")
    t = time.perf_counter()
    result_p2 = count_score(polymer_counter=count_polymer(polymer, rules, 40))
    print(f"Part2: {result_p2:>15} (t: {1000 * (time.perf_counter() - t):.3f} ms)")
