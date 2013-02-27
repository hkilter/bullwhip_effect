#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      Luke
#
# Created:     04/09/2012
# Copyright:   (c) Luke 2012
# Licence:     <your licence>
#-------------------------------------------------------------------------------
#!/usr/bin/env python

import csv, couchdb, os
import simplejson as json

def main():
    pass

server = couchdb.Server('http://localhost:5984')
db = server['jobtobedone1']
server2 = couchdb.Server('https://leavesof3.iriscouch.com:6984')
db2 = server2['green_bananas']

#change path to present working directory
os.chdir('C:\Documents and Settings\Luke\Desktop\growth_scout\\test_scripts')

table = csv.reader(open('jobtobedone1_revenuebyyear_foundedyear_permalink.csv'), delimiter='\t', quotechar='\'')

next(table)

for row in table:
    jobtobedone1_doc_id = row[0]
    revenue = row[1]
    doc = db.get(jobtobedone1_doc_id)
    s = json.dumps(revenue, sort_keys=True, indent=1)
    try:
        doc['revenue'] = str(revenue)
    except:
        continue
    docs = json.loads(doc)
    print doc['revenue']
##    db.save(doc)
    db2.save(doc)







if __name__ == '__main__':
    main()
