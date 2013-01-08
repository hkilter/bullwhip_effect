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
os.chdir('C:\Documents and Settings\Luke\Desktop\Pilot_Neo4j\Create')

#database connection
db = neo4j.GraphDatabaseService("http://ec2-23-22-148-112.compute-1.amazonaws.com:7474/db/data/")

#create relationships between traders
table = csv.reader(open('neo4j_trader_stats.csv'), delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
next(table)

for row in table:
    try:
        #subject
        user = "%s" % (row[0])
        node_start = int(row[1])

        #objects
        num_trades = int(row[3])
        standard_dev = float(row[5])
        gain_100 = float(row[6])
        risk_group = "%s" % (row[7])

        gremlin_script = "g.v(%s)._().sideEffect{it.number_of_trades=%d; it.stddev=%d;it.gain_100=%d;risk_group='%s';}" % (node_start, num_trades,standard_dev, gain_100,risk_group)

        gremlin.execute(gremlin_script, db)
        print "Added " + user + " " + risk_group
    except:
        print "error" + user
        continue


if __name__ == '__main__':
    main()
