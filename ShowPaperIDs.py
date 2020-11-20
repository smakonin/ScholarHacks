#!/usr/bin/env python3
#
# Process the stats on my Google Scholar Citations/Profile Page
# Copyright (C) 2020 Stephen Makonin. All Right Reserved.
#


import datetime
from GoogleScholar import get_scholar_data


print()
print('Papers and their Google Scholar IDs:', datetime.datetime.now())

print()

(agg, papers) = get_scholar_data('cneuo_UAAAAJ')

title_len = 80
id_len = 30
print_templ = '%-' + str(id_len) + 's ' + '%-' + str(title_len) + 's '

print(print_templ % ('Google Scholar ID', 'Paper Title'))
print(print_templ % ( '-' * id_len, '-' * title_len))

for paper in papers:
    name = paper.title
    if len(name) > title_len:
        name = name[:(title_len-3)] + '...'

    print(print_templ % (paper.id[:id_len], name[:title_len]))

print(print_templ % ( '-' * id_len, '-' * title_len))

print()
