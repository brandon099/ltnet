#!/usr/bin/python

import re
import os
import sys
import logging as log
from urllib import request

log.basicConfig(format='%(message)s',
                level=log.DEBUG,
                stream=sys.stdout)

WHITE_PATH = os.path.abspath('/app/whitelist.txt')
SKIPS = ('localhost', 'broadcasthost',)

PREFACE = """# generated hosts a-record file

# Custom host records
# ---------------------------


# ---------------------------
"""

TEMPLATE = """
local-zone: "{site}" redirect
local-data: "{site} A 0.0.0.0"
""".lstrip()


def download(url):
    log.debug('..downloading from, %s', url)
    fp = request.urlopen(url)
    page_bytes = fp.read()
    sites = set()
    for line in page_bytes.decode('utf-8').split('\n'):
        line = line.lower()
        if line.startswith('#') or not line:
            # we don't care about comments
            continue
        for s in SKIPS:
            # these should be added to the outfile preface
            if s in line:
                continue
        site = line.split()
        if len(site) < 2:
            # improperly formatted list item
            continue
        # isolate the domain from comments
        site = site[1]
        if site.count('.') == 1:
            # no prefix, add www
            sites.add('www.%s' % site)
        if site.startswith('www.'):
            # has www. prefix, add non-prefix domain
            sites.add(site[4:])
        sites.add(site)
    log.debug('....hosts in file, %d', len(sites))
    return sites


def do_whitelisting(sites_set):
    rules = []

    with open(WHITE_PATH, 'r') as ins_file:
        for line in ins_file:
            if line.startswith('#') or not line.strip():
                continue
            rule = line.split('#')[0].strip()
            rules.append(re.compile(rule, re.I))

    log.info('.. %d  whitelist rules', len(rules))

    purge = set()

    for regex in rules:
        for site in sites_set:
            if regex.match(site):
                purge.add(site)

    log.info('.. %d  sites removed via %s', len(purge), WHITE_PATH)
    sites_set.difference_update(purge)


def output_sites(path, sites_set):
    log.debug('..creating file with %d hosts', len(sites_set))
    log.debug('..saving file to, %s', path)

    # do whitelisting
    if os.path.exists(WHITE_PATH):
        do_whitelisting(sites_set)

    with open(path, 'w') as out_file:
        out_file.write(PREFACE)
        for site in sorted(sites_set):
            out_file.write(TEMPLATE.format(site=site))

    return len(sites_set)

if __name__ == '__main__':
    all_sites = set()

    if len(sys.argv) < 3:
        print('list-download.py OUTPUT_PATH SITE [SITE SITE ..] ')
        sys.exit(0)

    total = 0

    for url in sys.argv[2:]:
        url = url.strip('\'" ,').replace(',', ' ')
        for u in url.split():
            if not u:
                continue
            sites = download(u)
            total += len(sites)
            all_sites.update(sites)

    final_total = output_sites(sys.argv[1], all_sites)

    log.debug('.. %d  duplicates removed ', total - final_total)
