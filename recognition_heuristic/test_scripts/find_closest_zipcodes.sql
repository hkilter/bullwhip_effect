#The geographic center of the continental United States is in the middle of Kansas
 and has a longitude of –98.6° and a latitude of 39.8°. 
By converting the differences in coordinates to miles, 
the following query finds the ten closest zip codes to the geographic center:

SELECT  zipcode, state, population, latitude, longitude, disteuc
FROM (SELECT zc.*,
             (CASE WHEN latitude > 39.8
                   THEN SQRT(SQUARE(difflat*68.9) +
                             SQUARE(difflong*SIN(latrad)*68.9))
                   ELSE SQRT(SQUARE(difflat*68.9) +
                             SQUARE(difflong*SIN(centerlatrad)*68.9))
              END) as disteuc
      FROM (SELECT zc.*, latitude - 39.8 as difflat,
                   longitude - (-98.6) as difflong,
                   latitude*PI()/180 as latrad,
                   39.8*PI()/180 as centerlatrad
            FROM zipcensus zc) zc) zc
ORDER BY disteuc


# The following query calculates all zip codes within eight miles of Dartmouth University in Hanover, NH
SELECT z.zipcode, z.state, zco.poname, distcirc, population, hh,
       hhmedincome
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
            WHERE zipcode IN ('03755')) comp) z LEFT OUTER JOIN
       zipcounty zco
      ON z.zipcode = zco.zipcode
WHERE distcirc < 8
ORDER BY distcirc

#find all the zipcodes where that had solar power in 2000 and compare to today
SELECT zipcode, longitude,
       (CASE WHEN hhuofuelsolar = 0 THEN latitude END) as nosolarlat,
       (CASE WHEN hhuofuelsolar > 0 THEN latitude END) as solarlat
FROM zipcensus
WHERE latitude BETWEEN 20 and 50 AND
      longitude BETWEEN -135 AND -65

#What proportion of zip codes in each state have at least one solar powered residence? The following query answers this question, using the Census Bureau definition of a state:

SELECT TOP 10 state,
       SUM(CASE WHEN hhuofuelsolar > 0 THEN 1.0 END)/COUNT(*) as propzips,
       SUM(hhuofuelsolar*hhuoccupied)/SUM(hhuoccupied) as prophhu
FROM zipcensus zc
GROUP BY state
ORDER BY 3 DESC
