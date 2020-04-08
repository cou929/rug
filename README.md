# rug

A static web page generator for myself. Built for [Please Sleep](http://please-sleep.cou929.nu/).

**Note**: This script is very early stage of development.

## Synopsys

    go get github.com/russross/blackfriday-tool
    rug -a /path/to/articles/ -t /path/to/templates/ -o /path/to/output/

This will search the articles in `/path/to/articles/`, which is written as markdown, build html with templates and save these to `/path/to/output/`.

### Options

    -h, --help            show this help message and exit
    -a ARTICLE_PATH, --articles=ARTICLE_PATH
                          path to articles dir (required)
    -t TEMPLATE_PATH, --templete=TEMPLATE_PATH
                          path to templates dir (required)
    -o OUTPUT_PATH, --output=OUTPUT_PATH
                          path to output dir (required)
    -n, --norss           don't publish new rss feed

### Installation

    $ python setup.py install
