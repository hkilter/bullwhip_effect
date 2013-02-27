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

permalinks = ['FB']

#change path to present working directory
os.chdir('C:\Documents and Settings\Luke\Desktop\growth_scout\\temp_scripts')

##table = csv.reader(open('inc.csv'), delimiter=',')
##table2 = csv.reader(open('jobtobedone1_id_name_twitter.csv'), delimiter='\t')
##
##next(table)
##
##permalink_list = []
##

##for row in table:
##    jobtobedone_doc_id = row[11]
##    soundex = row[10]
##    permalink  = row[6]
##    if((len(jobtobedone_doc_id) == 32) or (len(soundex) > 5) ):
##        permalink_list.append(permalink)

# save all the json objects to couchdb
##server = couchdb.Server('http://lotterblad:kriby326@leavesof3.iriscouch.com')
##db = server['ycharts_test']

#dictionary of permalinks/doc_ids

# loop over the list fetching all json objects. Then save to couchdb
j = 0
for link in permalinks:
    items = {}
    URL = 'http://ycharts.com/companies/%s/revenues' % (link)
    h = urllib2.urlopen(URL)
    response = h.read()

    html_response = HtmlResponse(URL, body=response)
    hxs = HtmlXPathSelector(html_response)
    sites1 = hxs.select('//div[@class="dataColLeft"]//tr')
    for row in sites1:
        row_date = row.select('//td[@class="col1"]').extract()
        print row_date
    sites2 = hxs.select('//div[@class="dataColRt"]//tr')
    for row in sites2:
        row_date = row.select('//td[@class="col1"]').extract()
        print row_date

##    database = "inc500_test"
##    try:
##        db = server.create(database)
##    except couchdb.http.PreconditionFailed, e:
##        # Already exists, so append to it, keeping in mind that duplicates could occur
##        db = server[database]
    try:
        item = []
        item.append(sites1)
        item.append(sites2)
    except:
        continue
##    j = j + 1

##db.save(items)
print(items)



