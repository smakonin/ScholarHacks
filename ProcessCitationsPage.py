#!/usr/bin/env python3
#
# Process the stats on my Google Scholar Citations/Profile Page
# Copyright (C) 2016 Stephen Makonin. All Right Reserved.
#

import urllib.request, re, datetime, html as HTML
from html.parser import HTMLParser

scholar_url = 'https://scholar.google.ca/citations?user=cneuo_UAAAAJ&hl=en&pagesize=999'

journals = [['Transactions on Smart Grid'             , 'TSG'    , 7.364],
            ['Pervasive Computing'                    , 'PvC'    , 3.022],
            ['Energy Efficiency'                      , 'ENEF'   , 1.634],
            ['Journal on Computing'                   , 'JoC'    , 'tbd'],
            ['Scientific Data'                        , 'SData'  , 4.836],
            ['Applied Energy'                         , 'APEN'   , 7.900],
            ['Data in Brief'                          , 'DIB'    , 'tbd'],
            ['Transactions on Circuits and Systems II', 'TCAS-II', 2.450],
            ['MDPI Data'                              , 'DATA'   , 'tbd']]

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
    global impact_tl
    for journal in journals:
        if text.find(journal[0]) > -1:
            if journal[2] != 'tbd':
                impact_tl += journal[2]
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
conf_citations = 0
journal_papers = 0
journal_citations = 0
impact_tl = 0
for paper in papers:
    key = 'citation_for_view='
    start = paper.find(key) + len('citation_for_view=')
    end = start + paper[start:].find('"')
    id = paper[start:end]

    paper = [v for v in re.sub('<[^<]+?>', '|', paper).split('|') if v]
    if len(paper) == 0:
        continue

    name = HTML.unescape(paper[0])
    if len(name) > title_len:
        name = name[:(title_len-3)] + '...'

    if len(paper) < 6:
        count = 0
    else:
        try:
            count = int(paper[4])
        except:
            count = 0

    impact = get_if(paper[2])

    if count == 0 and impact == '':
        continue

    if impact != '':
        journal_papers += 1
        journal_citations += count
    else:
        conf_citations += count

    print(print_templ % (name[:title_len], format(count, ',d'), impact))

print(print_templ % ('-' * title_len, '-' * 9, '-' * 10))

conf_papers = len(papers) - journal_papers

print(print_templ % ('Peer-Reviewed Conferences:                                  ' + format(conf_papers, '3d') + ' papers', format(conf_citations, ',d'), format(0, '10.3f')))
print(print_templ % ('Peer-Reviewed Journals:                                     ' + format(journal_papers, '3d') + ' papers', format(journal_citations, ',d'), format(impact_tl, '10.3f')))
print(print_templ % ('                                                            ----------', '---------', '----------'))
print(print_templ % ('Grand Totals:                                               ' + format(conf_papers+journal_papers, '3d') + ' papers', format(conf_citations+journal_citations, ',d'), format(impact_tl, '10.3f')))
print(print_templ % ('                                                            ==========', '=========', '==========')) 


# print(print_templ % ('Total Number of Papers = ' + str(len(papers)), format(conf_citations, ',d'), format(impact_tl, '10.3f')))
# #print('TOTALS: Number of Papers =', len(papers), ' Citations =', format(conf_citations, ',d'), 'and Impact Factor =', impact_tl)
# print(print_templ % ('Total Peer-Reviewed Conference Papers = ' + str(len(papers)), format(conf_citations, ',d'), format(impact_tl, '10.3f')))
# print(print_templ % ('Total Peer-Reviewed Journal Papers    = ' + str(len(papers)), format(journal_papers, ',d'), format(impact_tl, '10.3f')))
print()
