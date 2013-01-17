#-------------------------------------------------------------------------------
# Name:        diffusion by analogy
# Purpose:
#
# Author:      Luke
#
# Created:     01/10/2012
# Copyright:   (c) Luke 2013
# Licence:      GPL
#-------------------------------------------------------------------------------
#!/usr/bin/env python

import MySQLdb
import recognition_heuristic2

def main():
    pass

#input text, output scores 1 to 5 on each of Rogers categories

#classification
classifier = recognition_heuristic2.naivebayes(recognition_heuristic2.getwords)
classifier.setdb('seller_adopter_text.db')

#how to use the classifier
#classified_item = classifier.classify("some text")

#Query the MYSQL database and append to python dictionary
db = MySQLdb.connect(host='localhost', user='root',db='bass_data')
cur = db.cursor()

query = {}
for item in range(1,44):
    cur.execute("SELECT name, p_data, q_data FROM bass_data.historical WHERE idhistorical= %s", item)
    rows = cur.fetchall()
    #append all the names to a list
    for row in rows:
        name = str(row[0])
        subquery = {name : {"p_data": row[1], "q_data":row[2]}}
    query.update(subquery)

cur.close()
db.close()

if __name__ == '__main__':
    main()
