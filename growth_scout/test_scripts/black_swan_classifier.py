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

def frequency_train(c1):
    c1.train('incumbent', 'Incumbent Sustaining Strategy')
    c1.train('low-end mobile', 'Disruptive, Disruptive Range')
    c1.train('iOS apps', 'Incumbent Sustaining Strategy, Disruptive Range')
    c1.train('mobile', 'Disruptive Range')
    c1.train('brown ', 'Unknown')
    c1.train('analytics', 'Analytic Innovation')
    c1.train('different', 'Strategic Differentiation')
    c1.train('expensive', 'Anomoly')

# defining a category impact function
def impact_train(c1):
    c1.impactodds('Incumbent Sustaining Strategy', 15.51)
    c1.impactodds('Disruptive, Disruptive Range', 9.23)
    c1.impactodds('Incumbent Sustaining Strategy, Disruptive Range', 5.62)
    c1.impactodds('Disruptive Range', 1.20)
    c1.impactodds('Unknown', 2.77)
    c1.impactodds('Analytic Innovation', 8.3)
    c1.impactodds('Strategic Differentiation', 4.44)
    c1.impactodds('Anomoly', 3.26)

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
        features = self.getfeatures(category)
        for f in features:
            self.incimpact(f, odds)
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

     def classify(self, item, default=None):
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

        for cat in black_swan:
            if cat==best:
                continue
            if black_swan[cat]*self.getthreshold(best)>black_swan[best]:
                return default
        return best, cat_confidence








