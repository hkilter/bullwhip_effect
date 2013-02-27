#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      Luke
#
# Created:     08/05/2012
# Copyright:   (c) Luke 2012
# Licence:     <your licence>
#-------------------------------------------------------------------------------
#!/usr/bin/env python

def main():
    pass

import urllib2
from bs4 import BeautifulSoup

#get the dayTemp and dayWind for a zipcode. If the Temperature is over an amount or a
#the wind is over 45 print a warning for the zipcode

def getWeather(zipcode):
    address = "http://www.wunderground.com/cgi-bin/findweather/hdfForecast?query=%s" % (zipcode)
    page = urllib2.urlopen(address)
    soup =BeautifulSoup(page)
    dayTemp = soup.findAll(attrs={"class": "nobr"})[5].span.string
    dayWind = soup.findAll(attrs={"id": "windCompassSpeed"})[0].string
    infoTime = soup.findAll(attrs={"id": "infoTime"})[0].string
    latitude = soup.findAll(attrs={"id": "infoLatitude"})[0].span.string
    longitude = soup.findAll(attrs={"id": "infoLongitude"})[0].span.string
    pressure = soup.findAll(attrs={"id": "rapidpress"})[0].b.string
    sunRise = soup.findAll(attrs={"id": "sRise"})[0].span.string
    sunSet= soup.findAll(attrs={"id": "sSet"})[0].span.string
    zipcode_conditions = {"temperature": float(dayTemp), "wind_speed" : float(dayWind), "stationlatitude": latitude, "stationlongitude":longitude, "pressure" : pressure}
    return zipcode_conditions


if __name__ == '__main__':
    main()
