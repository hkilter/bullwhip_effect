#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      Luke
#
# Created:     12/11/2012
# Copyright:   (c) Luke 2012
# Licence:     <your licence>
#-------------------------------------------------------------------------------
#!/usr/bin/env python

from py2neo import neo4j
from py2neo import gremlin
import csv, os
import simplejson as json

def main():
    pass

#change to present working directory
os.chdir('C:\Documents and Settings\Luke\Desktop\supplier_buyer_graph')

#database connection
db = neo4j.GraphDatabaseService("http://ec2-23-23-59-121.compute-1.amazonaws.com:7474/db/data")

table = csv.reader(open('relationships.csv'), delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

#get the relationships from couchdb or csv
#loop over the list and add relationships

next(table)

for row in table:
    company = "%s" % (row[0])
    neo_dict = {"name": company}
    try:
        db.create(neo_dict)
        print neo_dict
    except rest.NoResponse:
        print "Cannot connect to host"
    except rest.ResourceNotFound:
        print "Database service not found"

if __name__ == '__main__':
    main()
