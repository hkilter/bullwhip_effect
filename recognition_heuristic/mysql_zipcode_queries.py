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

import MySQLdb

def main():
    pass

#zipcode or list of zipcodes for geocode query
zipcodes = 90210

#Query the MYSQL database and append to python list
db = MySQLdb.connect(host='localhost', user='root',db='sqlbook')
cur = db.cursor()
cur.execute("SELECT latitude,longitude FROM sqlbook.zipcounty WHERE zipcode = %s", zipcodes)
rows = cur.fetchall()
query = []
for row in rows:
    for col in row:
        query.append(col)

#select 10 similar locations to the one classified.
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
ORDER BY distcirc""", zipcodes)

query2 = []
rows = cur.fetchall()
for row in rows:
    for col in row:
        query2.append(col)


cur.close()
db.close()

if __name__ == '__main__':
    main()
