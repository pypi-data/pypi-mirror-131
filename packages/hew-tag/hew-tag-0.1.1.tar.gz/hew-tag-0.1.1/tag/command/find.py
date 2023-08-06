from . import arguments
from . import options
from .. import util
import click
import os

@click.command('find')
@options.all()
@options.null()
@options.recursive()
@options.tree()
@arguments.tag()
@arguments.path()
def find_command(all, null, recursive, tree, tag, path):
    '''Find files by tag.

    \b
    TAG  tag to find
    PATH path to search (default .)

    \b
    Examples:
      - tag find -r my-tag path/to/files/
      - tag find my-tag
    '''
    file_list = []
    def handle_file(file):
        if tag in file.tags:
            file_list.append(file)
    util.find_files(path, recursive, all, handle_file)

    file_list = sorted(map(lambda f: f.original, file_list))
    output = tree_output(path, file_list) if tree else file_list
    delimiter = '\0' if null else '\n'
    click.echo(delimiter.join(output), nl = not null)

def tree_output(path, files):
    head, tail = os.path.split(path)
    root = {
        'children': [],
        'dir': True,
        'name': path,
        'path': head if tail == '' else path,
    }

    index = 0;
    node = root
    done = False
    while not done:
        head, tail = os.path.split(files[index])
        if head == node['path']:
            node['children'].append({
                'dir': False,
                'name': tail,
            })
            index += 1
            done = index == len(files)
            continue

        if head.startswith(node['path']):
            new_path = None
            while head != node['path']:
                new_path = head
                head, tail = os.path.split(head)
            node = {
                'children': [],
                'dir': True,
                'name': tail,
                'path': new_path,
                'parent': node,
            }
            node['parent']['children'].append(node)
        else:
            node = node['parent']

    return node_output(root, '', [root['name']])

def node_output(node, prefix, output):
    children = node['children']
    for index, child in enumerate(children):
        child_prefix = None
        if (index + 1 == len(children)):
            child_prefix = f'{prefix}    '
            output.append(f"{prefix}└── {child['name']}")
        else:
            child_prefix = f'{prefix}│   '
            output.append(f"{prefix}├── {child['name']}")

        if child['dir']:
            node_output(child, child_prefix, output)
    return output
