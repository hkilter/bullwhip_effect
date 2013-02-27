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


server2 = couchdb.Server('https://leavesof3.iriscouch.com/')
db2 = server2['green_bananas']

doc_ids = []
for docid in db:
    eml = db.get(docid)
    doc_ids.append(eml)

##for adoc in doc_ids:
##    db2.update(adoc, all_or_nothing=True)

#check for duplicated documents

if __name__ == '__main__':
    main()
