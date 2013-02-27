#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      Luke
#
# Created:     31/08/2012
# Copyright:   (c) Luke 2012
# Licence:     <your licence>
#-------------------------------------------------------------------------------
#!/usr/bin/env python

import nltk, re, pprint, csv

def main():
    pass

test = ["Robert", "Rupert"]

def soundex(name, len=4):
    """ soundex module conforming to Knuth's algorithm
        implementation 2000-12-24 by Gregory Jorgensen
        public domain
    """

    # digits holds the soundex values for the alphabet
    digits = '01230120022455012623010202'
    sndx = ''
    fc = ''

    # translate alpha chars in name to soundex digits
    for c in name.upper():
        if c.isalpha():
            if not fc: fc = c   # remember first letter
            d = digits[ord(c)-ord('A')]
            # duplicate consecutive soundex digits are skipped
            if not sndx or (d != sndx[-1]):
                sndx += d

    # replace first digit with first alpha character
    sndx = fc + sndx[1:]

    # remove all 0s from the soundex code
    sndx = sndx.replace('0','')

    # return soundex code padded to len characters
    return (sndx + (len * '0'))[:len]



inc500= [line.strip() for line in open('C:\Documents and Settings\Luke\Desktop\growth_scout\inc500_list.txt', 'r')]
jobtobedone1 = [line.strip() for line in open('C:\Documents and Settings\Luke\Desktop\growth_scout\jobtobedone1_list.txt', 'r')]
jobtobedone1_tuple = [(company, soundex(company)) for company in jobtobedone1]
jobtobedone1_soundex = [soundex(company) for company in jobtobedone1]
matchlist = [line.strip() for line in open('C:\Documents and Settings\Luke\Desktop\growth_scout\unique_match_soundex.txt', 'r')]

new_list = []

doc = 'C:\Documents and Settings\Luke\Desktop\\growth_scout\out\unique_matchjobtobedone1_list.csv'
f = csv.writer(open(doc,'wb'), delimiter =',', quotechar='\'', quoting=csv.QUOTE_MINIMAL)

##for element in inc500:
##    scode = soundex(element)
##    if scode in jobtobedone1_soundex:
##        try:
##            f.writerow([element, scode])
##        except:
##            continue

for item in jobtobedone1:
    scode = soundex(item)
    if scode in matchlist:
        try:
            f.writerow([item, scode])
        except:
            continue
if __name__ == '__main__':
    main()
