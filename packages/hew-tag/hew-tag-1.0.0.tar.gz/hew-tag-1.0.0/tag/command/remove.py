from . import arguments
from . import options
from .. import util
import click

@click.command('remove')
@options.verbose()
@options.debug()
@arguments.tags()
@arguments.files()
def remove_command(verbose, debug, tags, files):
    '''Remove tags from files.

    \b
    TAGS  comma seperated list of tags
    FILES list of files

    \b
    Examples:
      - tag remove my-tag myfile{my-tag}.txt
      - tag remove my-tag-1,my-tag-2 *.txt
    '''
    tag_list = tags.split(',')
    util.rename_files(verbose, debug, files, lambda tag_set: tag_set.difference_update(tag_list))
