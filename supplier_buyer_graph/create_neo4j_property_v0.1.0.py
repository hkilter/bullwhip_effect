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
        user = row[0]
        node_start = neo_dict[user]

        #objects
        strategy_group = row[1]
        strategy_name =  row[2]
        start_year = int(row[3])
        last_year = int(row[4])
        starting_funds_millions = int(row[5])
        last_year_millions = int(row[6])
        survival_years = int(row[8])
        b2b_b2c = row[10]
        roles = row[11]

##        gremlin_script = "g.v(%s)._().sideEffect{it.strategy_group='%s';}" % (node_start, strategy_group)
##        gremlin_script2 = "g.v(%s)._().sideEffect{it.strategy_name='%s';}" % (node_start, strategy_name)
##        gremlin_script3 = "g.v(%s)._().sideEffect{it.start_year=%d;}" % (node_start, start_year)
##        gremlin_script4 = "g.v(%s)._().sideEffect{it.last_year=%d;}" % (node_start, last_year)
        gremlin_script5 = "g.v(%s)._().sideEffect{it.starting_funds_millions=%d;}" % (node_start, starting_funds_millions)
        gremlin_script6 = "g.v(%s)._().sideEffect{it.last_year_funds=%d;}" % (node_start, last_year_millions)
        gremlin_script7 = "g.v(%s)._().sideEffect{it.survival_years=%d;}" % (node_start, survival_years)
        gremlin_script8 = "g.v(%s)._().sideEffect{it.b2b_b2c='%s';}" % (node_start, b2b_b2c)
        gremlin_script9 = "g.v(%s)._().sideEffect{it.roles='%s';}" % (node_start, roles)

##        print gremlin_script
##        print gremlin_script2
##        print gremlin_script3
##        print gremlin_script4
        print gremlin_script5
        print gremlin_script6
        print gremlin_script7
        print gremlin_script8
        print gremlin_script9

##        gremlin.execute(gremlin_script, db)
##        gremlin.execute(gremlin_script2, db)
##        gremlin.execute(gremlin_script3, db)
##        gremlin.execute(gremlin_script4, db)
        gremlin.execute(gremlin_script5, db)
        gremlin.execute(gremlin_script6, db)
        gremlin.execute(gremlin_script7, db)
        gremlin.execute(gremlin_script8, db)
        gremlin.execute(gremlin_script9, db)
    except:
        print "error" + user
        continue


if __name__ == '__main__':
    main()
