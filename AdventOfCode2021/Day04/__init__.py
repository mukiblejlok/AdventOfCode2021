from typing import Sequence, List, Tuple, Optional


class Board:
    def __init__(self, numbers: Sequence[int], n: int = None):
        self.numbers = list(numbers)
        self.size = len(self.numbers)
        self.n = n if n else int(self.size ** 0.5)
        self.hits = [False] * self.size
        self.guessed_numbers = []
        # Check if it's square and it's unique
        assert self.n * self.n == self.size
        assert len(set(self.numbers)) == self.size

    def guess(self, number):
        if number in self.numbers:
            self.hits[self.numbers.index(number)] = True
            self.guessed_numbers.append(number)

    def check_bingo(self) -> Optional[List[int]]:
        for i in range(self.n):
            _rs = slice(i * self.n, (i + 1) * self.n, 1)          # row slice
            _cs = slice(i, (self.size - self.n) + i + 1, self.n)  # column slice
            if all(self.hits[_rs]):
                return self.numbers[_rs]
            if all(self.hits[_cs]):
                return self.numbers[_cs]

    @property
    def winning_number(self) -> Optional[int]:
        if self.check_bingo():
            return self.guessed_numbers[-1]

    @property
    def unmarked_numbers(self) -> List[int]:
        return [n for h, n in zip(self.hits, self.numbers) if not h]

    @property
    def score(self):
        return self.winning_number * sum(self.unmarked_numbers)

    def __repr__(self):
        return "".join([f"{e:>3} " if i % self.n else f"{e:>3}\n" for i, e in enumerate(self.numbers, 1)])


def load_case(path: str) -> Tuple[List[int], List[Board]]:
    with open(path, "r") as f:
        bingo_numbers = [int(n) for n in f.readline().split(",")]
        # skip_line
        _ = f.readline()
        board_numbers = []
        boards = []
        for line in f.readlines():
            if not line.strip():
                boards.append(Board(board_numbers))
                board_numbers = []
                continue
            board_numbers.extend([int(n) for n in line.strip().split()])
        return bingo_numbers, boards


def get_first_winning_board(numbers: List[int], boards: List[Board]) -> Board:
    for number in numbers:
        for i, board in enumerate(boards):
            board.guess(number)
            if board.check_bingo():
                return board


def get_last_winning_board(numbers: List[int], boards: List[Board]) -> Optional[Board]:
    winners = []
    for number in numbers:
        for i, board in enumerate(boards):
            if i in winners:
                continue
            board.guess(number)
            if board.check_bingo():
                winners.append(i)
                if len(winners) == len(boards):
                    return board


if __name__ == '__main__':
    # Test Case
    expected_result_1 = 188 * 24
    test_numbers, test_boards = load_case("test.txt")
    winning_board = get_first_winning_board(test_numbers, test_boards)
    assert expected_result_1 == winning_board.score

    expected_result_2 = 148 * 13
    test_numbers, test_boards = load_case("test.txt")
    last_board = get_last_winning_board(test_numbers, test_boards)
    assert expected_result_2 == last_board.score

    # Part 1
    numbers, boards = load_case("data.txt")
    winning_board = get_first_winning_board(numbers, boards)
    print(f"Part 1: {winning_board.score}")

    # Part 1
    numbers, boards = load_case("data.txt")
    last_board = get_last_winning_board(numbers, boards)
    print(f"Part 2: {last_board.score}")
