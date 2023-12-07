import sys
from typing import List, Dict, Optional
import logging

log_handler = logging.StreamHandler(sys.stdout)
log_handler.setFormatter(logging.Formatter("[%(asctime)s] %(name)s:%(levelname)s - %(message)s"))
log = logging.getLogger(__name__)
log.addHandler(log_handler)
log.setLevel(logging.INFO)

START_KEY = 'seed'
END_KEY = 'location'


class Range:
    def __init__(self, source_start: int, dest_start: int, length: int):
        self.source_start = source_start
        self.dest_start = dest_start
        self.length = length

    def find(self, key: int) -> Optional[int]:
        if key < self.source_start or key >= self.source_start + self.length:
            return None
        return self.dest_start + (key - self.source_start)

def solve(input_text: str) -> Dict[str, any]:
    lines = input_text.splitlines()
    seeds = lines[0][7:].split()
    maps: Dict[str, Dict[str, List[Range]]] = {}

    # FIXME while probably technically correct, building the full map like this isn't performant and doesn't finish in
    #  time. We need to use a custom data structure that checks the range instead
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
            dest_source_range = lines[i].split()

            if not maps.get(source):
                maps[source] = {}
            if not maps[source].get(dest):
                maps[source][dest] = []

            maps[source][dest].append(
                Range(int(dest_source_range[1]), int(dest_source_range[0]), int(dest_source_range[2]))
            )

            i += 1

    log.info('Find closest location...')
    end_to_start = {}
    for seed in seeds:
        key = START_KEY
        value = int(seed)
        while key != END_KEY:
            # TODO this assumes only one child key - i.e. a tree where only the parents of leaf nodes can have
            #  more than one child
            subkey = next(iter(maps[key].keys()))
            match = None
            for r in maps[key][subkey]:
                match = r.find(value)
                if match is not None:
                    break

            if match is not None:
                value = match
            key = subkey
        end_to_start[value] = seed

    min_end = None
    for end in end_to_start.keys():
        if min_end is None or end < min_end:
            min_end = end

    return {
        'seed': end_to_start[min_end],
        'location': min_end
    }
