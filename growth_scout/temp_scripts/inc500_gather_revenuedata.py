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

import urllib2, couchdb
import simplejson as json
from scrapy.selector import HtmlXPathSelector
from scrapy.http import HtmlResponse
from string import join

def main():
    pass

years = ['2006', '2007', '2008', '2009', '2010', '2011', '2012']
states = ['AL', 'AK', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DE', 'FL', 'GA', 'HI', 'ID', 'IL', 'IN', 'IA', 'KS', 'KY', 'LA', 'ME', 'MD', 'MI', 'MN', 'MA', 'MS', 'MT', 'NH', 'NJ', 'NM', 'NY', 'NC', 'ND', 'PA', 'RI',
           'SC', 'SD', 'TN', 'TX', 'UT', 'UT', 'VT', 'VA', 'WA', 'WV', 'WI', 'WY']

year = ['2012']
state = ['MN', 'CA']

# save all the json objects to couchdb
server = couchdb.Server('http://lotterblad:kriby326@leavesof3.iriscouch.com')
db = server['inc500']

# loop over the list fetching all json objects. Then save to couchdb
for date in year:
    items = {}
    j = 0
    try:
        for abbrev in states:
            URL = 'http://www.inc.com/inc5000/list/%s/state/%s' % (date, abbrev)
            h = urllib2.urlopen(URL)
            response = h.read()

            html_response = HtmlResponse(URL, body=response)
            hxs = HtmlXPathSelector(html_response)
            sites = hxs.select('//table[@id="fulltable"]/tr[position()>1]')
            database = "inc500_%s" % (date)
            try:
                db = server.create(database)
            except couchdb.http.PreconditionFailed, e:
                # Already exists, so append to it, keeping in mind that duplicates could occur
                db = server[database]

            for i in range(len(sites)):
                try:
                    item = {}
                    company = sites[i].select('td[position()=2]/a/text()').extract()
                    item['company'] = ' '.join(company)
                    profile = sites[i].select('td[position()=2]/a/@href').extract()
                    item['profile'] = ' '.join(profile)
                    growth = sites[i].select('td[position()=3]/text()').extract()
                    item['growth'] = ' '.join(growth)
                    revenue = sites[i].select('td[position()=4]/text()').extract()
                    item['revenue']= ' '.join(revenue)
                    state = sites[i].select('td[position()=5]/text()').extract()
                    item['state'] = ' '.join(state)
                    item['rev_year']= date
                    line = json.dumps(item)
                    print line
                    items[j] = json.loads(line)
                except:
                    continue
                #database id
                j = j + 1


        db.save(items)
    except:
        continue



