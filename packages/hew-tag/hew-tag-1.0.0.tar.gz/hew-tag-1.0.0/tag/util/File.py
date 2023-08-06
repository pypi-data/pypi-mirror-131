import os
import re

TAG_RE = re.compile(r'\{[a-zA-Z0-9-]+\}')

def get_raw_tags(filename):
    return TAG_RE.findall(filename)

def get_tag(raw_tag):
    return raw_tag[1:-1]

class File:
    def __init__(self, filepath):
        self.original = filepath
        self.dir, self.filename = os.path.split(self.original)
        self.base, self.ext = os.path.splitext(self.filename)
        raw_tags = get_raw_tags(self.base)
        self.tags = set()

        for raw_tag in raw_tags:
            self.base = self.base.replace(raw_tag, '')
            self.tags.add(get_tag(raw_tag))

    def __repr__(self):
        return f"File('{self.original}')"

    @property
    def absolute_path(self):
        return os.path.abspath(self.relative_path)

    @property
    def relative_path(self):
        tags = sorted(self.tags)
        tag_text = '{' + '}{'.join(tags) + '}' if len(tags) > 0 else ''
        filename = f"{self.base}{tag_text}{self.ext}"
        return os.path.join(self.dir, filename)
