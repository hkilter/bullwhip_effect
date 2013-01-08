#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      Luke
#
# Created:     05/12/2012
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
os.chdir('C:\Documents and Settings\Luke\Desktop\Pilot_Neo4j')

#database connection
db = neo4j.GraphDatabaseService("http://ec2-23-20-102-175.compute-1.amazonaws.com:7474/db/data")

#count_nodes = db.get_node_count()
neo_dict = {}
temp_dict = {}

for enode in range(0, 118):
    try:
        b = db.get_node(enode)
        temp_dict = b.get_properties()
        name = temp_dict['name']
        neo_dict[name] = enode
        strategy = temp_dict['strategy_name']
        print str(enode) + '\t' + strategy
    except:
        continue


if __name__ == '__main__':
    main()
