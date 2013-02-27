#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      Luke
#
# Created:     16/08/2012
# Copyright:   (c) Luke 2012
# Licence:     <your licence>
#-------------------------------------------------------------------------------
#!/usr/bin/env python

import couchdb
import simplejson as json
from string import join
from math import sqrt
from nltk.corpus import stopwords
from couchdb.design import ViewDefinition
from prettytable import PrettyTable
import fromwordcount__docclass_nnf

def main():
    pass

server = couchdb.Server('http://localhost:5984')
db = server['tweets_user_timeline_square']

doc_ids = []
for docid in db:
    doc_ids.append(docid)

def sim_pearson(prefs,p1,p2):
  # Get the list of mutually rated items
  si={}
  for item in prefs[p1]:
    if item in prefs[p2]: si[item]=1

  # if they are no ratings in common, return 0
  if len(si)==0: return 0

  # Sum calculations
  n=len(si)

  # Sums of all the preferences
  sum1=sum([prefs[p1][it] for it in si])
  sum2=sum([prefs[p2][it] for it in si])

  # Sums of the squares
  sum1Sq=sum([pow(prefs[p1][it],2) for it in si])
  sum2Sq=sum([pow(prefs[p2][it],2) for it in si])

  # Sum of the products
  pSum=sum([prefs[p1][it]*prefs[p2][it] for it in si])

  # Calculate r (Pearson score)
  num=pSum-(sum1*sum2/n)
  den=sqrt((sum1Sq-pow(sum1,2)/n)*(sum2Sq-pow(sum2,2)/n))
  if den==0: return 0

  r=num/den

  return r

# Returns the best matches for person from the prefs dictionary.
# Number of results and similarity function are optional params.

def topMatches(prefs,person,n=5,similarity=sim_pearson):
  scores=[(similarity(prefs,person,other),other)
                  for other in prefs if other!=person]
  scores.sort()
  scores.reverse()
  return scores[0:n]

#count the number of matches over a similarity threshold
##for i in range(1,len(recommend)):
##    user = 'test_user%s' % (i)
##    rating = tweet_classify_topmatches.topMatches(recommend,user, n=3)
##    if rating[0][0] > 0:
##        print user
##        print rating

##for adoc in doc_ids:
##    doc = db.get(adoc)
##    if(doc['sentence_type'] == 'COMP'):
##        for item in doc['words_tags_data'].iteritems():
##            irec[adoc] = item

def wordmatrixfeatures(x):
    return x

classifier = fromwordcount__docclass_nnf.naivebayes(wordmatrixfeatures)
classifier.setdb('C:\Documents and Settings\Luke\Desktop\growth_scout\\newtest.db')

tweet_word_count = db.view('keys/object_keys_list')
for r in tweet_word_count:
    if(len(r.value) > 1):
        try:
            classification = classifier.classify(r.value)
        except:
            continue
        print str(classification)

##classifier = fromwordcount__docclass_nnf.naivebayes(wordmatrixfeatures)
##classifier.setdb('square_test.db')

#left off at
## for adoc in doc_ids:
##display the text
#train on the dictionary(not the sentence)
##classifier.train('doc['words_tags_data'], 'strategy classification')
##if retweeted_count > some threshold

if __name__ == '__main__':
    main()
