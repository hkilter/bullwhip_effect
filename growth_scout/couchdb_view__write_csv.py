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
import os, sys, csv

def main():
    pass

server = couchdb.Server('http://localhost:5984')
DB = 'tweets_search_timeline_artshub'
db = server[DB]

#returns the keys and values from couch db view
view_cat = 'tweet'
view_type = 'all_tweets'

database_view = '%s/%s' % (view_cat, view_type)
company_view = db.view(database_view)
doc = 'C:\Documents and Settings\Luke\Desktop\\growth_scout\out\%s_%s.csv' % (DB, view_cat)
f = csv.writer(open(doc,'wb'), delimiter =',', quotechar='\'', quoting=csv.QUOTE_MINIMAL)
for r in company_view:
    try:
        f.writerow([r.key, r.value])
    except:
        continue

if __name__ == '__main__':
    main()
