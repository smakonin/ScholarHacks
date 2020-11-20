#!/usr/bin/env python3
#
# Process the stats on my Google Scholar Citations/Profile Page
# Copyright (C) 2020 Stephen Makonin. All Right Reserved.
#


import datetime
from GoogleScholar import get_scholar_data

(agg, papers) = get_scholar_data('cneuo_UAAAAJ')

f = open('./homepage.html', mode='r')
homepage = f.read()
f.close()

title_len = 80
id_len = 30
print_templ = '%-' + str(id_len) + 's ' + '%-' + str(title_len) + 's %9s'


old_papers = ''
new_papers = ''

for paper in papers:
    name = paper.title
    if len(name) > title_len:
        name = name[:(title_len-3)] + '...'

    if homepage.find(paper.id) < 0:
        new_papers += print_templ % (paper.id[:id_len], name[:title_len], format(paper.citations, ',d')) + '\n'
    else:
        old_papers += print_templ % (paper.id[:id_len], name[:title_len], format(paper.citations, ',d')) + '\n'


print()
print('Papers and their Google Scholar IDs:', datetime.datetime.now())
print()
print('IDs in Homepage:')
print(print_templ % ( '-' * id_len, '-' * title_len, '-' * 9))
print(print_templ % ('Google Scholar ID', 'Paper Title', 'Citations'))
print(print_templ % ( '-' * id_len, '-' * title_len, '-' * 9))
print(old_papers[:-1])
print(print_templ % ( '-' * id_len, '-' * title_len, '-' * 9))
print()
print('IDs *NOT* in Homepage:')
print(print_templ % ( '-' * id_len, '-' * title_len, '-' * 9))
print(print_templ % ('Google Scholar ID', 'Paper Title', 'Citations'))
print(print_templ % ( '-' * id_len, '-' * title_len, '-' * 9))
print(new_papers[:-1])
print(print_templ % ( '-' * id_len, '-' * title_len, '-' * 9))

print()
