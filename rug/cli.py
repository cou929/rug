# -*- coding: utf-8 -*-

"""
rug.cli

CLI interface.
"""

import os
import sys
import optparse
from .articles import Articles
from .articles import ArticlesWithMeta
from .view import IndivisualPage, ArchivePage, AboutPage, RSS


def dispatch():
    """
    Dispatcher.
    Read stdin and command line options, then call property method.
    """

    usage = 'usage: %prog -a ARTICLE_PATH -t TEMPLATE_PATH -o OUTPUT_PATH'
    parser = optparse.OptionParser(usage=usage)
    parser.add_option("-a", "--articles", action="store", dest="article_path",
                      type="string", help="path to articles dir (required)",
                      )
    parser.add_option("-t", "--templete", action="store", dest="template_path",
                      type="string", help="path to templates dir (required)",
                      )
    parser.add_option("-o", "--output", action="store", dest="output_path",
                      type="string", help="path to output dir (required)",
                      )
    parser.add_option("-n", "--norss", action="store_true",
                      dest="norss", default=False,
                      help="don't publish new rss feed"
                      )
    (options, args) = parser.parse_args()

    if (not options.article_path or
        not options.template_path or
        not options.output_path):
        parser.print_usage()
        sys.exit(1)

    run(options.article_path,
        options.template_path,
        options.output_path,
        options.norss)

    sys.exit()


def run(article_path, template_path, output_path, norss):
    articles = ArticlesWithMeta(article_path).get()
    templates = {
        'layout': os.path.join(template_path, 'layout.mustache')
        }
    indivisual_page = IndivisualPage(articles,
                                          templates,
                                          output_path)
    indivisual_page.publish()

    templates['content'] = os.path.join(
        template_path, 'include', 'archive.mustache')
    archive_pate = ArchivePage(articles, templates, output_path)
    archive_pate.publish()

    templates['content'] = os.path.join(
        template_path, 'include', 'about.html')
    about_pate = AboutPage([], templates, output_path)
    about_pate.publish()

    if not norss:
        rss = RSS(articles, templates, output_path)
        rss.publish()
