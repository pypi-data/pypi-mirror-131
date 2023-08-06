from . import File
import click
import os

def rename_files(verbose, debug, files, tag_handler):
    count = 0
    for src in files:
        file = File(src)
        tag_handler(file.tags)
        dst = file.relative_path
        if src == dst:
            continue
        count += 1
        if verbose:
            click.echo(f"{src} -> {dst}")
        if not debug:
            os.rename(src, dst)
    if verbose and count > 0:
        message = 'to rename' if debug else 'renamed'
        files = 'file' if count == 1 else 'files'
        click.echo()
        click.echo(f"{count} {files} {message}.")
