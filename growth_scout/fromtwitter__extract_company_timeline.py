#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      Luke
#
# Created:     24/07/2012
# Copyright:   (c) Luke 2012
# Licence:     <your licence>
#-------------------------------------------------------------------------------
#!/usr/bin/env python

import sys
import time
import twitter
import couchdb
from couchdb.design import ViewDefinition
from twitter__login import login
from twitter__util import makeTwitterRequest



##if len(sys.argv) < 2 or sys.argv[1] not in ('public', 'home', 'user'):
##    usage()
##if len(sys.argv) > 2 and not sys.argv[2].isdigit():
##    usage()
##if len(sys.argv) > 3 and sys.argv[1] != 'user':
##    usage()

# a loop that loops over and extracts a list of files
permalinks = [line.strip() for line in open('C:\Documents and Settings\Luke\Desktop\growth_scout\growthscout_test.txt', 'r')]

#probably need to add some error handling try: except
#as amazon broke the requestor

# Need to add the list of twitter accounts
# probably have to run it on the cloud(EC2)
# and save it on the cloud(S3)
#needs to loop over the list of users and create a timeline about them
#probably should store it on iris becuase this could get big

links = ['amazon']
#add list comprehesion.lower() to all screenames

for link in links:
    TIMELINE_NAME = 'user'
    MAX_PAGES = 2
    USER = link
    KW = { # For the Twitter API call
    'count': 200,
    'skip_users': 'true',
    'include_entities': 'true',
    'since_id': 1,}
    if TIMELINE_NAME == 'user':
        USER = link
        KW['id'] = USER # id or screen name
    if TIMELINE_NAME == 'home' and MAX_PAGES > 4:
        MAX_PAGES = 4
    if TIMELINE_NAME == 'user' and MAX_PAGES > 16:
        MAX_PAGES = 16
    if TIMELINE_NAME == 'public':
        MAX_PAGES = 1

        def usage():
            print 'Usage: $ %s timeline_name [max_pages] [user]' % (link, )
            print
            print '\ttimeline_name in [public, home, user]'
            print '\t0 < max_pages <= 16 for timeline_name in [home, user]'
            print '\tmax_pages == 1 for timeline_name == public'
            print 'Notes:'
            print '\t* ~800 statuses are available from the home timeline.'
            print '\t* ~3200 statuses are available from the user timeline.'
            print '\t* The public timeline updates once every 60 secs and returns 20 statuses.'
            print '\t* See the streaming/search API for additional options to harvest tweets.'
            exit()

    t = login()
    server = couchdb.Server('http://localhost:5984')
    DB = 'tweets_%s_timeline' % (TIMELINE_NAME, )
    if USER:
        DB = '%s_%s' % (DB, USER)
    try:
        db = server.create(DB)
    except couchdb.http.PreconditionFailed, e:
    # Already exists, so append to it, keeping in mind that duplicates could occur
        db = server[DB]
        # Try to avoid appending duplicate data into the system by only retrieving tweets
        # newer than the ones already in the system. A trivial mapper/reducer combination
        # allows us to pull out the max tweet id which guards against duplicates for the
        # home and user timelines. It has no effect for the public timeline
        def idMapper(doc):
            yield (None, doc['id'])
        def maxFindingReducer(keys, values, rereduce):
            return max(values)

        view = ViewDefinition('index', 'max_tweet_id', idMapper, maxFindingReducer, language='python')
        view.sync(db)
        KW['since_id'] = int([_id for _id in db.view('index/max_tweet_id')][0].value)

    # Harvest tweets for the given timeline.
    # For friend and home timelines, the unofficial limitation is about 800 statuses although
    # other documentation may state otherwise. The public timeline only returns 20 statuses
    # and gets updated every 60 seconds.
    # See http://groups.google.com/group/twitter-development-talk/browse_thread/
    # thread/4678df70c301be43
    # Note that the count and since_id params have no effect for the public timeline

    page_num = 1
    while page_num <= MAX_PAGES:
        KW['page'] = page_num
        api_call = getattr(t.statuses, TIMELINE_NAME + '_timeline')
        tweets = makeTwitterRequest(t, api_call, **KW)
        db.update(tweets, all_or_nothing=True)
        print 'Fetched %i tweets' % len(tweets)
        page_num += 1



