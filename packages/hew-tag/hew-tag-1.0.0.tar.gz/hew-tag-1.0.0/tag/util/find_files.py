from . import File
import os

def find_files(path, recursive, all, handler):
    def filename_p(filename):
        return all or not filename.startswith('.')

    def found(root, file):
        handler(File(os.path.join(root, file)))

    if recursive:
        for root, dirs, files in os.walk(path):
            for file in filter(filename_p, files):
                found(root, file)
    else:
        for entry in os.scandir(path):
            if entry.is_file() and filename_p(entry.name):
                found(path, entry.name)
