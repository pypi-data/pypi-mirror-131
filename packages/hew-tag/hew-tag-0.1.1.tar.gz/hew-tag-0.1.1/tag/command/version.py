import click
import tag

@click.command('version')
def version_command():
    '''Show version information.

    \b
    Examples:
      - tag version
    '''
    show_version()

def show_version():
    click.echo(f'''tag {tag.__version__}
License {tag.__license__}: {tag.__license_long__}
This is free software: you are free to change and redistribute it.
There is NO WARRANTY, to the extent permitted by law.

Written by {tag.__author__}.''')

