from typing import List


class Sea:
    def __init__(self, fishes: List[int]):
        self.fishes_by_age = [0] * 9

        for age in fishes:
            self.fishes_by_age[age] += 1

    def simulate_days(self, days: int):
        for _ in range(days):
            # Fishes at age 0 creates new fishes
            # So let's pop those
            # and that will simulate all fished getting older by one day
            ready_fishes = self.fishes_by_age.pop(0)
            # now we can add those popped fishes at the end of list
            # that will be an equivalent of adding new fishes to the pond
            # last position is index 8 so this means they would require 8 days to grow
            self.fishes_by_age.append(ready_fishes)
            # additionally we must update number of fishes that require 6 more days grow
            # with number of fishes that just gave a birth
            self.fishes_by_age[6] += ready_fishes
        return sum(self.fishes_by_age)


if __name__ == '__main__':
    # Test
    test_initial_state = [3, 4, 3, 1, 2]
    test_sea = Sea(fishes=test_initial_state)
    assert test_sea.simulate_days(80) == 5934
    test_sea = Sea(fishes=test_initial_state)
    assert test_sea.simulate_days(256) == 26984457539

    # Part 1 & 2
    with open("data.txt", "r") as f:
        initial_state = [int(i) for i in f.readline().strip().split(",")]
    data_sea = Sea(initial_state)
    print(f"Part1: {data_sea.simulate_days(80)}")
    data_sea = Sea(initial_state)
    print(f"Part2: {data_sea.simulate_days(256)}")
