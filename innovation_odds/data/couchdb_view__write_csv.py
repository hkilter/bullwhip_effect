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
DB = 'jobtobedone1'
db = server[DB]

#returns the keys and values from couch db view
view_cat = 'company'
view_type = 'revenuebyyear_foundedyear_permalink'

database_view = '%s/%s' % (view_cat, view_type)
company_view = db.view(database_view)
doc = 'C:\Documents and Settings\Luke\Desktop\\growth_scout\out\%s_%s.csv' % (DB, view_type)
f = csv.writer(open(doc,'wb'), delimiter =',', quotechar='\'', quoting=csv.QUOTE_MINIMAL)
for r in company_view:
    try:
        f.writerow([r.id, r.key, r.value])
    except:
        continue

if __name__ == '__main__':
    main()
