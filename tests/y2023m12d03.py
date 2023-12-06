import pytest
from skidson.aoc.solve.y2023m12d03 import is_symbol, find_part_numbers


def test_is_symbol():
    assert not is_symbol('.')
    assert is_symbol('$')
    assert is_symbol('#')
    assert not is_symbol('4')


def test_find_part_numbers():
    schematic = [
        ['1', '2', '3'],
        ['.', '$', '4'],
        ['#', '5', '6']
    ]
    assert set(find_part_numbers(schematic, 1, 1)) == {123, 4, 56}
