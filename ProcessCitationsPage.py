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
	print('%-9s = %5d' % (key, get_number(html, key)))

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

print('%-70s %9s' % ('Paper Title', 'Citations'))
print('%-70s %9s' % ('-' * 70, '-' * 9))
total = 0
for paper in papers:
	paper = [v for v in re.sub('<[^<]+?>', '|', paper).split('|') if v]
	if len(paper) == 0:
		continue

	id = ''
	name = paper[0]

	if len(paper) < 6:
		count = 0
	else:
		try:
			count = int(paper[4])
		except:
			count = 0

	print('%-70s %9d' % (name[:70], count))
	total += count

print('%-70s %9s' % ('-' * 70, '-' * 9))

print('TOTALS: Number of Papers =', len(papers), 'and Citations =', total)

print()

#print(rows[0])	
#
['AMPds: A public dataset for load disaggregation and eco-feedback research', 'S Makonin, F Popowich, L Bartram, B Gill, IV Bajic', 'Electrical Power &amp; Energy Conference (EPEC), 2013 IEEE, 1-6', ', 2013', '78', '2013']
#
#
#<td class="gsc_a_t"><a href="/citations?view_op=view_citation&amp;hl=en&amp;oe=ASCII&amp;user=cneuo_UAAAAJ&amp;pagesize=100&amp;citation_for_view=cneuo_UAAAAJ:zYLM7Y9cAGgC" class="gsc_a_at">AMPds: A public dataset for load disaggregation and eco-feedback research</a><div class="gs_gray">S Makonin, F Popowich, L Bartram, B Gill, IV Bajic</div><div class="gs_gray">Electrical Power &amp; Energy Conference (EPEC), 2013 IEEE, 1-6<span class="gs_oph">, 2013</span></div></td><td class="gsc_a_c"><a href="https://scholar.google.ca/scholar?oi=bibs&amp;hl=en&amp;oe=ASCII&amp;cites=9977726888743581483" class="gsc_a_ac">78</a></td><td class="gsc_a_y"><span class="gsc_a_h">2013</span></td>
#


