#-------------------------------------------------------------------------------
# Name:      Disruptive Junction
# Purpose:   Picks out comparative phrase sentences in text or a twitter
# feee
# Author:      Luke
#
# Created:     06/08/2012
# Copyright:   (c) Luke 2012
# Licence:     <your licence>
#-------------------------------------------------------------------------------
#!/usr/bin/env python

import nltk, re, pprint
import twitter
import couchdb
import simplejson as json
from string import join
from math import sqrt
from nltk.corpus import stopwords

# open the text file
##f = open('C:\Documents and Settings\Luke\Desktop\Programming\Python\py natural language\\CC_Disruptive.txt','r')
##raw = f.read()


#twitter search and directly pull comparisons
##search_results = []
##
##twitter_search = twitter.Twitter(domain='search.twitter.com')
##
##for page in range(1,6):
##    search_results.append(twitter_search.search(q='netflix', rpp=100, page=page))
##tweets = [r['text'] for result in search_results for r in result['results']]
##
##tokens = []
##for t in tweets:
##    tokens += [w for w in nltk.sent_tokenize(t)]
##tokens2 =[]
##
##tokens2 = [nltk.tokenize.word_tokenize(s) for s in tokens]
##pos_tagged_tokens = [nltk.pos_tag(t) for t in tokens2]

##databases = [line.strip() for line in open('C:\Documents and Settings\Luke\Desktop\growth_scout\growthscout_test.txt', 'r')]

#single search for testing bugs
link = 'amazonpayments'

#couchdb connection
server = couchdb.Server('http://localhost:5984')

TIMELINE_NAME = 'search'
data = 'tweets_%s_timeline' % (TIMELINE_NAME, )
HANDLE = link
DB = '%s_%s' % (data, HANDLE)
db = server[DB]

#Get databases
doc_ids = []
for docid in db:
    if (len(docid) == 32):
        doc_ids.append(docid)


#Search tweets are dumped in couchdb and indexed in a list format 1,2,3,...
#Get Tweet couchdb ids, the index number it is in the tweetlist and the text from each database.
#this allows you to put any metadata added back in the original place
tweettuple = []
for i in range(len(doc_ids)):
    doc =  db.get(doc_ids[i])
    try:
        tweets = doc['results']
        for j in range(len(tweets)):
            tweetstext = tweets[j]['text']
            tweettuple.append((str(doc_ids[i]), j, tweetstext.encode('ascii','ignore')))
    except:
        continue

#declare important and unimporant extraction words
addwords = ['more', 'better', 'most', 'least', 'less', 'best']
stopwords1 = nltk.corpus.stopwords.words('english') +['.', ',', '--', '\'s', '?',')','(', ':','\'','\'re', '"', '-', '}', '{', ]
stopwords = list(set(stopwords1) - set(addwords))


def extractchunk(tweettuple):
    #Break each tweet into groups of sentences and words
    #Run through the nltk standard pos tag and chunker functions

    sentences = [nltk.tokenize.sent_tokenize(nltk.clean_html(str(c))) for (a,w,c) in tweettuple]
    cid = [str(a) for (a,w, c) in tweettuple]
    tnum =[w for (a,w,c) in tweettuple]
    tokens = [nltk.tokenize.word_tokenize(str(s)) for s in sentences]
    pos_tagged_tokens = [nltk.pos_tag(t) for t in tokens]
    ne_chunks = nltk.batch_ne_chunk(pos_tagged_tokens)
    return zip(cid, tnum, ne_chunks)


tweet_chunk = extractchunk(tweettuple)

# Conditions tags or words or phrases
# chunker rules. Extracts {entity1,(0-3 words in between), comparison,(0 to 3 words in between), entity2}
# comparison grammar pattern
grammar = r"""
   NP: {<DT|JJ><NN.*>}
   CP : {<DT|JJ><JJR|JJS|RBR|RBS>+}
   VB : }<VB.*>{
  """

cp = nltk.RegexpParser(grammar, loop=3)

# word pattern and tag patterns
compwords = ['more', 'less', 'most', 'least']
comptags = ['JJR', 'RBR', 'JJS', 'RBS']
loctags = ['LOCATION', 'GPE']
pricetags = ['MONEY', 'PERCENT']
companytags = ['ORGANIZATION', 'BUSINESS']
facilitytags = ['FACILITY']
timetags = ['DATE', 'TIME']
peopletags = ['PERSON']

#compile the comparison patterns
pattern = "(?:%s)" % "|".join(map(re.escape, comptags))
pattern = re.compile(pattern)

#Comparison Sentence Extractor
def extractComp(tweet_chunk):
    comparison = []
    ne_chunks1 = [c for (a,w,c) in tweet_chunk]
    cid = [str(a) for (a,w, c) in tweet_chunk]
    tnum =[w for (a,w,c) in tweet_chunk]

    for i in range(len(ne_chunks1)):
        #break the tree into comparison chunks
        tree = cp.parse(ne_chunks1[i])
        for subtree in tree.subtrees():
            try:
                subtags = [pos for (word, pos) in ne_chunks1[i].leaves() if (len(pos) >1)]
            except:
                continue
            #Create lists of test patterns
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

comp_sent = []
comp_sent = extractComp(tweet_chunk)

comp_ids = [a for (a,b,c) in comp_sent]
cnum = [b for (a,b,c) in comp_sent]
sent_class = [c for (a,b,c) in comp_sent]

#update database with comparison clasification
##for i in range(len(comp_ids)):
##    try:
##        if(sent_class[i] == 'COMP'):
##            doc = db.get(comp_ids[i])
##            doc['results'][cnum[i]]['sentence_type'] = sent_class[i]
##            db.save(doc)
##    except:
##        print 'error in sentence-type update'
##        continue

#Extract Location Information. Expand to store facilities and devices
def extractLocation(tweet_chunk):
    comparison = []

    ne_chunks1 = [c for (a,w,c) in tweet_chunk]
    cid = [str(a) for (a,w, c) in tweet_chunk]
    tnum =[w for (a,w,c) in tweet_chunk]

    pattern2 = "(?:%s)" % "|".join(map(re.escape, loctags))
    pattern2 = re.compile(pattern2)

    for i in range(len(ne_chunks1)):
        subtest = [x for x in ne_chunks1[i] if pattern2.search((str(x)))]
        if (len(subtest) > 0):
                try:
                    comparison[cid[i]] = 'LOCATION'
                except:
                    continue
    return zip(cid, tnum, comparison)

##loc_sent = []
##loc_sent = extractLocation(tweet_chunk)
##
##loc_ids = [a for (a,b,c) in loc_sent]
##cnum2 = [b for (a,b,c) in loc_sent]
##loc_class = [c for (a,b,c) in loc_sent]
##

#Update CouchDB with locations
##for i in range(len(loc_ids)):
##    try:
##        if(loc_sent[i] == 'LOCATION'):
##            doc = db.get(loc_ids[i])
##            doc['results'][cnum2[i]]['location_type'] = loc_class[i]
##            db.save(doc)
##    except:
##        print 'error in location update'
##        continue

#Extract Price Information(percents or currency). Expand to resource usage.
def extractPrice(tweet_chunk):
    comparison = []

    ne_chunks1 = [c for (a,w,c) in tweet_chunk]
    cid = [str(a) for (a,w, c) in tweet_chunk]
    tnum =[w for (a,w,c) in tweet_chunk]


    pattern3 = "(?:%s)" % "|".join(map(re.escape, pricetags))
    pattern3 = re.compile(pattern3)

    for i in range(len(ne_chunks1)):
        subtest = [x for x in ne_chunks1[i] if pattern3.search((str(x)))]
        if (len(subtest) > 0):
                try:
                    comparison[cid[i]] = 'PRICE'
                except:
                    continue
    return zip(cid, tnum, comparison)

##price_sent =[]
##price_sent = extractPrice(tweet_chunk)
##
##price_ids = [a for (a,b,c) in price_sent]
##cnum3 = [b for (a,b,c) in pric_sent]
##price_class = [c for (a,b,c) in price_sent]
##
###Update CouchDB with locations
##for i in range(len(price_ids)):
##    try:
##        if(price_sent[i] == 'PRICE'):
##            doc = db.get(price_ids[i])
##            doc['results'][cnum3[i]]['price_type'] = price_class[i]
##            db.save(doc)
##    except:
##        print 'price update error'
##        continue

def similarTweet(tweet_chunk):

    words_tags =[]
    ne_chunks1 = [c for (a,w,c) in tweet_chunk]
    cid = [str(a) for (a,w, c) in tweet_chunk]
    tnum =[w for (a,w,c) in tweet_chunk]

    for i in range(len(ne_chunks1)):
        try:
            subtags = [pos for (word, pos) in ne_chunks1[i].leaves() if (len(pos) >1)]
        except:
            continue
        subwords1 = [word for (word,pos) in ne_chunks1[i].leaves() if (len(word) >1)]
        subtest = [x for x in subtags if pattern.search(str(x))]
        # store info for recommendation program that filter's out non-essential tags and words
        filtertags1 = [pos for pos in subtags if pos in comptags]
        try:
            filterwords1 = [w.lower() for w in subwords1 if (w not in stopwords)]
        except:
            continue
        recWords =[]
        for word in filterwords1:
            recWords.append(word)
        for tag in filtertags1:
            recWords.append(tag)
        words_tags.insert(i, recWords)
    return zip(cid, tnum, words_tags)

##words_tags_data =[]
##words_tags_data = similarTweet(tweet_chunk)
##
##comp_ids4 = [a for (a,b,c) in words_tags_data]
##cnum4 = [b for (a,b,c) in words_tags_data]
##words_tags4 = [c for (a,b,c) in words_tags_data]
##
##for adoc in comp_ids4:
##    try:
##        doc = db.get(comp_ids4[i])
##        doc['results'][cnum4[i]]['words_tags_data'] = words_tags4[i]
##        db.save(doc)
##    except:
##        print 'error in words_tags_data update'
##        continue
