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
import couchdb
import os, sys, csv

def main():
    pass

#iterative query
databases = [line.strip() for line in open('C:\Documents and Settings\Luke\Desktop\growth_scout\\cloudcomputing.txt', 'r')]

#single query
link = ['windowsazure']

for org in link:
    try:
        TIMELINE_NAME = 'search'
        HANDLE = org

##        server = couchdb.Server('https://lotterblad:kriby326@leavesof3.iriscouch.com/')
        server = couchdb.Server('http://localhost:5984/')
        DB = 'tweets_%s_timeline_%s' % (TIMELINE_NAME,HANDLE.lower())
        db = server[DB]

        #returns the keys and values from couch db view
        view_cat = 'industry'
        view_type = 'category_count'

        database_view = '%s/%s' % (view_cat, view_type)
        company_view = db.view(database_view)
        doc = 'C:\Documents and Settings\Luke\Desktop\\growth_scout\out\%s_%s.csv' % (HANDLE.lower(), view_type)
        f = csv.writer(open(doc,'wb'), delimiter =',', quotechar='\'', quoting=csv.QUOTE_MINIMAL)
        for r in company_view:
            try:
                f.writerow([r.id, r.key, r.value])
            except:
                continue
    except:
        continue
        print 'read error' + str(org)

if __name__ == '__main__':
    main()
