#!/usr/bin/env python3
#
# Process the stats on my Google Scholar Citations/Profile Page
# Copyright (C) 2016-2020 Stephen Makonin. All Right Reserved.
#


import datetime
from GoogleScholar import get_scholar_data


print()
print('Report generated on:', datetime.datetime.now())

print()

(agg, papers) = get_scholar_data('cneuo_UAAAAJ')

for key in agg:
    print('%-9s = %7s' % (key, format(agg[key], ',d')))
print()

title_len = 70
print_templ = '%-' + str(title_len) + 's %9s %-10s'

print(print_templ % ('Paper Title', 'Citations', 'Journal IF'))
print(print_templ % ('-' * title_len, '-' * 9, '-' * 10))
conf_citations = 0
journal_papers = 0
journal_citations = 0
book_citations = 0
impact_total = 0
book_count = 0
for paper in papers:
    name = paper.title
    if len(name) > title_len:
        name = name[:(title_len-3)] + '...'

    impact = ''

    if paper.is_conference:
        if paper.citations == 0:
            continue
        conf_citations += paper.citations
    if paper.is_journal:
        journal_papers += 1
        journal_citations += paper.citations

        if paper.impact_factor != 'tbd':
            impact = float(paper.impact_factor)
            impact_total += impact
            impact = '%10.03f' % (impact)
        else:
            impact = '%10s' % (paper.impact_factor)
    elif paper.is_book:
        book_count += 1
        book_citations += paper.citations

    print(print_templ % (name[:title_len], format(paper.citations, ',d'), impact))

print(print_templ % ('-' * title_len, '-' * 9, '-' * 10))

conf_papers = len(papers) - (journal_papers + book_count)
total_papers = conf_papers + journal_papers + book_count
total_citations = conf_citations + journal_citations + book_citations

print(print_templ % ('Peer-Reviewed Conferences:                                ' + format(conf_papers, '3d') + ' papers', format(conf_citations, ',d'), ''))
print(print_templ % ('Peer-Reviewed Journals:                                   ' + format(journal_papers, '3d') + ' articles', format(journal_citations, ',d'), format(impact_total, '10.3f')))
print(print_templ % ('Books Co-authored/Co-edited:                              ' + format(book_count, '3d') + ' books', format(book_citations, ',d'), ''))
print(print_templ % ((' ' * (title_len - 12)) + ('-' * 12), '-' * 9, '-' * 10))
print(print_templ % ('Grand Totals:                                             ' + format(total_papers, '3d') + ' works', format(total_citations, ',d'), format(impact_total, '10.3f')))
print(print_templ % ((' ' * (title_len - 12)) + ('=' * 12), '=' * 9, '=' * 10))

print()
