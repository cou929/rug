# -*- coding: utf-8 -*-

"""
rug.view

The model account for view.
"""

import os
import datetime
import markdown2
import pystache
import PyRSS2Gen


class Abstract:
    renderer = pystache.Renderer()

    def __init__(self, articles, template, output_path):
        self.articles = articles
        self.template = template
        self.output_path = output_path

    def publish(self):
        articles = self._extract_articles()
        self._render(articles)

    def _extract_articles(self):
        return self.articles

    def _render(self, articles):
        for article in articles:
            print(article.title)


class IndivisualPage(Abstract):
    def _extract_articles(self):
        result = []
        by_issued_date = lambda x: x['issued']
        sorted_list = sorted(self.articles, key=by_issued_date)
        list_length = len(sorted_list)

        for i, article in enumerate(sorted_list):
            if i > 0:
                article['prev'] = {
                    'title': sorted_list[i - 1]['title'],
                    'filename': sorted_list[i - 1]['filename']
                    }
            if i + 1 < list_length:
                article['next'] = {
                    'title': sorted_list[i + 1]['title'],
                    'filename': sorted_list[i + 1]['filename']
                    }
            result.append(article)

        return result

    def _render(self, articles):
        template_string = ''
        with open(self.template['layout'], 'r') as f:
            template_string = f.read()
        parsed = pystache.parse(template_string)

        for article in articles:
            html = markdown2.markdown(article['content'])
            dt = datetime.datetime.fromtimestamp(article['issued'])
            view_params = {
                'title': article['title'],
                'date': dt.strftime('%d %B %Y'),
                'date_iso': dt.isoformat(),
                'author': article['author'],
                'url': article['filename'] + '.html',
                'disqus_id': article['filename'],
                'content': html,
                'is_article': True,
                'year': dt.strftime('%Y'),
                }
            if 'prev' in article:
                view_params['prev_article'] = {
                    'url': article['prev']['filename'] + '.html',
                    'title': article['prev']['title']
                    }
            if 'next' in article:
                view_params['next_article'] = {
                    'url': article['next']['filename'] + '.html',
                    'title': article['next']['title']
                    },
            dest_path = os.path.join(self.output_path,
                              article['filename'] + '.html')
            with open(dest_path, 'w') as f:
                f.write(self.renderer.render(parsed, view_params))


class ArchivePage(Abstract):
    html_filename = 'index.html'

    def _extract_articles(self):
        by_issued_date = lambda x: x['issued']
        result = sorted(self.articles, key=by_issued_date)
        result.reverse()
        return result

    def _render(self, articles):
        template_string = ''
        with open(self.template['layout'], 'r') as f:
            template_string = f.read()
        layout_parsed = pystache.parse(template_string)
        with open(self.template['content'], 'r') as f:
                template_string = f.read()
                content_parsed = pystache.parse(template_string)

        params = []
        for article in articles:
            dt = datetime.datetime.fromtimestamp(article['issued'])
            params.append({
                'href': article['filename'] + '.html',
                'date': dt.strftime('%d %B %Y'),
                'title': article['title'],
                })
        contents = self.renderer.render(content_parsed, {'articles': params})

        dt = datetime.datetime.now()
        param = {
            'content': contents,
            'date': dt.strftime('%d %B %Y'),
            'date_iso': dt.isoformat(),
            'author': articles[0]['author'],
            'url': self.html_filename,
            'year': dt.strftime('%Y'),
            }

        dest_path = os.path.join(self.output_path, self.html_filename)
        with open(dest_path, 'w') as f:
            f.write(self.renderer.render(layout_parsed, param))


class AboutPage(Abstract):
    html_filename = 'about.html'
    title = 'About me'
    published_on = datetime.datetime(2014, 2, 24, 1, 37, 27)

    def _render(self, articles):
        template_string = ''
        with open(self.template['layout'], 'r') as f:
            template_string = f.read()
        parsed = pystache.parse(template_string)

        contents = ''
        with open(self.template['content'], 'r') as f:
            contents = f.read()

        today = datetime.datetime.now()
        param = {
            'content': contents,
            'date': self.published_on.strftime('%d %B %Y'),
            'date_iso': self.published_on.isoformat(),
            'title': self.title,
            'url': self.html_filename,
            'year': today.strftime('%Y'),
            'is_article': True,
            }

        dest_path = os.path.join(self.output_path, self.html_filename)
        with open(dest_path, 'w') as f:
            f.write(self.renderer.render(parsed, param))


class RSS(Abstract):
    rss_filename = 'rss.xml'
    rss_itemnum = 10

    def _extract_articles(self):
        by_issued_date = lambda x: x['issued']
        result = sorted(self.articles, key=by_issued_date)
        result.reverse()
        return result[:self.rss_itemnum]

    def _render(self, articles):
        items = []
        host = 'http://please-sleep.cou929.nu/'

        for article in articles:
            markdown_string = ''
            with open(article['path'], 'r') as f:
                f.readline()  # remove header
                markdown_string = f.read()
            html = markdown2.markdown(markdown_string)
            url = host + article['filename'] + '.html'
            items.append(PyRSS2Gen.RSSItem(
                    title=article['title'],
                    link=url,
                    description=html,
                    guid=PyRSS2Gen.Guid(url),
                    pubDate=datetime.datetime.fromtimestamp(article['issued'])
                    ))

        rss = PyRSS2Gen.RSS2(
            title='Please Sleep',
            link=host,
            description=u'From notes on my laptop.',
            lastBuildDate=datetime.datetime.now(),
            items=items
            )

        dest_path = os.path.join(self.output_path, self.rss_filename)
        rss.write_xml(open(dest_path, 'w'), encoding='utf-8')
