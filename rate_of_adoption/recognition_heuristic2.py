#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      Luke
#
# Created:     01/09/2012
# Copyright:   (c) Luke 2012
# Licence:     <your licence>
#-------------------------------------------------------------------------------
#!/usr/bin/env python

from pysqlite2 import dbapi2 as sqlite
import re
import math
import cPickle

#maybe only need a regular classfier for this
#almost an inverse of population

#product or service adoption circumstances
def frequency_train(c1):
    c1.train('Cellular and digital wireless phones have been on a disruptive path against wireline phones for 25 years. \
             Initially they were large, power-hungry car phones with spotty efficacy; but gradually have improved to the \
             point where, by some estimates, nearly one-fifth of mobile telephone users have chosen to cut the cord and do \
             without wireline telephone service.  The viability of the wireline long distance business is now in jeopardy. ', 'Cellular')
    c1.train('Its operating system was inadequate versus those of mainframe and minicomputer makers versus Unix and versus Apple system.  \
             But its migration from DOS to Windows to Windows NT is taking the firm up-market, to the point that the Unix world is seriously threatened. \
             Microsoft, in turn, faces a threat from Linux. Intel earliest microprocessor in 1971 could only constitute the brain of a four-function calculator. \
             Makers of computers whose logic circuitry is microprocessor-based have disrupted firms that made mainframe and minicomputers, whose logic circuitry \
             was printed wiring board-based. Dell direct-to customer retailing model and its fast-throughput, high asset-turns manufacturing model allowed it to  \
             come underneath Compaq, IBM and Hewlett Packard as a low-end disruptor in personal computers.  Clayton Christensen, the quintessential low-end consumer, \
             wrote his doctoral thesis on a Dell notebook computer purchased in 1989, because it was the cheapest portable computer on the market.  Because of Dell \
             reputation for marginal quality, students needed special permission from Harvard to use doctoral stipend money to buy a Dell rather than a computer with \
              a more reputable brand.  Today Dell supplies most of the Harvard Business School computers.', 'Home PC')
    c1.train('This firm makes a hand-held ultrasound device that enables healthcare professionals who historically needed the assistance of highly trained technicians \
              with expensive equipment, now to look inside the bodies of patients in their care, and thereby to provide more accurate and timely diagnoses. \
              The company floundered for a time attempting to implement its product as a sustaining innovation.  But as of the time this book was being written, \
              it seemed to have caught its disruptive stride in an impressive way. ', 'Ultrasound')


#two parameter training. We don't have any impacts in this case--yet. So, set to 1.
def impact_train(c1):
    # Class, coefficient of innovation, coefficient of imitation
    c1.impactodds('Ultrasound', 1)
    c1.impactodds('Home PC', 1)
    c1.impactodds('Cellular', 1)


#change to get features
def getwords(doc):
    splitter = re.compile('\\W*')
    #Split the words by non-alpha characters
    words = [word.lower() for word in splitter.split(doc) if len(word) > 2 and len(word)<20]

    #return the unique set of words only
    return dict((word_key,1) for word_key in words)

class classifier:
    def __init__(self, getfeatures, filename=None):
        #Counts of feature and category combinations
        self.feature_count = {}
        # Counts of documents in each category
        self.category_count={}
        self.category_impact={}
        self.confidence={}
        self.getfeatures=getfeatures

    def setdb(self,dbfile):
        self.con=sqlite.connect(dbfile)
        self.con.execute('create table if not exists fc(feature,category,count)')
        self.con.execute('create table if not exists cc(category,count)')
        self.con.execute('create table if not exists co(category,odds)')

    def incfeature(self, feature, category):
        count = self.fcount(feature,category)
        if count ==0:
            self.con.execute("insert into fc values('%s','%s',1)" % (feature,category))
        else:
            self.con.execute("update fc set count=%d where feature='%s' and category='%s'" % (count+1,feature,category))

    def inccategory(self, category):
        count=self.catcount(category)
        if count==0:
            self.con.execute("insert into cc values ('%s',1)" % (category))
        else:
            self.con.execute("update cc set count=%d where category='%s'"
                       % (count+1,category))

    def incimpact(self, category, impact):
         odds=self.catodds(category)
         if odds==0:
            self.con.execute("insert into co values ('%s','%s')"
                       % (category,impact))
         else:
            self.con.execute(
              "update co set odds=%d where category='%s'"
                 % (odds+impact,category))

    def fcount(self,feature, category):
        res=self.con.execute('select count from fc where feature="%s" and category="%s"'
                %(feature,category)).fetchone()
        if res==None: return 0
        else: return float(res[0])

    def catcount(self,category):
         res=self.con.execute('select count from cc where category="%s"'
                         %(category)).fetchone()
         if res==None: return 0.0
         else: return float(res[0])


    def catodds(self, category):
         res=self.con.execute('select odds from co where category="%s"'
                         %(category)).fetchone()
         if res==None: return 0.0
         else: return float(res[0])


    def totalcount(self):
        res=self.con.execute('select sum(count) from cc').fetchone();
        if res==None: return 0
        return res[0]

    def categories(self):
        cur=self.con.execute('select category from cc');
        return [d[0] for d in cur]

    def train(self,item,category):
        features=self.getfeatures(item)
        for f in features:
            self.incfeature(f,category)

        self.inccategory(category)
        self.con.commit()

    #might need to update still
    def impactodds(self, category, odds):
        #features = self.getfeatures(category)
        self.incimpact(category, odds)
        #for f in features:
            #self.incimpact(f, odds)
        self.con.commit()

    def featureprob(self,feature,category):
        if self.catcount(category) == 0: return 0
        return self.fcount(feature, category)/self.catcount(category)

    def setfilename(self,filename):
        self.filename=filename
        self.restoredata()

    def restoredata(self):
        try: f=file(self.filename,'rb')
        except: return
        self.fc=cPickle.load(f)
        self.cc=cPickle.load(f)
        f.close()

    def savedata(self):
        f=file(self.filename,'wb')
        cPickle.dump(self.fc,f,True)
        cPickle.dump(self.cc,f,True)
        f.close()

    def weightedprob(self, feature, category, probability_feature, weight=1.0, assumed=0.5):
        basicprob = probability_feature(feature,category)
        totals = sum([self.fcount(feature, category) for category in self.categories()])
        bp = ((weight*assumed)+(totals*basicprob))/(weight+totals)
        return bp


class naivebayes(classifier):
     def __init__(self,getfeatures):
        classifier.__init__(self,getfeatures)
        self.thresholds={}

     def docprob(self, item, category):
        features = self.getfeatures(item)
        # Multiply the probabilities of all the features together
        p=1
        for f in features: p*=self.weightedprob(f, category, self.featureprob)
        return p

     def prob(self, item, category):
        category_prob = self.catcount(category)/self.totalcount()
        docprob = self.docprob(item, category)
        return docprob*category_prob

     def setthreshold(self, category, t):
        self.thresholds[category]=t

     def getthreshold(self, category):
        if category not in self.thresholds:return 1.0
        return self.thresholds[category]

     def classify(self, item, default='Average'):
        black_swan= {}
        max =0.0
        tot_confidence ={}
        rel_confidence ={}
        for cat in self.categories():
            black_swan[cat]=self.prob(item,cat)*abs(self.catodds(cat))
            if black_swan[cat]>max:
                max = black_swan[cat]
                best = cat
            #confidence test
            upper_bound = abs(self.catodds(cat))
            if upper_bound != 0:
                tot_confidence[cat] = black_swan[cat]/upper_bound
            else:
                continue

        #relative confidence
        for cat in self.categories():
             rel_confidence[cat] = black_swan[cat]/black_swan[best]

        #category_confidence : iterate through the list and add all the relative values then subtract 1.01
        cat_confidence = 1- (sum(rel_confidence.values())-1.01)

        #add returning the top 5
        counter = 0
        for cat in black_swan:
            if cat==best:
                continue
            if black_swan[cat]*self.getthreshold(best)>black_swan[best]:
                return default
        return best, cat_confidence








