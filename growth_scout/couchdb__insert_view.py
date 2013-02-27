#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      Luke
#
# Created:     23/08/2012
# Copyright:   (c) Luke 2012
# Licence:     <your licence>
#-------------------------------------------------------------------------------
#!/usr/bin/env python

import couchdb
from couchdb.design import ViewDefinition

def main():
    pass

#iterative insert
databases = [line.strip() for line in open('C:\Documents and Settings\Luke\Desktop\\growth_scout\\growth_inc500_2.txt', 'r')]

#single inster
link = ['twilio']

for org in databases:
    try:
        TIMELINE_NAME = 'search'
        HANDLE = org

        server = couchdb.Server('https://lotterblad:kriby326@leavesof3.iriscouch.com/')
        DB = 'tweets_%s_timeline_%s' % (TIMELINE_NAME,HANDLE.lower())
        db = server[DB]

        comparative_tweet = """//emits all comparative tweets in document without duplicates
        var check = [];
        function(doc) {
        if(doc.results) {
           doc.results.forEach(function(tweet) {
               id = tweet.id
               if(tweet.sentence_type && (check.indexOf(id) == -1) ) {
                   emit(tweet.from_user_name, tweet.sentence_type +  ' ' + tweet.text)
                  }
              check.push(id)
             });
            }
         }"""
        all_tweets = """ //emits all comparative tweets in document without duplicates
var check = [];
        function(doc) {
        if(doc.results) {
           doc.results.forEach(function(tweet) {
               id = tweet.id
               if(tweet.id && (check.indexOf(id) == -1) ) {
                   emit(tweet.from_user_name, tweet.text)
                  }
              check.push(id)
             });
            }
         }"""

        view = ViewDefinition('tweet', 'comparative_tweet', comparative_tweet, language='javascript')
        view2 = ViewDefinition('tweet', 'all_tweets', all_tweets, language='javascript')
        #view.sync(db)
        view2.sync(db)

    except:
        continue

if __name__ == '__main__':
    main()
