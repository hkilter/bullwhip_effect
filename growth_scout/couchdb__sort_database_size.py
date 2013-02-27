#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      Luke
#
# Created:     02/09/2012
# Copyright:   (c) Luke 2012
# Licence:     <your licence>
#-------------------------------------------------------------------------------
#!/usr/bin/env python

import couchdb
import os, sys, csv

server = couchdb.Server('http://lotterblad:kriby326@leavesof3.iriscouch.com')

db_list ={}
for db in server:
    try:
        name = '%s' % (db)
        database = server[name]
        db_list[db]= couchdb.Database.info(database)
    except:
        continue

for data in db_list:
    if (db_list[data]['disk_size'] > 50000):
        print str(data) + '\t'+ str(db_list[data]['disk_size'])

