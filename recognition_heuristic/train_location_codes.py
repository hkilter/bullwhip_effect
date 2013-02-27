#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      Luke
#
# Created:     04/12/2012
# Copyright:   (c) Luke 2012
# Licence:     <your licence>
#-------------------------------------------------------------------------------
#!/usr/bin/env python

import recognition_heuristic
import MySQLdb
import string

def main():
    pass

#Step 1: classify objects in some text with a likely location code

     #use on unstructured text

classifier = recognition_heuristic.naivebayes(recognition_heuristic.getwords)

    #use this function if given a dictionary or key/value structured storage of text

##classifier = recognition_heuristic.naivebayes(wordmatrixfeatures)

#Step 2: Set the database to store the training. Set the region to train

classifier.setdb('likely_zipcode.db')
state = 'CA'
#Step 3: Train the text with a location code

   #initial test training already carried out
##recognition_heuristic.frequency_train(classifier)
##recognition_heuristic.impact_train(classifier)

#Step 4: connect to a training database. The sqlbook databse contains census information on zipcodes and population

db = MySQLdb.connect(host='localhost', user='root',db='sqlbook')
cur = db.cursor()

#Step 5: Get the frequency training database. In this case: Words about a zipcode.

cur.execute("SELECT zipcode, poname, state, countyname FROM zipcounty WHERE state =%s AND zipcode < 90250;", state)
rows = cur.fetchall()
query_features = []
for row in rows:
    query_features.append(row)

#Step 6: Train the classifier by word frequency
for i in range(0, len(query_features)):
    training_text = ' '.join(query_features[i])
    location_code = query_features[i][0]
    classifier.train(training_text, location_code)

#Step 7: Get the impact training database. In this case: The population of the zicodes classified.
#the following query returns zipcode, population

cur.execute("SELECT zipcode, population FROM zipcensus WHERE state =%s and zipcode < 90250;", state)
rows = cur.fetchall()
query2 = []
for row in rows:
    query2.append(row)


#Step 8: train the impact of your classification
for i in range(0, len(query2)):
    training_category = query2[i][0]
    population = int(query2[i][1])
    classifier.impactodds(training_category, population)


cur.close()
db.close()


if __name__ == '__main__':
    main()
