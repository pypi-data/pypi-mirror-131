from . import arguments
from . import options
from .. import util
import click

@click.command('sort')
@options.verbose()
@options.debug()
@arguments.files()
def sort_command(verbose, debug, files):
    '''Sort tags on files.

    \b
    FILES list of files

    \b
    Examples:
      - tag sort myfile{my-tag-2}{my-tag-1}.txt
      - tag sort *.txt
    '''
    util.rename_files(verbose, debug, files, lambda tag_set: tag_set)
