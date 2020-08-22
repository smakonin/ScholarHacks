# Simple libreary  to process Google Scholar Citations
# Copyright (C) 2016 Stephen Makonin. All Right Reserved.
#


import urllib.request, re, datetime, json, html as HTML
from html.parser import HTMLParser
from pprint import pprint
from dataclasses import dataclass, asdict, astuple


journals = [['Transactions on Smart Grid'             , 'TSG'    , 10.486],
            ['Pervasive Computing'                    , 'PvC'    ,  3.022],
            ['Energy Efficiency'                      , 'ENEF'   ,  1.961],
            ['Journal on Computing'                   , 'JoC'    ,  'tbd'],
            ['Scientific Data'                        , 'SData'  ,  6.776],
            ['Applied Energy'                         , 'APEN'   ,  8.426],
            ['Data in Brief'                          , 'DIB'    ,  1.430],
            ['Transactions on Circuits and Systems II', 'TCAS-II',  3.250],
            ['MDPI Data'                              , 'DATA'   ,  'tbd'],
            ['IEEE Access'                            , 'Access' ,  4.098]]
            ['Transactions on Power Systems'          , 'TPWRS'  ,  6.047],
            ['Transactions on Sustainable Energy'     , 'TSTE'   ,  7.440]]

books =    ['Sams Publishing',
            'Woodhead Publishing']

scholar_url = 'https://scholar.google.ca/citations?user=%s&hl=en&pagesize=999'

keys = ['Citations',
        'h-index',
        'i10-index']


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
    for journal in journals:
        if text.find(journal[0]) > -1:
            return journal[2]

    return ''

def is_book(text):
    for book in books:
        if text.find(book) > -1:
            return True

    return False


@dataclass
class PaperData:
    id: str
    title: str
    citations: int
    is_conference: bool
    is_journal: bool
    is_book: bool
    impact_factor: str


###EXAMPLE: get specific paper citations
#papers = {'cneuo_UAAAAJ:zYLM7Y9cAGgC': 'AMPds: A public dataset for load disaggregation and eco-feedback research',
#          'cneuo_UAAAAJ:UebtZRa9Y70C': 'Visual C++ 5.0 Developer\'s Guide',
#          'cneuo_UAAAAJ:LkGwnXOMwfcC': 'Transmitting Patient Vitals Over a Reliable ZigBee Mesh Network'}
#
#for key in papers:
#    print('%-50s citations = %5s' % (papers[key][:50], get_number(html, key, row_start='<tr class="gsc_a_tr">')))

def get_scholar_data(id):
    agg = []
    data = []

    response = urllib.request.urlopen(scholar_url % id)
    html = response.read().decode(response.headers.get_content_charset())
    response.close()

    papers_html = get_chunk(html, '<tbody id="gsc_a_b">', '</tbody>')
    papers_html = papers_html.replace('<tr class="gsc_a_tr">', '')
    papers_html = papers_html.replace('</tr>', '\n')
    papers = papers_html[:-1].split('\n')
    hparser = HTMLParser()

    agg = {}
    for key in keys:
        agg[key] = int(get_number(html, key))

    for paper in papers:
        key = 'citation_for_view='
        start = paper.find(key) + len('citation_for_view=')
        end = start + paper[start:].find('"')
        id = paper[start:end]

        paper = [v for v in re.sub('<[^<]+?>', '|', paper).split('|') if v]
        if len(paper) == 0:
            continue

        if len(paper) < 6:
            count = 0
        else:
            try:
                count = int(paper[4])
            except:
                count = 0

        name = HTML.unescape(paper[0])
        impact = get_if(paper[2])
        a_book = is_book(paper[2])

        data.append(PaperData(id, name, count, (impact == '' and not a_book), (impact != ''), a_book, impact))
    return (agg, data)

def get_scholar_json(id):
    (agg, papers) = get_scholar_data(id)

    dict = {'agg': {}, 'papers': {}}

    for key in agg:
        dict['agg'][key] = agg[key]

    for paper in papers:
        dict['papers'][paper.id] = asdict(paper)

    json_text = json.dumps(dict, sort_keys=True, indent=4)
    json_text = json_text.replace('"agg"', 'agg')
    json_text = json_text.replace('"papers"', 'papers')
    json_text = json_text.replace('"citations"', 'citations')
    json_text = json_text.replace('"id"', 'id')
    json_text = json_text.replace('"impact_factor"', 'impact_factor')
    json_text = json_text.replace('"is_book"', 'is_book')
    json_text = json_text.replace('"is_conference"', 'is_conference')
    json_text = json_text.replace('"is_journal"', 'is_journal')
    json_text = json_text.replace('"title"', 'title')
    return 'var sdata = ' + json_text


if __name__ == "__main__":
    print(get_scholar_json('cneuo_UAAAAJ'))
