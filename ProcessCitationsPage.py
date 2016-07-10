#!/usr/bin/env python3
#
# Process the stats on my Google Scholar Citations/Profile Page
# Copyright (C) 2016 Stephen Makonin. All Right Reserved.
#

import urllib.request, re


scholar_url = 'https://scholar.google.ca/citations?user=cneuo_UAAAAJ&hl=en&pagesize=999'

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
	
response = urllib.request.urlopen(scholar_url)
html = response.read().decode(response.headers.get_content_charset())
response.close()

print()

keys = ['Citations', 
		'h-index', 
		'i10-index']

for key in keys:
	print('%-9s = %7s' % (key, format(get_number(html, key), ',d')))

print()

###EXAMPLE: get specific paper citations
#papers = {'cneuo_UAAAAJ:zYLM7Y9cAGgC': 'AMPds: A public dataset for load disaggregation and eco-feedback research', 
#		  'cneuo_UAAAAJ:UebtZRa9Y70C': 'Visual C++ 5.0 Developer\'s Guide', 
#		  'cneuo_UAAAAJ:LkGwnXOMwfcC': 'Transmitting Patient Vitals Over a Reliable ZigBee Mesh Network'}
#
#for key in papers:
#	print('%-50s citations = %5s' % (papers[key][:50], get_number(html, key, row_start='<tr class="gsc_a_tr">')))
	

papers_html = get_chunk(html, '<tbody id="gsc_a_b">', '</tbody>')
papers_html = papers_html.replace('<tr class="gsc_a_tr">', '')
papers_html = papers_html.replace('</tr>', '\n')
papers = papers_html[:-1].split('\n')

print_templ = '%-25s %-70s %9s'

print(print_templ % ('Scholar ID', 'Paper Title', 'Citations'))
print(print_templ % ('-' * 25, '-' * 70, '-' * 9))
total = 0
for paper in papers:
	key = 'citation_for_view='
	start = paper.find(key) + len('citation_for_view=')
	end = start + paper[start:].find('"')
	id = paper[start:end]
		
	paper = [v for v in re.sub('<[^<]+?>', '|', paper).split('|') if v]
	if len(paper) == 0:
		continue
	name = paper[0]
	if len(name) > 70:
		name = name[:67] + '...'

	if len(paper) < 6:
		count = 0
	else:
		try:
			count = int(paper[4])
		except:
			count = 0

	print(print_templ % (id, name[:70], format(count, ',d')))
	total += count

print(print_templ % ('-' * 25, '-' * 70, '-' * 9))

print('TOTALS: Number of Papers =', len(papers), 'and Citations =', format(total, ',d'))

print()
