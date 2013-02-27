#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      Luke
#
# Created:     20/08/2012
# Copyright:   (c) Luke 2012
# Licence:     <your licence>
#-------------------------------------------------------------------------------
#!/usr/bin/env python

# -*- coding: utf-8 -*-
import os
import sys
from datetime import datetime as dt
import json
import feedparser
from bs4 import BeautifulStoneSoup
from nltk import clean_html

# Example feed:
# http://feeds.feedburner.com/oreilly/radar/atom
FEED_URL = 'http://feeds.feedburner.com/oreilly/radar/atom'

def cleanHtml(html):
    return BeautifulStoneSoup(clean_html(html)).contents[0]

fp = feedparser.parse(FEED_URL)
print "Fetched %s entries from '%s'" % (len(fp.entries[0].title), fp.feed.title)
blog_posts = []
for e in fp.entries:
    blog_posts.append({'title': e.title, 'content'
: cleanHtml(e.content[0].value), 'link': e.links[0].href})
if not os.path.isdir('out'):
    os.mkdir('out')
out_file = '%s__%s.json' % (fp.feed.title, dt.utcnow())
f = open(os.path.join(os.getcwd(), 'out', out_file), 'w')
f.write(json.dumps(blog_posts))
f.close()
print >> sys.stderr, 'Wrote output file to %s' % (f.name, )

#Modify to place in CouchDB