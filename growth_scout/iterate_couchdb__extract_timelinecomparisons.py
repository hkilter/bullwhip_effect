#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      Luke
#
# Created:     30/07/2012
# Copyright:   (c) Luke 2012
# Licence:     <your licence>
#-------------------------------------------------------------------------------
#!/usr/bin/env python

import sys
import couchdb
import nltk, re, pprint
import twitter
import simplejson as json
from string import join
from math import sqrt
from nltk.corpus import stopwords
from couchdb.design import ViewDefinition
from prettytable import PrettyTable

def main():
    pass

#read in all the files the files in the database with a given pattern


databases = [line.strip() for line in open('C:\Documents and Settings\Luke\Desktop\growth_scout\growthscout_test.txt', 'r')]

for org in databases:
    try:

        TIMELINE_NAME = 'user'
        HANDLE = org

        frequency = 1
        server = couchdb.Server('http://localhost:5984')
        DB = 'tweets_%s_timeline_%s' % (TIMELINE_NAME,HANDLE)

        db = server[DB]

        doc_ids = []
        for docid in db:
            if (len(docid) == 32):
                doc_ids.append(docid)

        #tweet tuple list
        tweettuple = []
        for adoc in doc_ids:
            try:
                doc = db.get(adoc)
                tweets = doc['text']
                tweettuple.append((str(adoc), str(tweets)))
            except:
                continue

        addwords = ['more', 'better', 'most', 'least', 'less', 'best']
        stopwords1 = nltk.corpus.stopwords.words('english') + ['.', ',', '--', '\'s', '?',')','(', ':','\'','\'re', '"', '-', '}', '{', ]
        stopwords = list(set(stopwords1) - set(addwords))

        #current rate is 70 to 140 tweets per minute

        def extractchunk(tweettuple):
            sentences = [nltk.tokenize.sent_tokenize(nltk.clean_html(str(w))) for (a,w) in tweettuple]
            cid = [str(a) for (a,w) in tweettuple]
            tokens = [nltk.tokenize.word_tokenize(str(s)) for s in sentences]
            pos_tagged_tokens = [nltk.pos_tag(t) for t in tokens]
            ne_chunks = nltk.batch_ne_chunk(pos_tagged_tokens)
            return dict(zip(cid, ne_chunks))


        tweet_chunk ={}
        tweet_chunk = extractchunk(tweettuple)

        for adoc in tweet_chunk.keys():
            doc = db.get(adoc)
            doc['comparison_pos'] = tweet_chunk[adoc]
            db.save(doc)

        grammar = r"""
               CP : {<JJR|JJS|RBR|RBS>+}
               COMP: {<NP> <.*>*<JJ.*||RB.*> <.*>*<NP>}
               """
        cp = nltk.RegexpParser(grammar, loop=3)
        comptags = ['JJR', 'RBR', 'JJS', 'RBS']
        loctags = ['LOCATION', 'GPE']
        pricetags = ['MONEY', 'PERCENT']
        companytags = ['ORGANIZATION', 'BUSINESS']
        facilitytags = ['FACILITY']
        timetags = ['DATE', 'TIME']
        peopletags = ['PERSON']

        pattern = "(?:%s)" % "|".join(map(re.escape, comptags))
        pattern = re.compile(pattern)

        #Comparision Sentence Tag Extractor
        def extractComp(tweet_chunk):
            comparison = {}
            ne_chunks1 =[value for key, value in tweet_chunk.iteritems()]
            cid = [key for key,value in tweet_chunk.iteritems()]

            for i in range(len(ne_chunks1)):
                tree = cp.parse(ne_chunks1[i])
                for subtree in tree.subtrees():
                    try:
                        subtags = [ne for (word, ne) in ne_chunks1[i].leaves() if (len(ne) >1)]
                    except:
                        continue
                    subwords = [word for (word,pos) in ne_chunks1[i].leaves() if (len(word) >1)]
                    subtest = [x for x in subtags if pattern.search(str(x))]
                    # Tests if tree is comparative
                    if (len(subtest) > 0 or subtree.node == 'COMP'):
                        try:
                            comparison[cid[i]] = 'COMP'
                        except:
                            continue
                    break
            return comparison

        #execute extract comparison
        comp_sent = {}
        comp_sent = extractComp(tweet_chunk)

        for adoc in comp_sent.keys():
            doc = db.get(adoc)
            try:
                doc['sentence_type'] = comp_sent[adoc]
                #update database
                db.save(doc)
            except:
                print 'comp_sent error'
                continue

        #Extract Location Information. Expand to store facilities and devices
        def extractLocation(tweet_chunk):
            comparison = {}
            ne_chunks1 =[value for key, value in tweet_chunk.iteritems()]
            cid = [key for key,value in tweet_chunk.iteritems()]
            pattern2 = "(?:%s)" % "|".join(map(re.escape, loctags))
            pattern2 = re.compile(pattern2)

            for i in range(len(ne_chunks1)):
                subtest = [x for x in ne_chunks1[i] if pattern2.search((str(x)))]
                if (len(subtest) > 0):
                        try:
                            comparison[cid[i]] = 'LOCATION'
                        except:
                            continue
            return comparison

        loc_sent = {}
        loc_sent = extractLocation(tweet_chunk)

        #Update CouchDB with locations
        for adoc in loc_sent.keys():
            doc = db.get(adoc)
            try:
                doc['location_type'] = loc_sent[adoc]
                #update database
                db.save(doc)
            except:
                print 'error' + str(adoc)
                continue

        #Extract Price Information(percents or currency). Expand to resource usage.
        def extractPrice(tweet_chunk):
            comparison = {}
            ne_chunks1 =[value for key, value in tweet_chunk.iteritems()]
            cid = [key for key,value in tweet_chunk.iteritems()]
            pattern3 = "(?:%s)" % "|".join(map(re.escape, pricetags))
            pattern3 = re.compile(pattern3)

            for i in range(len(ne_chunks1)):
                subtest = [x for x in ne_chunks1[i] if pattern3.search((str(x)))]
                if (len(subtest) > 0):
                        try:
                            comparison[cid[i]] = 'PRICE'
                        except:
                            continue
            return comparison

        price_sent ={}
        price_sent = extractPrice(tweet_chunk)

        for adoc in price_sent.keys():
            doc = db.get(adoc)
            try:
                doc['price_type'] = price_sent[adoc]
                #update database
                db.save(doc)
            except:
                print "error on doc\t" + str(adoc)

        #Recommendations System Data. Creates a dictionary of critical words and tags for classification and ranking tasks later.
        recommend = {}

        def similarTweet(tweet_chunk):

            ne_chunks1 =[value for key, value in tweet_chunk.iteritems()]
            cid = [key for key,value in tweet_chunk.iteritems()]

            #loop counter initialization
            count1 = 0

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
                recWords ={}
                recTags ={}
                for word in filterwords1:
                    recWords[word] = recWords.get(word,0)+1
                for tag in filtertags1:
                    recTags[tag] = recTags.get(tag,0) +1
                words_tags = dict(recTags.items() + recWords.items())
                recommend[cid[i]] = words_tags
            return recommend

        words_tags_data ={}
        words_tags_data = similarTweet(tweet_chunk)

        for adoc in words_tags_data.keys():
            try:
                doc = db.get(adoc)
                doc['words_tags_data'] = words_tags_data[adoc]
                db.save(doc)
            except:
                print 'error in words_tags_data update'
                continue
    except:
        print 'database error' + str(DB)


#need to lowercase all words, delete punctuation and fix keys

if __name__ == '__main__':
    main()
