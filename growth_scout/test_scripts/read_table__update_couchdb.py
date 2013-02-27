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

import csv, couchdb, os, re
import simplejson as json

def main():
    pass

server = couchdb.Server('http://localhost:5984')
db = server['jobtobedone1']
server2 = couchdb.Server('https://leavesof3.iriscouch.com:6984')
db2 = server2['green_bananas']

#change path to present working directory
os.chdir('C:\Documents and Settings\Luke\Desktop\growth_scout\\test_scripts')

table = csv.reader(open('copy_trader_virtual_open_positions.csv'), delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
##json_data = open('revenue_list.jl')
##model_list = []
##for line in json_data:
##    data = json.loads(line)
##    model_list.append(data)

next(table)

for row in table:
    jobtobedone1_doc_id = row[0]
    py_dictionary = row[1]
    doc = db.get(jobtobedone1_doc_id)
    #converts dictionary to json
    j = re.sub(r"[u]", r'', py_dictionary)
    j = j.replace('\'', '"')
    revenue = json.loads(j)
    try:
        doc['revenue'] = revenue
    except:
        continue
    print doc
    db.save(doc)
##    db2.save(doc)


if __name__ == '__main__':
    main()
