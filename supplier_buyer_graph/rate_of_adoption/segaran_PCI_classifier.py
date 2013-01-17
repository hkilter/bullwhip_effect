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

import re
import math

def sampletrain(c1):
    c1.train('Nobody owns the water.', 'good')
    c1.train('the quick rabbit jumps fences', 'good')
    c1.train('buy pharmaceuticals now', 'bad')
    c1.train('make quick money in the online casino', 'bad')
    c1.train('the quick brown fox jumps ', 'good')

def getwords(doc):
    splitter = re.compile('\\W*')
    #Split the wrods by non-alpha characters
    words = [word.lower() for word in splitter.split(doc) if len(word) > 2 and len(word)<20]

    #return the unique set of words only
    return dict((word_key,1) for word_key in words)

class classifier:
    def __init__(self, getfeatures, filename=None):
        #Counts of feature and category combinations
        self.feature_count = {}
        # Counts of documents in each category
        self.category_count={}
        self.category_impact ={}
        self.feature_impact ={}
        self.getfeatures=getfeatures

    def incfeature(self, feature, category):
        self.feature_count.setdefault(feature, {})
        self.feature_count[feature].setdefault(category,0)
        self.feature_count[feature][category]+= 1

    def inccategory(self, category):
        self.category_count.setdefault(category,0)
        self.category_count[category]+= 1

    # defining a category impact function
    def categoryimpact(self, category):
        self.category_impact.setdefault(feature, {})
        self.category_impact[category] = 1.0

    def fcount(self,feature, category):
        if feature in self.feature_count and category in self.feature_count[feature]:
            return float(self.feature_count[feature][category])
        return 0.0

    #defining feature impact. Maybe easier to define in a R classifier? Range, price
    def fimpact(self,feature,category):
        if feature in self.feature =='Disruptive':
            return float(self.feature_count[feature][category]*self.category_impact[category])
        return 0.0

    def catcount(self,category):
        if category in self.category_count:
            return float(self.category_count[category])
        return 0

    def totalcount(self):
        return sum(self.category_count.values())

    def categories(self):
        return self.category_count.keys()

    def train(self, item, category):
        features = self.getfeatures(item)
        for f in features:
            self.incfeature(f, category)

        self.inccategory(category)

    def featureprob(self,feature,category):
        if self.catcount(category) == 0: return 0
        return self.fcount(feature, category)/self.catcount(category)

    def weightedprob(self, feature, category, probability_feature, weight=1.0, assumed=0.5):
        basicprob = probability_feature(feature,category)
        totals = sum([self.fcount(feature, category) for category in self.categories()])
        bp = ((weight*assumed)+(totals*basicprob))/(weight+totals)
        return bp

    #want to return weighted impact instead of weighted probability
    def weightedimpact(self, feature, category, probability_feature, weight=1.0, assumed=0.5):
        basicprob = probability_feature(feature,category)
        #need to make weight_feature function do what probability_feature does
        impact_totals = sum([self.fcount(feature,category)*lookup_impact for category in self.categories()])
        impact = ((weight*assumed)+(impact_totals)* basicprob)/(weight+totals)

    #can't use the probability created by the weighted probability function
    #you can compare the results from different categories and seee which one has the highest probability

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
        probs = {}
        max =0.0
        for cat in self.categories():
            probs[cat]=self.prob(item,cat)
            if probs[cat]>max:
                max = probs[cat]
                best = cat

        for catcount in probs:
            if catcount==best: continue
            if probs[cat]*self.getthreshold(best)>probs[best]: return default
        return best








