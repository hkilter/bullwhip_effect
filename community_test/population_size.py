#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      Luke
#
# Created:     18/01/2013
# Copyright:   (c) Luke 2013
# Licence:     <your licence>
#-------------------------------------------------------------------------------
#!/usr/bin/env python

import csv, os

def main():
    pass

os.chdir("C:\Documents and Settings\Luke\Desktop\community_test")

#dictionary of all of the nodes
country_index = csv.reader(open('population_subset.csv'), delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
next(country_index)

country_dict ={}

for country in country_index:
    country_dict[country[0]] = int(country[2])

# point csv reader at csv file. Set delimiter and quote characters
table = csv.reader(open('community_saturation_hypothesis_subset.csv'), delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

#create a json object of the header rows with stored incoming csv column numbers
for row in table:
        data = {}
        #If IndexError: list index out of range, specify column range from length of csv
        for col in range(0,13):
            data2 = {row[col]: col}
            data.update(data2)
        break

headers = data
print headers

#invert the csv and store as a dictionary
inv_headers = {v:k for k, v in headers.items()}

#initilize datetime object
temp_dic = {}
for row in table:
    try:
        data ={}
        country= str(row[0])
        for col in range(1,13):
            if(row[col] > 0):
                data2 = {inv_headers[col]: float(row[col])}
            else:
                #data2 = {inv_headers[col]: 0.0}
                continue
            data.update(data2)
        print data #for testing
        #append data, reset last_trader, ++linecount
        temp_dic[country] = data
    except:
        print str(country) + ",error"
        continue

r = csv.reader(open('bass_adoption_triplestore.csv'), delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

#change triplestore to a dictionary
bass_data = {}
for row in r:
    if row[0] in bass_data:
        temp = bass_data[row[0]]
        temp2 = {row[1]:row[2]}
        temp.update(temp2)
        bass_data[row[0]] = temp
    else:
        bass_data[row[0]] = {row[1]:row[2]}

#Year to Project
year_query = 2011
time = str(year_query)

##year_series = [str(year) for year in range(2009,2012)]

#for year in year iterate a project the populations
Population = 0
#lookup adoption projected for year
for group in country_dict.iterkeys():
    try:
        Basic_Diffusion_Number = (float(bass_data[group][time])/100) / .0667
        if(Basic_Diffusion_Number > 1):
            Community_Population = country_dict[group] * (bass_data[group][time]/100)
            #Project when the cliff will be using bass
            #Lookup bass projection at year
            Population = Population + Community_Population
        else:
            #lookup best-fit or linear growth projection at year
            Community_Population = country_dict[group] * (temp_dic[group][time]/100)
            Population = Population + Community_Population
    except:
        print group

#Project the Population at a given year
Total_Population = sum([v for k,v in country_dict.iteritems()])
adoption_pct = Population/Total_Population * 100
adoption_text = "%d" % (int(adoption_pct))
print str(int(Population)) +  " of " + str(Total_Population) + " (" + adoption_text + "%) "+ "in " + str(year_query)



if __name__ == '__main__':
    main()
