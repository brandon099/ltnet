#!/usr/bin/python

import os
import sys
import logging as log
from urllib import request

log.basicConfig(level=log.DEBUG, stream=sys.stdout)

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


def output_sites(path, sites_set):
    log.debug('..creating file with %d hosts', len(sites_set))
    log.debug('..saving file to, %s', path)

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

    log.debug('..removed %d duplicates', total - final_total)
