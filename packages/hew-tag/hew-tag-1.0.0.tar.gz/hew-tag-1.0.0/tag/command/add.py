from . import arguments
from . import options
from .. import util
import click

@click.command('add')
@options.verbose()
@options.debug()
@arguments.tags()
@arguments.files()
def add_command(verbose, debug, tags, files):
    '''Add tags to files.

    \b
    TAGS  comma seperated list of tags
    FILES list of files

    \b
    Examples:
      - tag add my-tag myfile.txt
      - tag add my-tag-1,my-tag-2 *.txt
    '''
    tag_list = tags.split(',')
    util.rename_files(verbose, debug, files, lambda tag_set: tag_set.update(tag_list))
