#-------------------------------------------------------------------------------
# Name:       read_docid_print_inof
# Purpose:
#
# Author:      Luke
#
# Created:     04/09/2012
# Copyright:   (c) Luke 2012
# Licence:     GPL
#-------------------------------------------------------------------------------
#!/usr/bin/env python

import csv, couchdb, os
import simplejson as json
import string, operator

def main():
    pass

#change to the working directory and read in list of documents with revenue
os.chdir('C:\Documents and Settings\Luke\Desktop\\green_banana_citations\\test')
permlinks = [line.split() for line in open('couchdb_greenbananas_testdocs.txt', 'r')]

#format list of documents for iterating
permalinks =[]
for link in permlinks:
    doc1= ' '.join(link)
    permalinks.append(doc1)

#connect to the database
server = couchdb.Server('http://localhost:5984')
db = server['jobtobedone1']

#iterate over documents
for adoc in permalinks:
    try:
        #retrieve document attributes
        doc = db.get(adoc)
        check = doc['permalink']
        founded_year = doc['founded_year']
        revenue = doc['revenue']
        growth = doc['growth_multiple']
        employees = doc['number_of_employees']
        max_growth = max(growth.itervalues())
        year_growth= max(growth, key=growth.get)
        rev_value = max(revenue.itervalues())
        rev_year = max(revenue, key=revenue.get)
        min_value = min(revenue.itervalues())
        min_year = min(revenue, key=revenue.get)

        for key, value in revenue.iteritems():
            if (int(value) > 500000000):
                fivehundredm_revenue = 'TRUE'
                fivehundedm_value = value
            if (int(value) > 50000000):
                fiftym_revenue = 'TRUE'
                time_fiftym= int(key)-founded_year
                break
            else:
                fiftym_revenue = 'FALSE'
                time_fiftym = 'NULL'

        if((fivehundredm_revenue == 'TRUE') and time_fiftym < 8):
            green_banana = 'Group C, Banana'
        if((fivehundredm_revenue == 'TRUE') and time_fiftym < 10):
            green_banana = 'Group D, Banana'
        else:
            green_banana = ''
        if(founded_year > 2004):
            green_banana = 'Green Banana'

        #print documents
##        print adoc + '\t' +str(founded_year)+'\t' + str(check) + '\t' + str(fiftym_revenue)+ '\t' + str(time_fiftym) + '\t' + green_banana + '\t' + rev_year + '\t' + rev_value + '\t' + str(employees)
        print adoc +  '\t' + str(employees) + '\t' + str(year_growth)+ '\t' + str(max_growth)
    except:
        continue

if __name__ == '__main__':
    main()
