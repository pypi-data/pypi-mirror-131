import click

def files():
    return click.argument('files', nargs=-1, type=click.Path(exists=True))

def new_tag():
    return click.argument('new_tag')

def old_tag():
    return click.argument('old_tag')

def output():
    return click.argument('output')

def path(default='.'):
    return click.argument('path', default=default, type=click.Path(exists=True))

def tag():
    return click.argument('tag')

def tags():
    return click.argument('tags')
