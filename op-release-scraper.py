#!/usr/bin/env python3

import json
from argparse import ArgumentParser, FileType
from sys import stdin, stdout

from bs4 import BeautifulSoup, ResultSet, Tag


def scrape_downloads(hrefs: ResultSet):
    links = {}
    for a in hrefs:
        links[a.get_text()] = a.get_attribute_list('href')[0]
    return links


def scrape_article(article: Tag):
    ret = {}
    ret['id'] = article.get_attribute_list('id')[0]
    ret['version'] = article.find_all('h3')[0].text.split()[0].strip()
    released = article.find_all('span')[0].text.strip()
    ret['released'] = released[released.rfind(' ') + 1:]
    ret['downloads'] = {}
    system_apple = article.find_all('p', {'class': 'system apple'})[0]
    ret['downloads']['macOS'] = scrape_downloads(
        system_apple.find_all('a', href=True))
    system_freebsd = article.find_all('p', {'class': 'system freebsd'})[0]
    ret['downloads']['FreeBSD'] = scrape_downloads(
        system_freebsd.find_all('a', href=True))
    system_linux = article.find_all('p', {'class': 'system linux'})[0]
    ret['downloads']['Linux'] = scrape_downloads(
        system_linux.find_all('a', href=True))
    system_openbsd = article.find_all('p', {'class': 'system openbsd'})[0]
    ret['downloads']['OpenBSD'] = scrape_downloads(
        system_openbsd.find_all('a', href=True))
    system_windows = article.find_all('p', {'class': 'system windows'})[0]
    ret['downloads']['Windows'] = scrape_downloads(
        system_windows.find_all('a', href=True))
    return ret


def main():
    parser = ArgumentParser()
    parser.add_argument('-i',
                        '--in-file',
                        type=FileType('r'),
                        default=stdin,
                        help='input file, default: stdin')
    parser.add_argument('-o',
                        '--out-file',
                        type=FileType('w'),
                        default=stdout,
                        help='output file, default: stdout')
    args = parser.parse_args()
    soup = BeautifulSoup(args.in_file.read(), features='html.parser')
    releases = []
    for article in soup.find_all('article'):
        releases.append(scrape_article(article))
    print(json.dumps(releases, indent=2), file=args.out_file)

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        exit(130)
