from skidson.aoc.solve.y2023m12d05 import build_range, AlmanacRange, KeyRange


def test_build_range():
    assert_range(build_range('0 69 1'), 69, 70, -69)
    assert_range(build_range('49 53 8'), 53, 61, -4)
    assert_range(build_range('81 45 19'), 45, 64, 36)


def test_match_before():
    a = KeyRange(0, 5)
    b = AlmanacRange(5, 5, 5)
    result = b.match(a)
    assert result.match is None
    assert result.leftover == [a]


def test_match_after():
    a = KeyRange(10, 11)
    b = AlmanacRange(5, 5, 5)
    result = b.match(a)
    assert result.match is None
    assert result.leftover == [a]


def test_match_inside_left():
    a = KeyRange(0, 1)
    b = AlmanacRange(0, 0, 10)
    result = b.match(a)
    assert result.match.start == 0 and result.match.end == 1
    assert not result.leftover


def test_match_inside_right():
    a = KeyRange(9, 10)
    b = AlmanacRange(0, 0, 10)
    result = b.match(a)
    assert result.match.start == 9 and result.match.end == 10
    assert not result.leftover


def test_match_over_left_edge():
    a = KeyRange(0, 5)
    b = AlmanacRange(2, 2, 10)
    result = b.match(a)
    assert result.match.start == 2 and result.match.end == 5
    assert len(result.leftover) == 1
    assert result.leftover[0].start == 0 and result.leftover[0].end == 2


def test_match_over_right_edge():
    a = KeyRange(8, 15)
    b = AlmanacRange(0, 0, 10)
    result = b.match(a)
    assert result.match.start == 8 and result.match.end == 10
    assert len(result.leftover) == 1
    assert result.leftover[0].start == 10 and result.leftover[0].end == 15


def test_match_full():
    a = KeyRange(0, 10)
    b = AlmanacRange(3, 3, 5)
    result = b.match(a)
    assert result.match.start == 3 and result.match.end == 8
    assert len(result.leftover) == 2
    assert result.leftover[0].start == 0 and result.leftover[0].end == 3
    assert result.leftover[1].start == 8 and result.leftover[1].end == 10


# region Helpers
def assert_range(r: AlmanacRange, start: int, end: int, offset: int):
    assert r.start == start
    assert r.end == end
    assert r.offset == offset
# endregion