import logging
import sys
from dataclasses import dataclass
from typing import List, Dict, Optional

log_handler = logging.StreamHandler(sys.stdout)
log_handler.setFormatter(logging.Formatter("[%(asctime)s[(%(levelname)s] %(name)s: %(message)s"))
log = logging.getLogger(__name__)
log.addHandler(log_handler)
log.setLevel(logging.DEBUG)

DEFAULT_START_KEY = 'seed'
DEFAULT_END_KEY = 'location'


@dataclass(repr=True)
class KeyRange:
    start: int
    end: int


@dataclass
class Result:
    match: Optional[KeyRange]
    leftover: List[KeyRange]


@dataclass(repr=True)
class AlmanacRange(KeyRange):
    offset: int

    @staticmethod
    def from_line(line: str) -> 'AlmanacRange':
        dest_source_range = line.split()
        source_start = int(dest_source_range[1])
        dest_start = int(dest_source_range[0])
        length = int(dest_source_range[2])
        return AlmanacRange(source_start, source_start + length, dest_start - source_start)

    def match(self, key_range: KeyRange) -> Result:
        if key_range.end <= self.start or key_range.start >= self.end:
            return Result(None, [key_range])
        match_start = max(key_range.start, self.start)
        match_end = min(key_range.end, self.end)
        match = KeyRange(match_start + self.offset, match_end + self.offset)

        leftover = []
        if match_start > key_range.start:
            leftover.append(KeyRange(key_range.start, match_start))
        if match_end < key_range.end:
            leftover.append(KeyRange(match_end, key_range.end))

        return Result(match, leftover)

    def reverse(self) -> 'AlmanacRange':
        return AlmanacRange(self.start + self.offset, self.end + self.offset, -1 * self.offset)


class Almanac:
    def __init__(self):
        self.data = {}
        self.order = []

    def put(self, source: str, dest: str, key_range: AlmanacRange, linked: bool = False):
        if not self.data.get(source):
            self.data[source] = {}
            self.order.append(source)
        if not self.data[source].get(dest):
            self.data[source][dest] = []
        self.data[source][dest].append(key_range)

        if linked:
            self.put(dest, source, key_range.reverse())

    def get(self, source: str, dest: str) -> List[AlmanacRange]:
        return self.data[source][dest]

    def get_map(self, source: str) -> Dict[str, List[AlmanacRange]]:
        return self.data[source]

    def get_default_dest(self, source: str):
        """
        Returns the first key (by insertion order). Only important if Almanac is doubly-linked
        :param source:
        :return:
        """
        return next(iter(self.data[source].keys()))


def solve(input_text: str) -> int:
    lines = input_text.splitlines()

    seeds = lines[0][7:].split()
    return traverse(seeds, build_almanac(lines))


def build_almanac(lines: List[str], link: bool = False) -> Almanac:
    almanac = Almanac()

    i = 1
    while i < len(lines):
        # skip blank lines
        if not lines[i]:
            i += 1
            continue

        # get line up until " map:"
        log.info(f'Parsing {lines[i][:-1]}...')
        map_name = lines[i][:-5].split('-to-')
        source = map_name[0]
        dest = map_name[1]
        i += 1
        while i < len(lines) and lines[i]:
            log.debug(f'Parsing range {lines[i]}...')
            almanac.put(source, dest, AlmanacRange.from_line(lines[i]), link)
            i += 1

    return almanac


def traverse(
        seeds: List[any], almanac: Almanac, start_key: str = DEFAULT_START_KEY, end_key: str = DEFAULT_END_KEY
) -> int:
    log.info(f'Traversing almanac from {start_key} to {end_key}...')
    end_ranges = []
    for i in range(0, len(seeds), 2):
        start = int(seeds[i])
        seed_range = KeyRange(start, start + int(seeds[i + 1]))
        search_ranges = [seed_range]

        order = almanac.order.copy()
        if end_key not in order:
            order.append(end_key)
        if order.index(start_key) > order.index(end_key):
            order.reverse()

        key = start_key
        while key != end_key:
            subkey = order[order.index(key) + 1]
            matches = []
            for entry in almanac.get(key, subkey):
                for search_range in search_ranges:
                    result = entry.match(search_range)
                    if result.match is None:
                        continue

                    log.debug(f"{key} {search_range} {'+' if entry.offset >= 0 else ''}{entry.offset}"
                              f" -> {subkey} {result.match}")
                    matches.append(result.match)
                    search_ranges.remove(search_range)
                    search_ranges += result.leftover

            search_ranges += matches
            key = subkey
        end_ranges += search_ranges
        log.debug(f'Mapped {start_key} range {seed_range} to {end_key} range {search_ranges}')

    min_location = None
    for search_range in end_ranges:
        if min_location is None or search_range.start < min_location:
            min_location = search_range.start

    return min_location
