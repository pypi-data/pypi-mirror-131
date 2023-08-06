from . import arguments
from . import options
from .. import util
import click

@click.command('clear')
@options.verbose()
@options.debug()
@arguments.files()
def clear_command(verbose, debug, files):
    '''Clear tags from files.

    \b
    FILES list of files

    \b
    Examples:
      - tag clear myfile{my-tag}.txt
      - tag clear *.txt
    '''
    util.rename_files(verbose, debug, files, lambda tag_set: tag_set.clear())
