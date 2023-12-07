from typing import List, Dict

START_KEY = 'seed'
END_KEY = 'location'


def solve(input_text: str) -> Dict[str, any]:
    lines = input_text.splitlines()
    seeds = lines[0][7:].split()
    maps: Dict[str, Dict[str, Dict[int, int]]] = {}

    # FIXME while probably technically correct, building the full map like this isn't performant and doesn't finish in
    #  time. We need to use a custom data structure that checks the range instead
    i = 1
    while i < len(lines):
        # skip blank lines
        if not lines[i]:
            i += 1
            continue

        # get line up until " map:"
        map_name = lines[i][:-5].split('-to-')
        source = map_name[0]
        dest = map_name[1]
        i += 1
        while i < len(lines) and lines[i]:
            dest_source_range = lines[i].split()

            for j in range(0, int(dest_source_range[2])):
                if not maps.get(source):
                    maps[source] = {}
                if not maps[source].get(dest):
                    maps[source][dest] = {}
                maps[source][dest][int(dest_source_range[1]) + j] = int(dest_source_range[0]) + j

            i += 1

    end_to_start = {}
    for seed in seeds:
        key = START_KEY
        value = int(seed)
        while key != END_KEY:
            # TODO this assumes only one child key - i.e. a tree where only the parents of leaf nodes can have
            #  more than one child
            subkey = next(iter(maps[key].keys()))
            value = maps[key][subkey].get(value, value)
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
