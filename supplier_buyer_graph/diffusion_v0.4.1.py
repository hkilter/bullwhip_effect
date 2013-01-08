#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      Luke
#
# Created:     01/06/2013
# Copyright:   (c) Luke 2013
# Licence:     <your licence>
#-------------------------------------------------------------------------------
#!/usr/bin/env python

import sys, os, csv
import networkx as net
import matplotlib.pyplot as plot
import matplotlib.colors as colors
from py2neo import neo4j
from py2neo import gremlin
import random as r

def main():
    pass

#I've already defined a company network
#Go and get a company
db = neo4j.GraphDatabaseService("http://ec2-23-21-228-70.compute-1.amazonaws.com:7474/db/data/")
neo_index = csv.reader(open('graph_nodes.txt'), delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
neo_dict ={}

for company in neo_index:
    neo_dict[company[0]] = int(company[1])

total_disruptive_range_capital = 4301.00

class Company(object):
    def __init__(self, id):
        temp_dict = db.get_node(id)
        #Start with a single initial preference
        self.id=id
        self.initial = r.random()
        self.attitude = self.initial
        self.model = temp_dict['b2b_b2c']
        self.start_role = temp_dict['roles']
        self.starting_funds = temp_dict['starting_funds_millions']
        self.business_model = temp_dict['strategy_name']
        self.last_year = temp_dict['last_year']
        #company values initial opinion and subsequent information equally
        self.neighbor_trust= 0.8

    def __str__(self):
        return(str(self.id))

    def step(self):
        #loop through the neighbors and aggregate their preferences
        neighbors=g[self]
        #all nodes in the list of neighbors need to be weighted by status
        weight=1/float((len(neighbors)+1))
        #maybe this should be 1/rank. Thus weighting the opinon of a boss or high status person more heavily
        status=weight*self.attitude
        for node in neighbors:
            status+=weight*node.starting_funds
        # update my beliefs = initial belief plus sum of all influences
        self.attitude =(1-self.alpha)*self.initial + self.alpha*status

#define a growth function
#based on market size

density = 0.035
g = net.Graph()

for item in neo_dict.itervalues():
    if((item < 25) or (32 < item < 98)):
        c=Company(item)
        g.add_node(c)
        print "added " + str(c)

#simple rules for links.
#1. Your starting funds have to be greater than 0 to make links
#2. Your number of links you're capable of carrying relates to your market share of the network
#3. Your ability to make links relates to the density of the graph. Less density (easier to make links) with less money

for x in g.nodes():
    if((x.starting_funds > 0)):
        LINK_MAX = x.starting_funds/total_disruptive_range_capital
        link_count = 0
        for y in g.nodes():
            if((x.business_model =='Disruptive Range') or (x.business_model == 'Disruptive, Disruptive Range') or x.business_model =='Incumbent Sustaining Stratgy, Disruptive Range'):
                g.add_edge(x,y)
                link_count = link_count + 1
                if(link_count > LINK_MAX):
                    break
            if ((x.starting_funds/total_disruptive_range_capital) >= density):
                g.add_edge(x,y)
                link_count = link_count + 1
                if(link_count > LINK_MAX):
                    break

# draw the resulting graph and color the nodes by their value
col=[n.attitude for n in g.nodes()]
pos=net.spring_layout(g)
net.draw_networkx(g,pos=pos, node_color=col)

# collect new attitude data, print it to the terminal and plot it.
col=[n.attitude for n in g.nodes()]
print col
plot.plot(col)

plot.show()

if __name__ == '__main__':
    main()
