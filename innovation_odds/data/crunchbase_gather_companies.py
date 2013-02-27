#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      Luke
#
# Created:     28/06/2012
# Copyright:   (c) Luke 2012
# Licence:     <your licence>
#-------------------------------------------------------------------------------
#!/usr/bin/env python

#This script downloads all the json objects from crunchbase and puts them into couchdb

import urllib
import simplejson as json
import couchdb

def main():
    pass

# save all the json objects to couchdb
server = couchdb.Server('http://2p2.iriscouch.com')
db = server['companies']

# point program at links file and pick out company permalinks


company= open('C:\Documents and Settings\Luke\Desktop\Programming\Python\py web programming\crunchbase_test.txt', 'r')
permalinks = [line.strip() for line in open('C:\Documents and Settings\Luke\Desktop\Programming\Python\py web programming\crunchbase_test.txt', 'r')]

# loop over the list fetching all json objects. Then save to couchdb
for name in permalinks:
    h = urllib.urlopen('http://api.crunchbase.com/v/1/company/%s.js' % (name))
    try:
        data = json.loads(h.read())
    except:
        continue
    if not 'name' in data:
        continue
    db.save(data)


#took about 6 hours to run(1 GB download). Alteratively you could save to a text file or run in parallel


##    f = open('C:\crunchbase_6272012', 'w')
##    for line in content:
##        try:
##            f.write('%s\n' % line)
##        except UnicodeEncodeError:
##            pass

# close my connectinos
##f.close()

if __name__ == '__main__':
    main()
