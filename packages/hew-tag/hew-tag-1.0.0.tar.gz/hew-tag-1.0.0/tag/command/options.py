import click

def all():
    return click.option('--all', '-a', default=False, is_flag=True, help='Include hidden files.')

def count():
    return click.option('--count', '-c', default=False, is_flag=True, help='Show count of matches.')

def debug():
    return click.option('--debug', '-d', default=False, is_flag=True, help='Make no changes to the file system.')

def null():
    return click.option('--null', '-0', default=False, is_flag=True, help='End output lines with NULL (\\0) instead of newline.')

def recursive():
    return click.option('--recursive', '-r', default=False, is_flag=True, help='Include subdirectories recursively.')

def tree(help = 'Show output as tree.'):
    return click.option('--tree', '-t', default=False, is_flag=True, help=help)

def verbose():
    return click.option('--verbose', '-v', default=False, is_flag=True, help='Show additional output.')

def version():
    return click.option('--version', default=False, is_flag=True, help='Show version information.')
