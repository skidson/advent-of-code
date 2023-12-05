from typing import Dict, List


COLOUR_THRESHOLDS: Dict[str, int] = {'red': 12, 'green': 13, 'blue': 14}


class Game:
    def __init__(self, index: int):
        self.index = index
        self.max_colours = {}
        for colour in COLOUR_THRESHOLDS:
            self.max_colours[colour] = 0


def solve(input_text: str) -> (int, int):
    game_index_sum = 0
    game_power_sum = 0
    for line in input_text.splitlines():
        game_line = line.split(': ')
        game = Game(int(game_line[0][5:]))
        draws = game_line[1].split('; ')
        for draw in draws:
            colour_text = draw.split(', ')
            for group in colour_text:
                group_text = group.split(' ')
                count = int(group_text[0])
                colour = group_text[1]
                if game.max_colours.get(colour) is None or game.max_colours.get(colour) < count:
                    game.max_colours[colour] = count

        if is_valid(game):
            game_index_sum = game_index_sum + game.index

        power = 1 if game.max_colours else 0
        for colour in game.max_colours:
            power = power * game.max_colours[colour]
        game_power_sum = game_power_sum + power

    return game_index_sum, game_power_sum


def is_valid(game: Game) -> bool:
    for colour in COLOUR_THRESHOLDS:
        if game.max_colours.get(colour) > COLOUR_THRESHOLDS[colour]:
            return False
    return True
