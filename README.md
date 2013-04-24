Bullwhip Effect
===============

This is the beginning set of scripts and tools for adaptive and graph based time series modeling using python and R. 
My goal for the project is to be able to use these scripts to answer (and bet on) strategic and logistics questions relating to the bullwhip effect.

You can read about the history of the bullwhip effect at:

http://en.wikipedia.org/wiki/Bullwhip_effect

The bullwhip concept first appeared in Jay Forrester's 1958 article, "Industrial Dynamics—A Major Breakthrough
for Decision Makers," in Harvard Business Review.  The decline of a business was (and still is) often blamed 
on a bad economy or a competitor.  What Forrester sought to model with system dynamics was the process of feedback loops in an industry. 

General Electric, in the 1950’s, was puzzled as to why their household appliance plants sometimes worked three or four shifts and then, a few years later, had to lay of half their staff.

Forrester, after finding out how the corporation made hiring and inventory decisions sought to tackle the problem using system dynamics and simulation--originally using just a pencil and a few pages in a notebook to get an idea of information flow through the company. Through modeling the process (that eventually became computerized for simulation), Forrester accounted how individual managers at the level of sales , distribution and production responded to the information locally available to them as they tried to control their piece of the organization.
Forrester found the managers in each link, in what today is called a supply chain, were responding in a rational fashion to the incentives and information they faced. They were often making choices based on their need to provide good customer service while avoiding excessive inventories. The resulting changes in orders, production, hiring, and other decisions fed back to alter inventories, change prices and advertising rates. The feedback structure of the supply chain amplified each response into persistent cyclical swings, now called the Bullwhip effect. The Bullwhip affect was attributed to exist--even in a state of steady demand--because at every level management relied on their next in chain customer and supplier for demand forecasting. 

#Load the Historical Database
 
 http://dev.mysql.com/downloads/mysql/

1. rate_of_adoption/bass_history.txt can be loaded to a MySQL database with the mysql_bass_db_creation.txt script. Be sure to change the location of the bass_history.txt to wherever the directory it is in on your machine.

#Forecasting Model Pipeline: 
Prerequisites: Community census data on population. 2 data points (or more) on percentage adoption in a community. 

1. Determine:  Historical similarity of innovation and imitation -> Use python program diffusion_query_branch.py 
to generate a p and q (imitation and innovation coefficient).

2.	Gather Community data: population size, and adoption statistics - >  Use community test.py split data on the 
year where Basic diffusion number = 1 (or is projected to equal 6.67% adoption). 

3.	Execute R programs from that point in time: diffusion_number_bass.r, diffusion_rforecast.r

4.	Save output forecast tables to text (csv) files, images to png

5.	Execute python program population_size.py: This outputs the forecasted adoption at a given year by
combining the projected adoption percentage  with the size of the community. Example: If its projected 
20% adoption in 1999 of 1 billion people in China, the program outputs 200 million 

6.	Compare accuracy between diffusion_number_bass and diffusion_rforecast or just use to get an estimate 
of adoption via one method at a future time


#Future Plans

 I need to add a user interface for ratings
   
   -as of now they can be changed by changing the historical database dictionary diffusion_query_branch.py

  - adding graph database support with the simplegraph module and
 
   -expand the historical database to include more examples
