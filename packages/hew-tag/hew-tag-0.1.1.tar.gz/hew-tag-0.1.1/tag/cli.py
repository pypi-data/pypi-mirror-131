from .command import options
from .command.add import add_command
from .command.clear import clear_command
from .command.find import find_command
from .command.index import index_command
from .command.list import list_command
from .command.remove import remove_command
from .command.rename import rename_command
from .command.set import set_command
from .command.sort import sort_command
from .command.version import version_command, show_version
import click

@click.group(invoke_without_command=True)
@options.version()
@click.pass_context
def cli(ctx, version):
    '''tag - manage file name tags

    \b
    File tags:
      - are in the file name matching: {[a-zA-Z0-9-]+}
      - start with '{' and end with '}'
      - consist of letters, numbers and the '-' character

    \b
    Examples:
      - myfile{my-tag-1}{my-tag-2}.txt
      - My Title Case File {My-Tag-1}{My-Tag-2}.txt
    '''
    if version:
        show_version()
    elif ctx.invoked_subcommand is None:
        click.echo(ctx.get_help())

cli.add_command(add_command)
cli.add_command(clear_command)
cli.add_command(find_command)
cli.add_command(index_command)
cli.add_command(list_command)
cli.add_command(remove_command)
cli.add_command(rename_command)
cli.add_command(set_command)
cli.add_command(sort_command)
cli.add_command(version_command)
