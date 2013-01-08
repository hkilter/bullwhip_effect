#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      Luke
#
# Created:     04/01/2013
# Copyright:   (c) Luke 2013
# Licence:     <your licence>
#-------------------------------------------------------------------------------
#!/usr/bin/env python

import sys
import os
import networkx as net
import matplotlib.pyplot as plot
import matplotlib.colors as colors
import random as r

def main():
    pass

#I've already defined a company network
#Go and get a company

#two phenomenon: diffusion through a population normally: r(0) rate
#                difusion through a set of companies, non-normally : watching the other companies market cap

class Company(object):
    def __init__(self, id):
        #Start with a single initial preference
        self.id=id
        self.i = r.random()
        self.a = self.i
        #we value initial opinion and subsequent information equally
        self.alpha=0.8

    def __str__(self):
        return(str(self.id))

    def step(self):
        #loop through the neighbors and aggregate their preferences
        neighbors=g[self]
        #all nodes in the list of neighbors are equally weighted, including self
        w=1/float((len(neighbors)+1))
        s=w*self.a
        for node in neighbors:
            s+=w*node.a

        # update my beliefs = initial belief plus sum of all influences
        self.a=(1-self.alpha)*self.i + self.alpha*s

    def interact(self):
        partner=r.choice(g.nodes())
        s=0.5*(self.a + partner.a)
        # update my beliefs = initial belief plus sum of all influences
        self.a=(1-self.alpha)*self.i + self.alpha*s
        g.add_edge(self,partner,weight=(1-self.a-partner.a))

class Influencer(Company):
    def __init__(self,id):
        self.id = id
        self.i = r.random()
        self.a = 1 ## opinion is strong and immovable

    def step(self):
        pass

density=0.035
g=net.Graph()

#create a network of Company objects. Also could be called the network of agents for diffusion model.
for i in range(10):
    c=Company(i)
    g.add_node(c)

#start edits here. Create read_neo4j_graph to networkx object

#this will be a simple random graph, every pair of nodes has an
#equal probability of connection
for x in g.nodes():
    for y in g.nodes():
        if r.random()<=density: g.add_edge(x,y)

# draw the resulting graph and color the nodes by their value
col=[n.a for n in g.nodes()]
pos=net.spring_layout(g)
#net.draw_networkx(g,pos=pos, node_color=col)
plot.savefig("network.png")

#in the edited versions, define an influencer as a consumer? Or as company?

influencers=2
connections=4

#add the influencers to the ntwork and connect each to 3 other nodes

for i in range(influencers):
    inf = Influencer("Inf"+str(i))
    for x in range(connections):
        g.add_edge(r.choice(g.nodes()), inf)

for i in range(30):
    # iterate through all nodes in the network and tell them to make a step
    for node in g.nodes():
        node.step()

    # collect new attitude data, print it to the terminal and plot it.
    col=[n.a for n in g.nodes()]
    print col
    plot.plot(col)

plot.show()

if __name__ == '__main__':
    main()
