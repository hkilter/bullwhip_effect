#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      Luke
#
# Created:     03/12/2012
# Copyright:   (c) Luke 2012
# Licence:     <your licence>
#-------------------------------------------------------------------------------
#!/usr/bin/env python

import couchdb
import recognition_heuristic
import MySQLdb
import get__weather_data

def main():
    pass

server = couchdb.Server('http://localhost:5984')
DB = 'test'
db = server[DB]

#read database and get objects

##tweet_features = db.view('objects/docid_list_objects')
##for r in tweet_features:
##    if(len(r.value) > 1):
##        try:
##            for r in tweet_features:
##                features.append(r.value)
##        except:
##            continue

classifier = recognition_heuristic.naivebayes(recognition_heuristic.getwords)

#all of California
##classifier.setdb('likely_zipcode.db')
#124 sample
classifier.setdb('test_100.db')

#List operations: for i in length of features classify
##classifier.classify(tweet_features[i])

#single test
location_text = 'Beverly Hills'
classified_zipcode = classifier.classify('Beverly Hills')

zipcode = str(classified_zipcode[0])
confidence = str(classfied_zipcode[1])

#query MYSQL database and append to python list
db = MySQLdb('')
cur = db.cursor()
cur.execute("SELECT latitude,longitude FROM sqlbook.zipcounty WHERE zipcode = %s", zipcode)
rows = cur.fetchall()
latitude = rows[0][0]
longitude = rows[0][1]

likely_zipcode = {"location_text": location_text, "zipcode": zipcode, "latitude": latitude, "longitude": longitude}
weather = get__weather_data.getWeather(likely_zipcode['zipcode'])

likely_zipcode.update(weather)
print likely_zipcode

#if not close enough
#select 10 close locations to the one classified.

cur.execute("""SELECT z.zipcode, z.state, zco.poname, distcirc, population, hh,
       hhmedincome, z.latitude, z.longitude
FROM (SELECT zips.*,
             ACOS(COS(comp.latrad)*COS(zips.latrad)*
                                   COS(comp.longrad - zips.longrad) +
                  SIN(comp.latrad)*SIN(zips.latrad))*radius as distcirc
      FROM (SELECT zc.*, latitude*PI()/180 as latrad,
                   longitude*PI()/180 as longrad, 3949.9 as radius
            FROM zipcensus zc) zips CROSS JOIN
           (SELECT zc.*, latitude*PI()/180 as latrad,
                   longitude*PI()/180 as longrad
            FROM zipcensus zc
            WHERE zipcode IN (%s)) comp) z LEFT OUTER JOIN
       zipcounty zco
      ON z.zipcode = zco.zipcode
WHERE distcirc < 8
ORDER BY distcirc""", zipcode)

query2 = []
rows = cur.fetchall()
for row in rows:
    query2.append(row)

top_ten = []
#specific to this query
for i in range(0, len(query2)):
    if(i < 11):
        temp_dic = {"city": query2[i][2], "zipcode": query2[i][0], "match_latitude":query2[i][7], "match_longitude": query2[i][8]}
        top_ten.append(temp_dic)
    else:
        break


#display choices on a map and let user pick the best


cur.close()
db.close()

if __name__ == '__main__':
    main()
