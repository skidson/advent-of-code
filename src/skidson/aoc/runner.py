import datetime
import importlib
import logging
import sys

import click
from importlib_resources import files

INPUT_FILE = 'input.txt'
log = logging.getLogger(__name__)


@click.command()
@click.argument('date', type=click.DateTime(formats=['%Y-%m-%d']))
@click.option('--filename', default=INPUT_FILE)
def run(date: datetime.date, filename: str):
    input_text = files(f"skidson.aoc.resources.{date.strftime('%Y.%m.%d')}").joinpath(filename).read_text()

    module = importlib.import_module(f"skidson.aoc.solve.{date.strftime('y%Ym%md%d')}")
    print(module.solve(input_text))
    pass


if __name__ == '__main__':
    run(sys.argv[1:])
    sys.exit(0)
