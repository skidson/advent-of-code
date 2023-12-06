from typing import List, Dict

BLANK = '.'
GEAR = '*'


def solve(input_text: str) -> Dict[str, int]:
    schematic: List[List[str]] = []
    for row_index, line in enumerate(input_text.splitlines()):
        schematic.append([])
        for char in line:
            schematic[row_index].append(char)

    part_numbers = []
    gear_ratios = []
    for y, row in enumerate(schematic):
        for x, char in enumerate(row):
            nearby_parts = []
            if is_symbol(char):
                nearby_parts = find_part_numbers(schematic, x, y)
            part_numbers = part_numbers + nearby_parts

            if char == GEAR and len(nearby_parts) == 2:
                gear_ratios.append(nearby_parts[0] * nearby_parts[1])

    return {
        'part_numbers_sum': sum(part_numbers),
        'gear_ratios_sum': sum(gear_ratios)
    }


def is_symbol(char: str):
    return not char.isnumeric() and char != BLANK


def find_part_numbers(schematic: List[List[str]], x: int, y: int) -> List[int]:
    part_numbers = []

    # check surrounding squares
    # TODO this could be more efficient and stateless by processing an entire row fully, however,
    #  not mutating the schematic could cause the same part number to be found twice
    for i in range(-1, 2):
        for j in range(-1, 2):
            x_index = x + i
            y_index = y + j
            num_buffer = ''
            # if in a number, move to the leftmost digit
            while 1 <= x_index < len(schematic[y]) and schematic[y_index][x_index].isnumeric():
                if schematic[y_index][x_index - 1].isnumeric():
                    x_index = x_index - 1
                else:
                    break

            # grab the digit, delete it, and keep moving right
            while x_index < len(schematic[y]) and schematic[y_index][x_index].isnumeric():
                num_buffer = num_buffer + schematic[y_index][x_index]
                schematic[y_index][x_index] = BLANK
                x_index = x_index + 1

            if num_buffer:
                part_numbers.append(int(num_buffer))

    return part_numbers
