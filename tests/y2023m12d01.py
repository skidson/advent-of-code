import pytest
from skidson.aoc.solve.y2023m12d01 import val_from_word


def test_val_from_word():
    assert val_from_word("one", 0) == 1
    assert val_from_word("two", 0) == 2
    assert val_from_word("three", 0) == 3
    assert val_from_word("four", 0) == 4
    assert val_from_word("five", 0) == 5
    assert val_from_word("six", 0) == 6
    assert val_from_word("seven", 0) == 7
    assert val_from_word("eight", 0) == 8
    assert val_from_word("nine", 0) == 9


def test_val_from_word_extra():
    assert val_from_word("tone", 0) == 1
    assert val_from_word("two3", 0) == 2
    assert val_from_word("4three", 0) == 4
    assert val_from_word("four5", 0) == 4
    assert val_from_word("fi6ve", 0) is None
