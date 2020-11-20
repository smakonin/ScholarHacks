#!/usr/bin/env python3
#
# Process the stats on my Google Scholar Citations/Profile Page
# Copyright (C) 2016-2020 Stephen Makonin. All Right Reserved.
#


import datetime
from GoogleScholar import get_scholar_json


json = get_scholar_json('cneuo_UAAAAJ')

f = open('../smakonin.github.io/scholar.js', 'w')
f.write(json)
f.close()
