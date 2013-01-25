bullwhip_effect
===============

study of a disruptive entrant to a network

#Load the Historical Database
 
 http://dev.mysql.com/downloads/mysql/

1. bass_history.txt can be loaded to MySQL database with the mysql_bass_db_creation.txt script 
 by executing it in the SQL query window. Be sure to change the location of the bass_history.txt
to wherever it is on your machine.

#Model Pipeline: 
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
