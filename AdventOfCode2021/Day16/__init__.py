import time
from functools import reduce
from typing import Tuple


class Packet:
    def __init__(self, hex_str: str = None, bits: str = None):
        self.hex_str = hex_str
        self.bitarray: str = bits if bits else bin(int(hex_str, 16))[2:].zfill(len(hex_str) * 4)
        self.version = int(self.bitarray[:3], 2)
        self.id = int(self.bitarray[3:6], 2)
        self.subpackets = []
        if self.id == 4:
            self.content, i = self._get_literal_value(self.bitarray[6:])
            self.length = 6 + i
        else:
            self.content = None
            _lid = 15 if self.bitarray[6] == "0" else 11
            _sp = _lid + 3 + 3 + 1
            self.data_length = int(self.bitarray[7:7 + _lid], 2)
            read_count = 0
            read_length = 0
            while (_lid == 11 and read_count < self.data_length) or (_lid == 15 and read_length < self.data_length):
                _bits = self.bitarray[_sp + read_length:]
                new_packet = Packet(bits=_bits)
                self.subpackets.append(new_packet)
                read_length += new_packet.length
                read_count += 1
            self.length = _sp + read_length

    @staticmethod
    def _get_literal_value(bits: str) -> Tuple[int, int]:
        value_str = ""
        i = 0
        while True:
            value_str += bits[i + 1:i + 5]
            if bits[i] == "0":
                break
            i += 5
        return int(value_str, 2), i + 5

    def __repr__(self):
        elements = [f"v:{self.version}", f"id:{self.id}", f"len:{self.length}"]
        if self.content:
            elements.append(f"content: {self.content}")
        if self.subpackets:
            elements.append(f"subpackets: {self.subpackets}")
        return f"Packet({', '.join(elements)})"

    def get_value(self):
        # Literal Value
        if self.id == 4:
            return self.content
        # Agg Modes
        _sub_values = (s.get_value() for s in self.subpackets)
        # Sum
        if self.id == 0:
            return sum(_sub_values)
        # Product
        if self.id == 1:
            return reduce(lambda x, y: x * y, _sub_values)
        # Min
        if self.id == 2:
            return min(_sub_values)
        # Max
        if self.id == 3:
            return max(_sub_values)
        # For next three modes it can be assumed there are exactly two subpackets
        a, b = self.subpackets[0].get_value(), self.subpackets[1].get_value()
        # Greater
        if self.id == 5:
            return 1 if a > b else 0
        # Less
        if self.id == 6:
            return 1 if a < b else 0
        # Equal
        if self.id == 7:
            return 1 if a == b else 0


def sum_versions(packet: Packet) -> int:
    sv = 0
    sv += packet.version
    for sub_packet in packet.subpackets:
        sv += sum_versions(sub_packet)
    return sv


if __name__ == '__main__':

    # Test 1
    test_cases = (
        ("8A004A801A8002F478", 16),
        ("620080001611562C8802118E34", 12),
        ("C0015000016115A2E0802F182340", 23),
        ("A0016C880162017C3686B18A3D4780", 31),
    )
    for test_data, expected_sum in test_cases:
        test_packet = Packet(hex_str=test_data)
        test_result = sum_versions(test_packet)
        assert test_result == expected_sum, test_result

    # Test 2
    test_cases = (
        ("C200B40A82", 3),
        ("04005AC33890", 54),
        ("880086C3E88112", 7),
        ("CE00C43D881120", 9),
        ("D8005AC2A8F0", 1),
        ("F600BC2D8F", 0),
        ("9C005AC2F8F0", 0),
        ("9C0141080250320F1802104A08", 1),
    )
    for test_data, expected_value in test_cases:
        assert Packet(hex_str=test_data).get_value() == expected_value

    with open("data.txt") as f:
        data = f.readline().strip()
    # Part 1
    t = time.perf_counter()
    result_p1 = sum_versions(Packet(hex_str=data))
    print(f"Part1: {result_p1:>12} (t: {1000 * (time.perf_counter() - t):.3f} ms)")

    # Part 2
    t = time.perf_counter()
    result_p2 = Packet(hex_str=data).get_value()
    print(f"Part2: {result_p2:>12} (t: {1000 * (time.perf_counter() - t):.3f} ms)")
