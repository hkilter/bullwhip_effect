#-------------------------------------------------------------------------------
# Name:        diffusion by analogy
# Purpose:
#
# Author:      Luke
#
# Created:     01/10/2012
# Copyright:   (c) Luke 2013
# Licence:      GPL
#-------------------------------------------------------------------------------
#!/usr/bin/env python

import MySQLdb
import recognition_heuristic2
from math import sqrt
import csv
import simplejson as json

def main():
    pass

#input text, output scores 1 to 5 on historical similarity

#Query the MYSQL database and append to python dictionary
db = MySQLdb.connect(host='localhost', user='root',db='bass_data')
cur = db.cursor()

query = {}
for item in range(1,48):
    cur.execute("SELECT name, p_data, q_data,population_size_at_time  FROM bass_data.historical WHERE idhistorical= %s", item)
    rows = cur.fetchall()
    #append all the names to a list
    for row in rows:
        name = str(row[0])
        if(row[3]):
            size_at_time = row[3]
            size_at_time = json.loads(size_at_time)
        else:
            size_at_time = 'null'
        subquery = {name : {"p_data": row[1], "q_data":row[2], "size_at_time": size_at_time}}
    query.update(subquery)

cur.close()
db.close()

#go through and rate the similarity of your product to past examples
#decide whether to keep going or stop

#test on smart phones
historical_similarity={'Smart_Phone': {'Satellite TV': 4.0, 'email': 4.0,
 'Radio': 3.5, 'Home PC': 4.5, 'Color TV': 2.5,
 'Cable TV': 4.0, 'AOL':4.0, 'ATM machines': 4.5}, 'Satellite TV':{'email': 3.0,
 'Radio': 3.5, 'Home PC': 4.0, 'Color TV': 4.5,
 'Cable TV': 5.0, 'ATM machines': 2.5}, 'Data_Plan':{'AOL': 4.5, 'Cable TV': 4.0, 'Cell phone': 5.0, 'Smart_Phone': 5.0, 'Satellite TV': 4.0,'email':3.5}}

#Returns a distance-based similarity score for person1 and person2
def sim_distance(sim_db,item1,item2):
  # Get the list of shared_items
  similar_items={}
  for item in sim_db[item1]:
    if item in sim_db[item2]: similar_items[item]=1

  # if they have no ratings in common, return 0
  if len(similar_items)==0: return 0

  # Add up the squares of all the differences
  sum_of_squares=sum([pow(sim_db[item1][item]-sim_db[item2][item],2)
                      for item in sim_db[item1] if item in sim_db[item2]])

  return 1/(1+sum_of_squares)

# Returns the Pearson correlation coefficient for p1 and p2
def sim_pearson(prefs,p1,p2):
  # Get the list of mutually rated items
  similar_items={}
  for item in prefs[p1]:
    if item in prefs[p2]: similar_items[item]=1

  # if they are no ratings in common, return 0
  if len(similar_items)==0: return 0

  # Sum calculations
  n=len(similar_items)

  # Sums of all the preferences
  sum1=sum([prefs[p1][it] for it in similar_items])
  sum2=sum([prefs[p2][it] for it in similar_items])

  # Sums of the squares
  sum1Sq=sum([pow(prefs[p1][it],2) for it in similar_items])
  sum2Sq=sum([pow(prefs[p2][it],2) for it in similar_items])

  # Sum of the products
  pSum=sum([prefs[p1][it]*prefs[p2][it] for it in similar_items])

  # Calculate r (Pearson score)
  num=pSum-(sum1*sum2/n)
  den=sqrt((sum1Sq-pow(sum1,2)/n)*(sum2Sq-pow(sum2,2)/n))
  if den==0: return 0

  r=num/den

  return r

def topMatches(prefs,item,n=5,similarity=sim_pearson):
  scores=[(similarity(prefs,item,other),other)
                  for other in prefs if other!=item]
  scores.sort()
  scores.reverse()
  return scores[0:n]

#Gets recommendations for a person by using a weighted average
# of every other user's rankings
def getRecommendations(prefs,person,similarity=sim_pearson):
  totals={}
  simSums={}
  for other in prefs:
    # don't compare me to myself
    if other==person: continue
    sim=similarity(prefs,person,other)

    # ignore scores of zero or lower
    if sim<=0: continue
    for item in prefs[other]:

      # only score movies I haven't seen yet
      if item not in prefs[person] or prefs[person][item]==0:
        # Similarity * Score
        totals.setdefault(item,0)
        totals[item]+=prefs[other][item]*sim
        # Sum of similarities
        simSums.setdefault(item,0)
        simSums[item]+=sim

  # Create the normalized list
  rankings=[(total/simSums[item],item) for item,total in totals.items()]

  # Return the sorted list
  rankings.sort()
  rankings.reverse()
  return rankings

top_match = topMatches(historical_similarity, 'Smart_Phone',n=3)

count =len(top_match)-1
# get population estimate

key_list =[]
for items in range(0, 2):
    key = top_match[items][1]
    key_list.append(key)

population_size = 0

#get the p and q values
#project wireless data plan + smart_phone

population_ratio = 0.000

for item in key_list:
    if(query[item]['size_at_time']['size'] > 0 and query[item]['size_at_time']['available_size'] > 0):
        population_ratio = population_ratio + float(query[item]['size_at_time']['size'])/float(query[item]['size_at_time']['available_size'])


population_ratio = population_ratio/len(key_list)

value = query[key]
p = value['p_data']
q = value['q_data']
m = value['size_at_time']['available_size'] * population_ratio




if __name__ == '__main__':
    main()
