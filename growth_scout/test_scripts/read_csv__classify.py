#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      Luke
#
# Created:     09/09/2012
# Copyright:   (c) Luke 2012
# Licence:     <your licence>
#-------------------------------------------------------------------------------
#!/usr/bin/env python

import os,csv, nltk, sqlite3
#note must add to python path
import black_swan_classifier
##import fromwordcount__docclass_nnf
#Send numbers to r classifier

def main():
    pass

#change path to present working directory
os.chdir('C:\Documents and Settings\Luke\Desktop\growth_scout\\test_scripts')

#stopwords
stopwords1 = nltk.corpus.stopwords.words('english') + ['.', ',', '--', '\'s', '?',')','(', ':','\'','\'re', '"', '-', '}', '{','/p', '<','>']

table = csv.reader(open('business_model_train_failure.csv'), delimiter=',', quotechar='\"')

##table2 = csv.reader(open('jobtobedone1_id_name_twitter.csv'), delimiter='\t')

def getwordstext(ttext):
    Word_count ={}
    tokens = nltk.word_tokenize(ttext)
    words = [w for w in tokens if (w not in stopwords1)]
    for word in words:
        Word_count[word] = Word_count.get(word,0)+1
    return Word_count

def getstring(string):
    return string


def wordmatrixfeatures(x):
    return x

next(table)

#black swan classifier
classifier = black_swan_classifier.naivebayes(wordmatrixfeatures)
classifier.setdb('C:\Documents and Settings\Luke\Desktop\growth_scout\\test_scripts\\bswan_classifier.db')

#frequency classifier
##classifier = fromwordcount__docclass_nnf.naivebayes(wordmatrixfeatures)
##classifier.setdb('C:\Documents and Settings\Luke\Desktop\growth_scout\\test_scripts\\frequency_classifier.db')

classification = {}
feature_list =[]
company =[]
class_human=[]

for row in table:
    business_text = row[2]
    business_class = row[0]
    word_count = getwordstext(business_text)

    #need to classify all fifteen words at once knowing expected population size
##    try:
##            classifier.train(word_count, business_type)
##            classification[row[1]] = classifier.classify(business_text,default=None)
##    except:
##        continue
##        print 'error'
    print word_count
    feature_list.append(word_count)
##    class_human.append(business_class)
    company.append(business_class)
##    for i in range(len(feature_list)):
##        try:
##            classification[company[i]] = classifier.classify(feature_list[i],default=None)
##        except:
##            continue
##            print 'error' + str(company[i])


#start at 71 in business_model_train
#aword_count = getwordstext('Provides cloud-based services for publishing and distributing professional digital media. Customers include the New York Times and General Motors.')
#classifier.train(aword_count, 'Disruptive Range')

# for i in range(len(feature_list)):
#    classifier.train(feature_list[i], classification[i])
#classification[company[0]] = classifier.classify(feature_list[0],default=None)

if __name__ == '__main__':
    main()
