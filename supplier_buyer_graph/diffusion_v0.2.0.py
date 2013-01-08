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

    def _roulette_choice(self,names,values, inverse=False):
        """
        roulette method makes unequally weighted choices based on a set of values
        Names and values should be lists of equal lengths
        values are between 0 and 1
        if inverse=False, names with higher values have a higher probability of choice;
        if inverse=True, names with lower values have hight probability

        """
        wheel=names
        for i in range(len(names)):
            if not inverse:
                wheel.extend([names[i] for x in range(1+int(values[i]*10))])
            else:
                wheel.extend([names[i] for x in range(1+int((1-values[i])*10))])
        return(r.choice(wheel))

    def interact(self):
        """
        instead of looking at all of the neighbors,
        let's pick a random node and exchange information with him
        this will create an edge and weigh it with their similarity.

        Phase II -- make roulette choice instead of random choice
        """
        neighbors=g[self].keys()
        values=[v['weight'] for v in g[self].values()]

        ## roll dice and decide to communicate with
        ## similar (0.6), dissimilar(0.3) or random (0.1)
        roll=r.random()
        if r <= 0.1 or len(neighbors)==0:
            partner=r.choice(g.nodes())
        elif r<=0.4:
            partner=self._roulette_choice(neighbors,values,inverse=True)
        else:
            partner=self._roulette_choice(neighbors,values,inverse=False)

        w=0.5
        s=self.a*w + partner.a*w
        # update my beliefs = initial belief plus sum of all influences
        self.a=(1-self.alpha)*self.i + self.alpha*s
        g.add_edge(self,partner,weight=(1-self.a-partner.a))

density=0.9
g=net.Graph()

#create a network of Company objects. Also could be called the network of agents for diffusion model.
for i in range(10):
    c=Company(i)
    g.add_node(c)


def consensus(g):
    """
    Calculcate consensus opinion of the graph
    """
    aa=[n.a for n in g.nodes()]
    return min(aa),max(aa),sum(aa)/len(aa)

def trim_edges(g, weight=1):
    g2=net.Graph()
    for f, to, edata in g.edges(data=True):
        if edata != {}:
            if edata['weight'] > weight:
                g2.add_edge(f,to,edata)
    return g2

density=0.05
decay_rate=0.01
network_size=100
runtime=200
g=net.Graph()

# create a network of Company objects
for i in range(network_size):
    c=Company(i)
    g.add_node(c)

##this will be a simple random graph, with random weights
for x in g.nodes():
    for y in g.nodes():
        if r.random()<=density: g.add_edge(x,y,weight=r.random())

col=[n.a for n in g.nodes()]
pos=net.spring_layout(g)
net.draw_networkx(g,pos=pos, node_color=col,cmap=plot.cm.Reds)

cons=[]
for i in range(runtime):
    for node in g.nodes():
        node.interact()

    #degrade edge weights by a fixed rate
    for f,t,data in g.edges(data=True):
        data['weight']=data['weight']*(1-decay_rate)
        if data['weight']<0.1: g.remove_edge(f,t)

    col=[n.a for n in g.nodes()]
    ew=[1000*edata['weight'] for f,to,edata in g.edges(data=True)]
    plot.figure(2)
    plot.plot(col)

    cons.append(consensus(g))

plot.figure(i)
g2=trim_edges(g, weight=0.3)
col=[n.a for n in g2.nodes()]
net.draw_networkx(g2,node_color=col, cmap=plot.cm.Reds) #,edge_color=ew,edge_cmap=plot.cm.RdPu)

plot.figure(i+1)
plot.plot(cons)
plot.figure(i+2)
plot.hist([e['weight'] for f,t,e in g.edges(data=True)])
plot.show()

if __name__ == '__main__':
    main()
