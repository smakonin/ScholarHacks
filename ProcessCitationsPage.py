#!/usr/bin/env python3.5
#
# Process the stats on my Google Scholar Citations/Profile Page
# Copyright (C) 2016 Stephen Makonin. All Right Reserved.
#

import urllib.request, re, datetime
from html.parser import HTMLParser

scholar_url = 'https://scholar.google.ca/citations?user=cneuo_UAAAAJ&hl=en&pagesize=999'

journals = [['Transactions on Smart Grid'             , 'TSG'    , 6.645],
            ['Pervasive Computing'                    , 'PvC'    , 3.250],
            ['Energy Efficiency'                      , 'ENEF'   , 1.186],
            ['Journal on Computing'                   , 'JoC'    , 'tbd'],
            ['Scientific Data'                        , 'SData'  , 4.836],
            ['Transactions on Circuits and Systems II', 'TCAS-II', 1.660]]

def get_chunk(html, pre, post):
    start = html.find(pre) + len(pre)
    end = start + html[start:].find(post)
    return html[start:end]

def get_number(html, keyword, pre='<tr>', post='</tr>'):
    idx = html.rfind(keyword)
    start = html[:idx].rfind(pre) + 4
    end = idx + html[idx:].find(post)
    row = html[start:end]
    columns = row.replace('</td>', '</td>\n').split('\n')
    num = int(re.sub('<[^<]+?>', '', columns[1]))
    return num

def get_if(text):
    global total_if
    for journal in journals:
        if text.find(journal[0]) > -1:
            if journal[2] != 'tbd':
                total_if += journal[2]
                return '%10.03f' % (journal[2])
            else:
                return '%10s' % (journal[2])

    return ''

response = urllib.request.urlopen(scholar_url)
html = response.read().decode(response.headers.get_content_charset())
response.close()


print()
print('Report generated on:', datetime.datetime.now())

print()

keys = ['Citations',
        'h-index',
        'i10-index']

for key in keys:
    print('%-9s = %7s' % (key, format(get_number(html, key), ',d')))

print()

###EXAMPLE: get specific paper citations
#papers = {'cneuo_UAAAAJ:zYLM7Y9cAGgC': 'AMPds: A public dataset for load disaggregation and eco-feedback research',
#          'cneuo_UAAAAJ:UebtZRa9Y70C': 'Visual C++ 5.0 Developer\'s Guide',
#          'cneuo_UAAAAJ:LkGwnXOMwfcC': 'Transmitting Patient Vitals Over a Reliable ZigBee Mesh Network'}
#
#for key in papers:
#    print('%-50s citations = %5s' % (papers[key][:50], get_number(html, key, row_start='<tr class="gsc_a_tr">')))


papers_html = get_chunk(html, '<tbody id="gsc_a_b">', '</tbody>')
papers_html = papers_html.replace('<tr class="gsc_a_tr">', '')
papers_html = papers_html.replace('</tr>', '\n')
papers = papers_html[:-1].split('\n')
hparser = HTMLParser()

title_len = 70
print_templ = '%-' + str(title_len) + 's %9s %-10s'

print(print_templ % ('Paper Title', 'Citations', 'Journal IF'))
print(print_templ % ('-' * title_len, '-' * 9, '-' * 10))
total = 0
total_if = 0
for paper in papers:
    key = 'citation_for_view='
    start = paper.find(key) + len('citation_for_view=')
    end = start + paper[start:].find('"')
    id = paper[start:end]

    paper = [v for v in re.sub('<[^<]+?>', '|', paper).split('|') if v]
    if len(paper) == 0:
        continue

    name = hparser.unescape(paper[0])
    if len(name) > title_len:
        name = name[:(title_len-3)] + '...'

    if len(paper) < 6:
        count = 0
    else:
        try:
            count = int(paper[4])
        except:
            count = 0

    if count == 0:
        continue

    impact = get_if(paper[2])

    print(print_templ % (name[:title_len], format(count, ',d'), impact))
    total += count

print(print_templ % ('-' * title_len, '-' * 9, '-' * 10))

print(print_templ % ('Total Number of Papers = ' + str(len(papers)), format(total, ',d'), format(total_if, '10.3f')))
#print('TOTALS: Number of Papers =', len(papers), ' Citations =', format(total, ',d'), 'and Impact Factor =', total_if)

print()
