#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      Luke
#
# Created:     12/06/2012
# Copyright:   (c) Luke 2012
# Licence:     <your licence>
#-------------------------------------------------------------------------------
#!/usr/bin/env python

import time
import twitter, couchdb, datetime
import simplejson as json
import re, os, sys, csv, string
from couchdb.design import ViewDefinition
from twitter__login import login
from twitter__util import makeTwitterRequest

def main():
    pass

#os.chdir('C:\\Documents and Settings\\Luke\\Desktop\\basket_shoppingcart\\worker_bee\\test.txt')

#for large lists
##twitter_hashtags = [line.split() for line in open('test.txt', 'r')]

#for importing small lists
##twitter_usernames = [line.split() for line in open('cloudcomputing.txt', 'r')]
##permalinks =[]
##for i in range(0,len(twitter_usernames)):
##    list_item  = ' '.join(twitter_usernames[i])
##    permalinks.append(list_item)

##chunks=[twitter_usernames[x:x+140] for x in xrange(0, len(twitter_usernames), 140)]

#iterative list search. just bump chunks[j] to go to next section
#2011 len(chunks) =  38
##permalinks =[]
##for i in range(0,len(chunks[10])):
##     list_item  = ' '.join(chunks[10][i])
##     permalinks.append(list_item)

#single search for exceptions or hashes
links = [line.split() for line in open('test.txt', 'r')]

for link in links:
    TIMELINE_NAME = 'search'
    MAX_PAGES = 6
    try:
##        QUERY = '#%s' % (link)
##        HANDLE = link

        t = login()
        #need error handling in the case of no tweets, make sure database naming is in line with semantic ontologies

        #small sectors upload to
        server = couchdb.Server('http://localhost:5984/')

        DB = 'tweets_%s_closure' % (TIMELINE_NAME, )

##        if QUERY:
##            DB = '%s_%s' % (DB, HANDLE.lower())
        try:
            db = server.create(DB)
        except couchdb.http.PreconditionFailed, e:
        # Already exists, so append to it, keeping in mind that duplicates could occur
            db = server[DB]

        if TIMELINE_NAME == 'search':
            MAX_PAGES = 6

        twitter_search=twitter.Twitter(domain="search.twitter.com")

        search_results =[]

        #Gather what anyone is saying about company
        for page in range(1,MAX_PAGES):
            search_results.append(twitter_search.search(q="road closures", rpp=100, page=page))

        #Save the search results to the database
        s = json.dumps(search_results, sort_keys=True, indent=1)
        docs = json.loads(s)
        db.update(docs, all_or_nothing=True)
##        date = '%d.%d.%d' % (now.month, now.day, now.year)
##        time = '%d:%d' % (now.hour, now.minute)
##        datetime1 = '%s@%s' %(date, time)
##        couchid = {"_id": user}
##        neo_node = {"neo4j_node" :neo_num}
##        couchid.update(doc_time)
##        db.save(couchid)
    except:
        continue

if __name__ == '__main__':
    main()
