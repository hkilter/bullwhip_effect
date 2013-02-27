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

import csv, couchdb, os, string
import simplejson as json

def main():
    pass

#change path to present working directory
os.chdir('C:\Documents and Settings\Luke\Desktop\growth_scout\\test_scripts')

#connect to couchdb
server = couchdb.Server('http://localhost:5984')
db = server['jobtobedone1']

#Get the doc_ids
##doc_ids = []
##for docid in db:
##    if (len(docid) == 32):
##        doc_ids.append(docid)

json_data = open('business_model_text2.jl')

model_list = []
for line in json_data:
    data = json.loads(line)
    model_list.append(data)

value_test =[]
model_test =[]
for i in range(len(model_list)):
    model_key = model_list[i].keys()
    model_key1 = ' '.join(model_key)
    model_test.append(model_key1)

    model_value = model_list[i].values()
    model_value1 = ' '.join(model_value[0])
    value_test.append(model_value1)

for i in range(len(model_test)):
    print model_test[i] + '\t' + value_test[i]
##doc_test =[] #testing doc
##for adoc in doc_ids:
##    doc = db.get(adoc)
##    permalink = doc['permalink']
##    if(permalink in model_test):
##        #update that doc with the text data
##        i = model_test.index(permalink)
##        doc['business_model'] = value_test[i]
##        print adoc
##        doc_test.append(doc)

if __name__ == '__main__':
    main()
