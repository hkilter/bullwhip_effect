#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      Luke
#
# Created:     07/05/2012
# Copyright:   (c) Luke 2012
# Licence:     <your licence>
#-------------------------------------------------------------------------------
#!/usr/bin/env python

def main():
    pass

from nntplib import *

s = NNTP('web.aioe.org')
(resp, count, first, last, name) = s.group('comp.lang.python')
(resp, subs) = s.xhdr('subject', (str(first)+'-'+str(last)))
for subject in subs[-10:]:
    print(subject)

number = input('Which article do you want to read? ')
(reply, num, id, list) = s.body(str(number))
for line in list:
    print(line)

if __name__ == '__main__':
    main()
