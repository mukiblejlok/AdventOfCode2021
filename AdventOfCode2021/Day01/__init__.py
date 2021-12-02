from typing import List


def diff(numbers: List[int]) -> List[int]:
    return [n1 - n0 for n0, n1 in zip(numbers, numbers[1:])]


def sum_window_3(numbers: List[int]) -> List[int]:
    return [a + b + c for a, b, c in zip(numbers, numbers[1:], numbers[2:])]


def no_of_positive_numbers(numbers: List[int]) -> int:
    return sum(n > 0 for n in numbers)


if __name__ == '__main__':
    with open("data.txt", "r") as f:
        measurements = [int(line.strip()) for line in f.readlines()]

    no_of_positive_diffs = no_of_positive_numbers(diff(measurements))
    print(f"Part 1: {no_of_positive_diffs}")

    no_of_positive_diffs3 = no_of_positive_numbers(diff(sum_window_3(measurements)))
    print(f"Part 2: {no_of_positive_diffs3}")
