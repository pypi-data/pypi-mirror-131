from . import arguments
from . import options
from .. import util
import click

@click.command('list')
@options.all()
@options.count()
@options.null()
@options.recursive()
@arguments.path()
def list_command(all, count, null, recursive, path):
    '''List tags on files.

    \b
    PATH path to search (default .)

    \b
    Examples:
      - tag list -r path/to/files/
      - tag list
    '''
    tags = {}
    def handle_file(file):
        for tag in file.tags:
            tags[tag] = 1 if not tag in tags else tags[tag] + 1
    util.find_files(path, recursive, all, handle_file)

    output = []
    for tag in sorted(tags.keys()):
        if count:
            output.append(f"{tag}: {tags[tag]}")
        else:
            output.append(tag)
    delimiter = '\0' if null else '\n'
    click.echo(delimiter.join(output), nl = not null)
