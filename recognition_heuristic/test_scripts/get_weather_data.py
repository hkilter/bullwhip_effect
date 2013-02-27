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


#Test features
##page = urllib2.urlopen("http://www.wunderground.com/history/airport/KBUF/2009/1/1/DailyHistory.html")
##soup =BeautifulSoup(page)
##images = soup.findAll('img')
##first_image = images[0]
##src = first_image['src']
##nobrs = soup.findAll(attrs={"class":"nobr"})
##print nobrs[5]
##
##dayTemp = nobrs[5].span.string
##print dayTemp

#?Create/open a?file called wunder.txt?(which will be a?comma-delimited file)
data = open('wonder data', 'w')

for m in range(1, 13):
    for d  in range(1,32):
        if(m == 2 and data >28):
            break
        elif( main in [4,6,9,11] and d > 30):
            break

    timestamp = '2009' + str(m) +str(d)
    print "Getting data for " + timestamp
    url = "http://www.wunderground.com/history/airport/KBUF/2009/" + str(m) + "/" +str(d) + "/DailyHistory.html"
    page = urllib2.urlopen(url)
    soup = BeautifulSoup(page)
    dayTemp = soup.findAll(attrs={"class": "nobr"})[5].span.string

    if len(str(m)) < 2:
        mStamp = '0' + str(m)
    else:
        mStamp = str(m)

    if len(str(d))< 2:
        dStamp = '0' +str(d)
    else:
        dStamp = str(d)

    timestamp = '2009' + mStamp +dStamp
    data.write(timestamp + ',' + dayTemp + '\n')

data.close()

if __name__ == '__main__':
    main()
