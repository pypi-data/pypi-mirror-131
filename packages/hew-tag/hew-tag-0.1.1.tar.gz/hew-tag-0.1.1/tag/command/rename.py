from . import arguments
from . import options
from .. import util
import click

@click.command('rename')
@options.verbose()
@options.debug()
@arguments.old_tag()
@arguments.new_tag()
@arguments.files()
def rename_command(verbose, debug, old_tag, new_tag, files):
    '''Rename a tag on files.

    \b
    OLD_TAG current tag name
    NEW_TAG new tag name
    FILES list of files

    \b
    Examples:
      - tag rename my-tag my-new-tag myfile{my-tag}.txt
      - tag rename my-tag my-new-tag *.txt
    '''
    def tag_handler(tag_set):
        if old_tag in tag_set:
            tag_set.remove(old_tag)
            tag_set.add(new_tag)
    util.rename_files(verbose, debug, files, tag_handler)
