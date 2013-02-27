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

#change path to present working directory
os.chdir('C:\Documents and Settings\Luke\Desktop\growth_scout\\test_scripts')

table = csv.reader(open('business_model.csv'), delimiter=',')
##table2 = csv.reader(open('jobtobedone1_id_name_twitter.csv'), delimiter='\t')

next(table)

for row in table:
    jobtobedone_doc_id = row[0]
    bm_text = row[6]
    if(len(jobtobedone_doc_id) == 32):
        doc = db.get(jobtobedone_doc_id)
        #initiate objects. make sure to shutdown when updating
        try:
            doc['business_model_text']= bm_text
            db.save(doc)
            print(doc)
##                except:
##                    print 'comp_sent error'
##                    continue
        except:
            continue






if __name__ == '__main__':
    main()
