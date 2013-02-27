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
import string

def main():
    pass

os.chdir('C:\Documents and Settings\Luke\Desktop\\green_banana_citations\\test')
permlinks = [line.split() for line in open('couchdb_greenbananas_testdocs.txt', 'r')]

permalinks =[]
for link in permlinks:
    doc1= ' '.join(link)
    permalinks.append(doc1)

server = couchdb.Server('http://localhost:5984')
db = server['jobtobedone1']

#Get the doc_ids
##doc_ids = []
##for docid in db:
##    if (len(docid) == 32):
##        doc_ids.append(docid)

##table2 = csv.reader(open('jobtobedone1_id_name_twitter.csv'), delimiter='\t')

for adoc in permalinks:
##    adoc1= ' '.join(adoc)
    doc = db.get(adoc)
    check = doc['permalink']
    revenue = doc['revenue']
    funding = doc[]

##    overview = doc['overview']
##    if(doc['revenue']):
##        revenue = doc['revenue']
##    else:
##        revenue = 0
    result = [i for i in permalinks if i in check]
    if (len(result)> 1):
        print adoc + '\t' + str(check)
    else:
        continue
        #initiate objects. make sure to shutdown when updating
##        try:
##            if(doc['offices'][0]['state_code'] == state):
##    ##        doc['revenue']=''
##    ##        doc['growth_multiple']=''
##                try:
##                    if (len(doc['revenue']) > 0 ):
##                        extra = {row[2] : row[4]}
##                        doc['revenue'].update(extra)
##                        extra2 = {row[2] : row[9]}
##                        doc['growth_multiple'].update(extra2)
##                    else:
##                        doc['revenue'] = {row[2] : row[4]}
##                        doc['inc_url'] = str(row[5])
##                        doc['growth_multiple']= {row[2] : row[9]}
##                        #update database
####                    print str(doc['revenue']) + doc['permalink']+ str(doc['growth_multiple'])
##                    db.save(doc)
##                except:
##                    print 'comp_sent error'
##                    continue
##        except:
##            continue






if __name__ == '__main__':
    main()
