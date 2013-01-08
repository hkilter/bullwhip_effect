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
import string, os, csv
import simplejson as json

def main():
    pass

#change to present working directory
os.chdir('C:\Documents and Settings\Luke\Desktop\supplier_buyer_graph')

#database connection
db = neo4j.GraphDatabaseService("http://ec2-23-23-59-121.compute-1.amazonaws.com:7474/db/data/")

table = csv.reader(open('relationships.csv'), delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

next(table)

for row in table:
    try:
        #subject
        user = row[0]
        node_start = row[1]

        #objects
        risk_group = row[7]

        gremlin_script = "g.v(%s)._().sideEffect{it.risk_group='%s';}" % (node_start, risk_group)

        gremlin.execute(gremlin_script, db)
        #print gremlin_script
    except:
        print "error" + user
        continue


if __name__ == '__main__':
    main()
