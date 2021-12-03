from collections import Counter
from typing import List


def count_bits(binary_strings: List[str]) -> List[Counter]:
    counters = [Counter() for _ in range(len(binary_strings[0]))]
    for binary_string in binary_strings:
        for i, char in enumerate(binary_string):
            counters[i][char] = counters[i].get(char, 0) + 1
    return counters


def filter_out_string(binary_strings: List[str], most_common: bool = True) -> str:
    position = 0
    while len(binary_strings) > 1 and position < len(binary_strings[0]):
        counters = count_bits(binary_strings)
        most_dominant_char, most_dominant_no = counters[position].most_common()[0]
        least_dominant_char, least_dominant_no = counters[position].most_common()[-1]
        is_the_same = most_dominant_no == least_dominant_no
        if most_common:
            dominant_bit = "1" if is_the_same else most_dominant_char
        else:
            dominant_bit = "0" if is_the_same else least_dominant_char
        binary_strings = [s for s in binary_strings if s[position] == dominant_bit]
        position += 1

    assert len(binary_strings) == 1
    return "".join(binary_strings)


if __name__ == '__main__':
    test_case = [
        "00100",
        "11110",
        "10110",
        "10111",
        "10101",
        "01111",
        "00111",
        "11100",
        "10000",
        "11001",
        "00010",
        "01010",
    ]
    expected_answer1 = 22 * 9
    expected_answer2 = 23 * 10
    # Test Case 1
    test_case_bit_count = count_bits(test_case)
    most_common_bit_string = "".join([counter.most_common()[0][0] for counter in test_case_bit_count])
    least_common_bit_string = "".join([counter.most_common()[-1][0] for counter in test_case_bit_count])
    most_common_int = int(most_common_bit_string, 2)
    least_common_int = int(least_common_bit_string, 2)
    assert most_common_int * least_common_int == expected_answer1
    # Test Case 2
    p2_most_common_str = filter_out_string(test_case, most_common=True)
    p2_least_common_str = filter_out_string(test_case, most_common=False)
    p2_most_common_int = int(p2_most_common_str, 2)
    p2_least_common_int = int(p2_least_common_str, 2)
    assert p2_least_common_int * p2_most_common_int == expected_answer2

    with open("data.txt", "r") as f:
        data = [line.strip() for line in f.readlines()]
    # Part 1
    data_count = count_bits(data)
    most_common_bit_string = "".join([counter.most_common()[0][0] for counter in data_count])
    least_common_bit_string = "".join([counter.most_common()[-1][0] for counter in data_count])
    most_common_int = int(most_common_bit_string, 2)
    least_common_int = int(least_common_bit_string, 2)
    print(f"Part 1: {most_common_int * least_common_int}")

    # Part 2
    p2_most_common_str = filter_out_string(data, most_common=True)
    p2_least_common_str = filter_out_string(data, most_common=False)
    p2_most_common_int = int(p2_most_common_str, 2)
    p2_least_common_int = int(p2_least_common_str, 2)
    print(f"Part 2: {p2_most_common_int * p2_least_common_int}")
