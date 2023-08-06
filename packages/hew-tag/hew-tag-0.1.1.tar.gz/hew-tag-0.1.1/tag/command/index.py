from . import arguments
from . import options
from .. import util
import click
import os

@click.command('index')
@options.all()
@options.debug()
@options.recursive()
@options.tree(help = 'Create index with nested tag tree.')
@options.verbose()
@arguments.path(default = None)
@arguments.output()
def index_command(all, debug, recursive, tree, verbose, path, output):
    '''Index tagged files.

    \b
    PATH   path to search
    OUTPUT path to new index

    \b
    Examples:
      - tag index my-files my-index
      - tag index -r my-files my-index
    '''
    abspath = os.path.abspath(path)

    if os.path.exists(output) and os.listdir(output):
        raise click.ClickException(\
            f'Index directory "{output}" exists with content. '\
            + f'Delete "{output}" or choose a different path.')

    file_list = []
    def handle_file(file):
        if len(file.tags) > 0:
            file_list.append(file)
    util.find_files(abspath, recursive, all, handle_file)

    index = {}
    for file in file_list:
        for perm in permute(sorted(file.tags), tree):
            filename = os.path.split(file.original)[1]
            path = os.path.join(output, *perm, filename)
            if path not in index:
                index[path] = []
            index[path].append(file)

    count = 0
    for key in sorted(index.keys()):
        index_len = len(index[key])
        count += index_len
        parent = os.path.split(key)[0]
        if not debug:
            os.makedirs(parent, exist_ok=True)
        if index_len == 1:
            file = index[key][0]
            src = file.original
            dst = os.path.join(parent, file.filename)
            if verbose:
                click.echo(f"{dst} -> {src}")
            if not debug:
                os.symlink(src, dst)
        else:
            for file in index[key]:
                path = file.dir[len(abspath)+1:]
                filename = file.filename
                if path:
                    split = path.split(os.sep)
                    id = '-'.join(split)
                    base, ext = os.path.splitext(filename)
                    filename = f"{base}-{id}{ext}"
                src = file.original
                dst = os.path.join(parent, filename)
                if verbose:
                    click.echo(f"{dst} -> {src}")
                if not debug:
                    os.symlink(src, dst)
    if verbose and count > 0:
        message = 'to index' if debug else 'indexed'
        click.echo()
        click.echo(f"{count} files {message}.")

def permute(items, tree):
    if tree:
        return _permute([], items)
    return map(lambda item: [item], items)

def _permute(prefix, suffix):
    result = [prefix] if prefix else []
    if not suffix:
        return result
    for index, item in enumerate(suffix):
        child_prefix = prefix.copy()
        child_prefix.append(item)
        child_suffix = suffix.copy()
        del child_suffix[index]
        result = result + _permute(child_prefix, child_suffix)
    return result
