from . import arguments
from . import options
from .. import util
import click

@click.command('set')
@options.verbose()
@options.debug()
@arguments.tags()
@arguments.files()
def set_command(verbose, debug, tags, files):
    '''Set tags on files.

    Add and remove tags to ensure each file has the supplied tags and only the supplied tags.

    \b
    TAGS  comma seperated list of tags
    FILES list of files

    \b
    Examples:
      - tag set my-tag myfile{my-tag}.txt
      - tag set my-tag-1,my-tag-2 *.txt
    '''
    tag_list = tags.split(',')
    def tag_handler(tag_set):
        tag_set.clear()
        tag_set.update(tag_list)
    util.rename_files(verbose, debug, files, tag_handler)
