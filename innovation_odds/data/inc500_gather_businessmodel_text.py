#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      Luke
#
# Created:     29/08/2012
# Copyright:   (c) Luke 2012
# Licence:     <your licence>
#-------------------------------------------------------------------------------
#!/usr/bin/env python

import urllib2, couchdb, os
import simplejson as json
from scrapy.selector import HtmlXPathSelector
from scrapy.http import HtmlResponse
from string import join

def main():
    pass


#change path to present working directory
os.chdir('C:\Documents and Settings\Luke\Desktop\growth_scout')


permalinks = [line.strip() for line in open('C:\Documents and Settings\Luke\Desktop\growth_scout\growthscout_test.txt', 'r')]
##table = csv.reader(open('inc.csv'), delimiter=',')
##table2 = csv.reader(open('jobtobedone1_id_name_twitter.csv'), delimiter='\t')

##next(table)

permalink_list = []

##for row in table:
##    jobtobedone_doc_id = row[11]
##    permalink  = row[6]
##    if(len(jobtobedone_doc_id) == 32):
##        permalink_list.append(permalink)

# save all the json objects to couchdb
server = couchdb.Server('http://lotterblad:kriby326@leavesof3.iriscouch.com')
db = server['inc500_test']

#dictionary of permalinks/doc_ids

# loop over the list fetching all json objects. Then save to couchdb
j = 0
for link in permalinks:
    items = {}
    URL = 'http://www.inc.com/inc5000/profile/%s' % (link)
    h = urllib2.urlopen(URL)
    response = h.read()

    html_response = HtmlResponse(URL, body=response)
    hxs = HtmlXPathSelector(html_response)
    sites = hxs.select('//div[@class="business-model"]')
##    database = "inc500_test"
##    try:
##        db = server.create(database)
##    except couchdb.http.PreconditionFailed, e:
##        # Already exists, so append to it, keeping in mind that duplicates could occur
##        db = server[database]
    try:
        item = {}
        item[link] = sites.select('p[@class="business-model-text"]/text()').extract()
        line = json.dumps(item)
        print line
        items[j] = json.loads(line)
    except:
        continue
    j = j + 1






