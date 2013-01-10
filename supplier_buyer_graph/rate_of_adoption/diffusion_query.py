#-------------------------------------------------------------------------------
# Name:        module1
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

#classification
classifier = recognition_heuristic2.naivebayes(recognition_heuristic2.getwords)
classifier.setdb('seller_adopter_text.db')
#classify_item = classifier.classify("some text")

#initialize database
#
#id
id = 40

#Query the MYSQL database and append to python list
db = MySQLdb.connect(host='localhost', user='root',db='bass_data')
cur = db.cursor()
cur.execute("SELECT name, p_data, q_data FROM bass_data.historical WHERE idhistorical= %s", id)
rows = cur.fetchall()
query = []

for row in rows:
    for col in row:
        query.append(col)

cur.close()
db.close()

if __name__ == '__main__':
    main()
