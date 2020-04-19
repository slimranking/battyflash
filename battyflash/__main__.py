import os

import click

from battyflash.utils import store_json, load_json
from battyflash.packs import query_entry, add_entry, flash_from_data

@click.group()
def cli():
    pass


@cli.command(name="build-flashpack")
@click.argument('flashpack', default=None, required=False)
@click.argument('directory', default='/Users/tom/.battyflash/data', required=False)
def cmd_build_flashpack(flashpack, directory):
    build_flashpack(flashpack=flashpack, directory=directory)


@cli.command(name="flashpack-quiz")
@click.argument('flashpack', default=None, required=False)
@click.argument('directory', default='/Users/tom/.battyflash/data', required=False)
@click.argument('tags', nargs=-1, default=None, required=False)
def cmd_flashpack_quiz(flashpack, directory, tags):
    flashpack_quiz(flashpack=flashpack, directory=directory, tags=tags)


def build_flashpack(flashpack, directory):
    """
    Add entries to <flashpack> in <dir>
    """
    if not flashpack:
        flashpack = input('Which Flashpack would you like to use?\n')

    flashdir = os.path.join(directory, flashpack)
    
    data = load_json(flashdir)
    
    if not data:
        print('Flashpack does not exist, creating new Flashpack')

    # TODO: Better word than "entry"
    print('Lets begin by adding an entry')

    while True:
        name, entry = query_entry(flashpack)
        if not name:
            break
        add_entry(data, name, entry)

    print('Thanks! storing new data...\n')
    store_json(data, flashdir)


def flashpack_quiz(flashpack, directory, tags):
    """
    Randomly quiz from <flashpack> in <directory>.

    tags: list
        Filter by these tag, e.g. verb, noun
    """
    if not flashpack:
        flashpack = input('Which Flashpack would you like to use?\n')
    
    flashdir = os.path.join(directory, flashpack)

    data = load_json(flashdir)

    print('\n\nFor each item, respond with the flash, to exit, return nothing\n')
    flash_from_data(data, tags)
    
    print('Nice quizzing! Storing results...\n')

    store_json(data, flashdir)


if __name__ == '__main__':
    cli()
