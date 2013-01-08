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

#dictionary of all of the nodes
neo_index = csv.reader(open('graph_nodes.txt'), delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

neo_dict ={}

for company in neo_index:
    neo_dict[company[0]] = int(company[1])

table = csv.reader(open('relationships.csv'), delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
next(table)

for row in table:
    try:
        #subject
        user = "%s" % (row[0])
        node_start = neo_dict[user]

        #object
        user_copied = "%s" % (row[3])
        node_end = neo_dict[user_copied]

        #predicates
        relationship = 'copy'
        rel_prop_gain = float(row[5])

        gremlin_script = "g.addEdge(g.v(%d), g.v(%d), 'copy',[gain: %d])" % (node_start, node_end, rel_prop_gain)
        gremlin.execute(gremlin_script, db)
        print "Added " + user + " copied  " + user_copied + " "+ rel_prop_gain
    except:
        print "error" + user
        continue


if __name__ == '__main__':
    main()
