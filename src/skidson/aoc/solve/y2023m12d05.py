import logging
import sys
from typing import List, Dict, Optional

log_handler = logging.StreamHandler(sys.stdout)
log_handler.setFormatter(logging.Formatter("[%(asctime)s[(%(levelname)s] %(name)s: %(message)s"))
log = logging.getLogger(__name__)
log.addHandler(log_handler)
log.setLevel(logging.DEBUG)

START_KEY = 'seed'
END_KEY = 'location'


class KeyRange:
    def __init__(self, start: int, end: int):
        """
        A numerical range.
        :param start: the start of the range, inclusive
        :param end:  the end of the range, exclusive
        """
        self.start = start
        self.end = end

    def __str__(self):
        return f'{{start: {self.start}, end: {self.end}, (length: {self.end - self.start})}}'

    def __repr__(self):
        return self.__str__()


class Result:
    def __init__(self, match: Optional[KeyRange], leftover: List[KeyRange]):
        self.match = match
        self.leftover = leftover


class AlmanacRange(KeyRange):
    def __init__(self, source_start: int, dest_start: int, length: int):
        super().__init__(source_start, source_start + length)
        self.offset = dest_start - source_start

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

    def __str__(self):
        return f'{{start: {self.start}, end: {self.end}, offset: {self.offset}}}'


def solve(input_text: str) -> int:
    lines = input_text.splitlines()
    maps: Dict[str, Dict[str, List[AlmanacRange]]] = build_maps(lines)

    log.info('Finding closest location...')
    seeds = lines[0][7:].split()
    return find_lowest_location(seeds, maps)


def build_maps(lines: List[str]) -> Dict[str, Dict[str, List[AlmanacRange]]]:
    maps: Dict[str, Dict[str, List[AlmanacRange]]] = {}

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
            if not maps.get(source):
                maps[source] = {}
            if not maps[source].get(dest):
                maps[source][dest] = []

            maps[source][dest].append(build_range(lines[i]))
            i += 1

    return maps


def build_range(line: str) -> AlmanacRange:
    dest_source_range = line.split()
    return AlmanacRange(int(dest_source_range[1]), int(dest_source_range[0]), int(dest_source_range[2]))


def find_lowest_location(seeds: List[str], maps: Dict[str, Dict[str, List[AlmanacRange]]]) -> int:
    location_ranges = []
    for i in range(0, len(seeds), 2):
        start = int(seeds[i])
        seed_range = KeyRange(start, start + int(seeds[i+1]))
        search_ranges = [seed_range]
        key = START_KEY
        while key != END_KEY:
            # TODO this assumes only one child key - i.e. a tree where only the parents of leaf nodes can have
            #  more than one child
            subkey = next(iter(maps[key].keys()))
            matches = []
            for r in maps[key][subkey]:
                for key_range in search_ranges:
                    result = r.match(key_range)
                    if result.match is None:
                        continue

                    matches.append(result.match)
                    search_ranges.remove(key_range)
                    search_ranges += result.leftover

            search_ranges += matches
            key = subkey
        location_ranges += search_ranges
        log.debug(f'Mapped seed range {seed_range} to locations {search_ranges}')

    min_location = None
    for key_range in location_ranges:
        if min_location is None or key_range.start < min_location:
            min_location = key_range.start

    return min_location
