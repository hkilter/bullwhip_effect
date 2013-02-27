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
from bs4 import BeautifulSoup
from urllib import urlopen
import nltk

# Need to build a class based url text parser similar to fpdb or hand histories
# Example feed:
# http://feeds.feedburner.com/oreilly/radar/atom
URL = 'http://thepaymentsblog.com/2012/07/28/which-is-better-or-worse-irrational-exuberance-or-blatant-denial-of-reality/'

html = urlopen(URL).read()
soup = BeautifulSoup(html)
text = soup.get_text()
text2 = nltk.clean_html(text)

def cleanHtml(html):
    html = urlopen(html).read()
    return nltk.clean_html(html)

def extractchunk(html):
    sentences = [nltk.tokenize.sent_tokenize(html)]
    tokens = [nltk.tokenize.word_tokenize(str(s)) for s in sentences]
    pos_tagged_tokens = [nltk.pos_tag(t) for t in tokens]
    ne_chunks = nltk.batch_ne_chunk(pos_tagged_tokens)
    return ne_chunks

urltext = cleanHtml(html)
ne_chunks1 = extractchunk(urltext)

def extractComp(url_chunk):
    comparison = []
    ne_chunk = [c for (a,w,c) in tweet_chunk]
    cid = [str(a) for (a,w, c) in tweet_chunk]
    tnum =[w for (a,w,c) in tweet_chunk]

    for i in range(len(ne_chunks1)):
        tree = cp.parse(ne_chunks1[i])
        for subtree in tree.subtrees():
            try:
                subtags = [pos for (word, pos) in ne_chunks1[i].leaves() if (len(pos) >1)]
            except:
                continue
            subwords = [word for (word,pos) in ne_chunks1[i].leaves() if (len(word) >1)]
            subtest = [x for x in subtags if pattern.search(str(x))]
            # Tests if tree is comparative
            if (len(subtest) > 0 or subtree.node == 'COMP'):
                try:
                    comparison.insert(i,'COMP')
                except:
                    continue
                break
            else:
                comparison.insert(i,'NON-COMP')
                continue
    return zip(cid, tnum, comparison)

##print "Fetched %s entries from '%s'" % (len(fp.entries[0].title), fp.feed.title)
##blog_posts = []
##for e in fp.entries:
##    blog_posts.append({'title': e.title, 'content'
##: cleanHtml(e.content[0].value), 'link': e.links[0].href})
##if not os.path.isdir('out'):
##    os.mkdir('out')
##out_file = '%s__%s.json' % (fp.feed.title, dt.utcnow())
##f = open(os.path.join(os.getcwd(), 'out', out_file), 'w')
##f.write(json.dumps(blog_posts))
##f.close()
##print >> sys.stderr, 'Wrote output file to %s' % (f.name, )

#needs to take a blog and make a pigeon posts object(similar to a tweet)
#automatic summary and


#Modify to place in CouchDB