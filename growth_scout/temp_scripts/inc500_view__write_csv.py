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
years = ['2006', '2007', '2008', '2009', '2010', '2011', '2012']
test = ['2006']

for year in test:
    try:
        server = server = couchdb.Server('http://lotterblad:kriby326@leavesof3.iriscouch.com')
        DB = 'inc500_%s' % (year)
        db = server[DB]

        #returns the keys and values from couch db view
        view_cat = 'company'
        view_type = 'all_stats'

        database_view = '%s/%s' % (view_cat, view_type)
        company_view = db.view(database_view)
        doc = 'C:\Documents and Settings\Luke\Desktop\\growth_scout\out\%s_%s.csv' % (DB, view_type)
        f = csv.writer(open(doc,'wb'), delimiter ='\t', quotechar='\'', quoting=csv.QUOTE_MINIMAL)
        for r in company_view:
            try:
                f.writerow([r.key, r.id, year, r.value])
            except:
                continue
    except:
        continue

if __name__ == '__main__':
    main()
