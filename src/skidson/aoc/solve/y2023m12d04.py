from typing import List, Dict


def solve(input_text: str) -> Dict[str, int]:
    score = 0
    copies: Dict[int, int] = {}

    lines = input_text.splitlines()
    for index, line in enumerate(lines):
        card = line.split(':')
        card_numbers = card[1].split('|')
        winning_numbers = set(card_numbers[0].split())
        my_numbers = card_numbers[1].split()

        # score = 2^(matches-1)
        matches = 0
        for number in my_numbers:
            if number in winning_numbers:
                matches += 1

        if matches > 0:
            this_copies = copies.get(index, 0) + 1
            score = score + ((2 ** (matches - 1)) * this_copies)
            for i in range(1, matches + 1):
                i_copies = copies.get(index + i, 0) + this_copies
                copies[index + i] = i_copies

    count = len(lines)
    for value in copies.values():
        count += value

    return {
        'score': score,
        'count': count
    }
