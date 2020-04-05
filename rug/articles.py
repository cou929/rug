# -*- coding: utf-8 -*-

"""
rug.articles

The model account for articles.
"""

import os
import re
import pwd


class Articles:
    def __init__(self, path):
        if (not os.path.exists(path)):
            raise StandardError('no such file or directory: %s' % path)
        self.articles = []
        self.path = path
        self.supported_suffixes = ['md']
        self.load()

    def load(self):
        result = []
        articles = self._list_articles(self.path)
        for article in articles:
            result.append(self._parse_article(article))
        self.articles = result

    def get(self):
        return self.articles

    def _list_articles(self, filepath):
        results = []
        pattern = '^(' + '|'.join(self.supported_suffixes) + ')$'
        is_supported = re.compile(pattern)

        for root, dirs, files in os.walk(filepath):
            for f in files:
                suffix = f.split('.')[-1]
                if is_supported.match(suffix):
                    results.append(os.path.join(root, f))

        return results

    def _parse_article(self, filepath):
        header = ''
        markdown_string = ''
        with open(filepath, 'r') as f:
            header = f.readline()
            markdown_string = f.read()
        (title, tags) = self._parse_header(header)
        (mode, ino, dev, nlink, uid,
         gid, size, atime, mtime, ctime) = os.stat(filepath)
        issued = mtime
        author = pwd.getpwuid(uid).pw_gecos
        filename = '.'.join(filepath.split('/')[-1].split('.')[0:-1])

        return {
            'title': title,
            'author': author,
            'tags': tags,
            'issued': issued,
            'path': filepath,
            'filename': filename,
            'content': markdown_string,
            }

    def _parse_header(self, header):
        '''
        >>> self._parse_header('* tag: title')
        ('title', ['tag'])
        >>> self._parse_header('*tag,tag, tag2:  this is title   ')
        ('this is title', ['tag', 'tag2'])
        '''
        title = ''
        tags = []
        head_parser = re.compile(r'^\*(.*?):(.*?)$')

        res = head_parser.search(header)
        if res:
            (tagstring, title) = res.groups()
            tags = self._extract_tags(tagstring)

        return (title.strip(), tags)

    def _extract_tags(self, tagstring):
        '''
        >>> self._extract_tags('foo, bar, baz')
        ['foo', 'bar', 'baz']
        >>> self._extract_tags('blah, blah, blah')
        ['blah']
        >>> self._extract_tags('foo,bar,bar')
        ['foo', 'bar']
        >>> self._extract_tags('     foo,bar,bar       ,  baz')
        ['foo', 'bar', 'baz']
        >>> self._extract_tags('')
        []
        >>> self._extract_tags('   ')
        []
        '''
        return self._unique(filter(
                lambda x: x != '',
                map(lambda x: x.strip(), tagstring.split(','))
                ))

    def _unique(self, seq):
        '''
        >>> self._unique([1, 2, 2, 3])
        [1, 2, 3]
        >>> self._unique(['foo', 'foo', 'foo'])
        ['foo']
        '''
        checked = []
        for i in seq:
            if i not in checked:
                checked.append(i)
        return checked


if __name__ == '__main__':
    import doctest
    doctest.testmod(extraglobs={'self': Articles('/tmp')})
