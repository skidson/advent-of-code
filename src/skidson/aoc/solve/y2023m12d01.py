from typing import Dict, Optional

WORD_NUMBERS: Dict[str, int] = {
    'one': 1,
    'two': 2,
    'three': 3,
    'four': 4,
    'five': 5,
    'six': 6,
    'seven': 7,
    'eight': 8,
    'nine': 9
}

min_word_length = None
max_word_length = None
for word in WORD_NUMBERS:
    word_length = len(word)
    if min_word_length is None or word_length < min_word_length:
        min_word_length = word_length
    if max_word_length is None or word_length > max_word_length:
        max_word_length = word_length


def solve(input_text: str) -> int:
    calibration_sum = 0
    line: str
    for line in input_text.splitlines():
        calibration_sum = calibration_sum + process_line(line)
    return calibration_sum


def process_line(line: str) -> int:
    start = 0
    end = len(line) - 1

    first_digit = None
    last_digit = None
    while start <= end and (first_digit is None or last_digit is None):
        first_char = line[start]
        if first_digit is None and first_char.isnumeric():
            first_digit = first_char

        if first_digit is None:
            first_digit = val_from_word(line, start)

        if first_digit is None:
            start = start + 1

        last_char = line[end]
        if last_digit is None and last_char.isnumeric():
            last_digit = last_char

        if last_digit is None:
            last_digit = val_from_word(line, end)

        if last_digit is None:
            end = end - 1

    if first_digit is None or last_digit is None:
        raise ValueError(f'Line {line} contains no digits')

    return int(f'{first_digit}{last_digit}')


def val_from_word(line: str, index: int) -> Optional[int]:
    val = None
    for i in range(min_word_length, max_word_length + 1):
        end_index = index + i
        if end_index > len(line):
            break
        val = WORD_NUMBERS.get(line[index:end_index])
        if val is not None:
            return val
    return val
