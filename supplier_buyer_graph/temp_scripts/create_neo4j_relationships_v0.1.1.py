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
db = neo4j.GraphDatabaseService("http://ec2-23-20-102-175.compute-1.amazonaws.com:7474/db/data/")

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
        user_sells = row[12]
        user_buys = row[13]

        #predicates
        #may be plural
        supplier_to = 'supply_type'
        buyer_of = 'buyer_type'

        #create lists from csv
        reader = csv.reader([user_sells], delimiter=',',skipinitialspace=True)
        for r in reader:
            seller_list = r

        reader2 = csv.reader([user_buys], delimiter=',',skipinitialspace=True)
        for r in reader2:
            buyer_list = r


        #simulation of relationships

            #make true/false nodes
            #b2b
            #b2c
            #every_strategy
            #every_role
##            b = db.get_node(enode)
##            temp_dict = b.get_properties()
##            name = temp_dict['name']

            #get the properties of the starting node
            #get the properties of the ending node
            #case or if/then add_link

        #execution script
        for buyer in seller_list:
            node_end = neo_dict[buyer]
            gremlin_script = "g.addEdge(g.v(%s),g.v(%s), 'supply_type', [name: '%s'])" % (node_start, node_end, buyer)
            print gremlin_script
            gremlin.execute(gremlin_script, db)


        for seller in buyer_list:
            node_end = neo_dict[seller]
            gremlin_script2 = "g.addEdge(g.v(%s), g.v(%s), 'buyer_type', [name: '%s']) " % (node_start, node_end, seller)
            print gremlin_script2
            gremlin.execute(gremlin_script2, db)

        #gremlin.execute(gremlin_script, db)

    except:
        print "error" + user
        continue


if __name__ == '__main__':
    main()
