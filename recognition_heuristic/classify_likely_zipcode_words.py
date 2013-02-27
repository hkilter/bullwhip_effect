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


def classifyZipcode(location_text):
    classifier = recognition_heuristic.naivebayes(recognition_heuristic.getwords)

    classifier.setdb('test_100.db')

    classified_zipcode = classifier.classify(location_text)

    zipcode = str(classified_zipcode[0])
    confidence = str(classfied_zipcode[1])

    #query MYSQL database and append to python list
    cur = db.cursor()
    cur.execute("SELECT latitude,longitude FROM sqlbook.zipcounty WHERE zipcode = %s", zipcode)
    rows = cur.fetchall()
    latitude = rows[0][0]
    longitude = rows[0][1]

    likely_zipcode = {"location_text": location_text, "zipcode": zipcode, "latitude": latitude, "longitude": longitude}
    weather = get__weather_data.getWeather(likely_zipcode['zipcode'])

    likely_zipcode.update(weather)
    return likely_zipcode

def closeLocations(zipcode):
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

    top_three = []
    #specific to this query
    for i in range(0, len(query2)):
        if(i < 4):
            temp_dic = {"city": query2[i][2], "zipcode": query2[i][0], "match_latitude":query2[i][7], "match_longitude": query2[i][8]}
            top_ten.append(temp_dic)
        else:
            break
    return top_three

db = MySQLdb.connect(host='localhost', user='root',db='sqlbook')
location_text ="Beverly Hills"
likely_zipcode = classifyZipcode(location_text)

cur.close()
db.close()

print location_text

#if wrong
top_ten = closeLocations(likely_zipcode['zipcode'])

for item in top_ten:
    print item['city'] + ',' + item['zipcode']
#display choices on a map and let user pick the best

if __name__ == '__main__':
    main()
