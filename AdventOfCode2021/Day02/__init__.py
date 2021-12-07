import time


class Position:

    def __init__(self, x: int = 0, y: int = 0, aim: int = 0):
        self.x = x
        self.y = y
        self.aim = aim

    def move(self, movement: str, value: int) -> None:
        movement = str(movement).casefold()
        value = int(value)
        if movement == "forward":
            self.x += value
        if movement == "up":
            self.y -= value
        if movement == "down":
            self.y += value

    def move_with_aim(self, movement: str, value: int) -> None:
        movement = str(movement).casefold()
        value = int(value)
        if movement == "forward":
            self.x += value
            self.y += self.aim * value
        if movement == "up":
            self.aim -= value
        if movement == "down":
            self.aim += value

    def __repr__(self):
        return f"Position(x={self.x}, y={self.y}, aim={self.aim})"


if __name__ == '__main__':

    test_case = [
        "forward 5",
        "down 5",
        "forward 8",
        "up 3",
        "down 8",
        "forward 2",
    ]
    expected_value_p1 = 150
    expected_value_p2 = 900
    p1 = Position()
    p2 = Position()
    for step in test_case:
        p1.move(*step.split())
        p2.move_with_aim(*step.split())
    assert p1.x * p1.y == expected_value_p1, p1
    assert p2.x * p2.y == expected_value_p2, p2

    # Part 1 & 2
    t = time.perf_counter()
    p1 = Position()
    p2 = Position()
    with open("data.txt", "r") as f:
        for line in f.readlines():
            step = line.strip().split()
            p1.move(*step)
            p2.move_with_aim(*step)

    print(f"Part 1: {p1} X*Y: {p1.x * p1.y}")
    print(f"Part 2: {p2} X*Y: {p2.x * p2.y} (t: {1000*(time.perf_counter() - t):.3f} ms)")
