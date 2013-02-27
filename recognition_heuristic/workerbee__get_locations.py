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
from py2neo import neo4j
from py2neo import gremlin

databases = ['closure']

for org in databases:
    try:
        TIMELINE_NAME = 'search'
        HANDLE = org

        server = couchdb.Server('http://localhost:5984')
        DB = 'tweets_%s_%s' % (TIMELINE_NAME,HANDLE)
        db = server[DB]
        doc_ids = []
        for docid in db:
            if (len(docid) == 32):
                doc_ids.append(docid)
        #couchdb searchtimeline extractor

        #tweet tuple list
        tweettuple = []

        for i in range(len(doc_ids)):
            doc = db.get(doc_ids[i])
            try:
                tweets = doc['results']
                for j in range(len(tweets)):
                    tweetstext = tweets[j]['text']
                    tweettuple.append((str(doc_ids[i]), j, tweetstext.encode('ascii','ignore')))
            except:
                continue


        addwords = ['more', 'better', 'most', 'least', 'less', 'best']
        stopwords1 = nltk.corpus.stopwords.words('english') +['.', ',', '--', '\'s', '?',')','(', ':','\'','\'re', '"', '-', '}', '{', ]
        stopwords = list(set(stopwords1) - set(addwords))

        #from each tweet extract chunks
        def extractchunk(tweettuple):
            sentences = [nltk.tokenize.sent_tokenize(nltk.clean_html(str(c))) for (a,w,c) in tweettuple]
            cid = [str(a) for (a,w, c) in tweettuple]
            tnum =[w for (a,w,c) in tweettuple]
            tokens = [nltk.tokenize.word_tokenize(str(s)) for s in sentences]
            pos_tagged_tokens = [nltk.pos_tag(t) for t in tokens]
            ne_chunks = nltk.batch_ne_chunk(pos_tagged_tokens)
            return zip(cid, tnum, ne_chunks)

        tweet_chunk = extractchunk(tweettuple)

        # Conditions tags or words or phrases
        #first reasonable chunker. Extracts {entity1,(0-3 words in between), comparison,(0 to 3 words in between), entity2}
        # comparison grammar pattern
        grammar = r"""
          NP: {<DT|CD>?<NNP|NNS>+}
          LINK: {<IN><CC.*>?<IN>*}
          EVENT: {<MD>+<VB.*>*<RB.*>?}
          """

        chunkparser = nltk.RegexpParser(grammar, loop=3)

        #sub-leaves functions gets tagged trees of parsed sentence that meet the condition passed
        def sub_leaves(tree, node):
            return [t.leaves() for t in tree.subtrees (lambda s: s.node == node)]

        # word pattern and/or tag mining patterns NP =  programmer defined noun  phrase
        #object mapper
        loctags = ['LOCATION', 'GPE','ORGANIZATION', 'BUSINESS','PERSON','FACILITY', 'DATE', 'TIME', 'NP']

        pattern2 = "(?:%s)" % "|".join(map(re.escape, loctags))
        pattern2 = re.compile(pattern2)

        #relational mapper
        linktags = ['IN', 'CC']
        pattern3 = "(?:%s)" % "|".join(map(re.escape, linktags))
        pattern3 = re.compile(pattern3)

        #Extract Location Information. Expand to store facilities and devices
        #store the entities and the links in the order they come in
        def extractLinks(tweet_chunk, subject):
            tweet_objects = []
            relationships = []

            entity_chunks = [c for (a,w,c) in tweet_chunk]
            couch_id = [str(a) for (a,w, c) in tweet_chunk]
            tweet_number =[w for (a,w,c) in tweet_chunk]

            for i in range(len(entity_chunks)):
                tree = chunkparser.parse(entity_chunks[i])
                #get objects
                tweet_objects1 = [x for x in tree if pattern2.search((str(x)))]
                #get relationships
                tweet_links = sub_leaves(tree, 'EVENT') + sub_leaves(tree, 'LINK')
                tweet_objects.append(tweet_objects1)
                relationships.append(tweet_links)
            return zip(couch_id, tweet_number, tweet_objects, relationships)

        #call the extract location function
        subject = "road+closure"
        sent_links = extractLinks(tweet_chunk, subject)

        #couchdb database
        db2 = server['test']
        #Update CouchDB with locations
        for i in range(0, len(sent_links)):
            objects =[]
            relationships = []
            objects.append(sent_links[i][2])
            relationships.append(sent_links[i][3])
            tweet_subject_object_relationship = {"subject": subject, "objects": objects, "relationships": relationships}
            update ={"id": sent_links[i][0], "locations": sent_links[i][1], "triplestore": tweet_subject_object_relationship}
            db2.save(update)
    except:
        print 'database error: ' + str(DB)
        continue

