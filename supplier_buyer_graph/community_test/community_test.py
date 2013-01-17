#-------------------------------------------------------------------------------
# Name:        Read_table__update_couchdb
# Purpose:     Read a csv file and load documents to couchdb
#
# Author:      Luke Otterblad
#
# Created:     04/09/2012
# Copyright:   (c) Luke 2012
# Licence:     GPL
#-------------------------------------------------------------------------------
#!/usr/bin/env python

#resquired libraries
import csv, os, re, couchdb
import simplejson as json
import datetime
import operator

def main():
    pass

server = couchdb.Server('http://127.0.0.1:5984')

#change path to present working directory
os.chdir('C:\Documents and Settings\Luke\Desktop')

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

# skip header if you just need the data
#invert dictionary
inv_headers = {v:k for k, v in headers.items()}

def update_data_couchdb(entity, history_list):
    DB = 'trades_etoro_%s' % (entity.lower())
    try:
        db = server.create(DB)
        db.update(history_list, all_or_nothing=True)
    except couchdb.http.PreconditionFailed, e:
        # Already exists, so append to it, keeping in mind that duplicates could occur
        db = server[DB]
        #If IndexError: list index out of range, specify column range from length of csv
        db.update(history_list, all_or_nothing=True)
    return

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

#sample size is 107
len(temp_dic)

#Get year of hypothesis pass of basic diffusion number
for item in temp_dic.iterkeys():
    years = temp_dic[item]
    year_hash = sorted(years, reverse=True)
    for year in year_hash:
        if(years[year]< 6.67):
            split_point = year
            print item + ", "+ split_point
            break
        else:
            continue

#sums from that key to then end of list
country_index = csv.reader(open('country_tipping_points.txt'), delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

country_dict ={}
for community in country_index:
    country_dict[community[0]] = int(community[1])

#sums from the beginning up to the tipping point (but not including)
country_list = {}
for item in country_dict.iterkeys():
    tipping_point = country_dict[item]
    years = sorted(temp_dic[item])
    pre_basic_diffusion_number =[(int(x),y) for x,y in temp_dic[item].iteritems() if int(x)< tipping_point]
    post_basic_diffusion_number=[(int(x),y) for x,y in temp_dic[item].iteritems() if int(x) >= tipping_point]
    country_list[item] = {"pre_basic_diffusion_number": pre_basic_diffusion_number, "post_basic_diffusion_number": post_basic_diffusion_number}

#country list with before and after scenarios
#do the time series forecasts versus actual
train_data = country_list['Albania']['pre_basic_diffusion_number']
test_data = country_list['Albania']['post_basic_diffusion_number']


#test the train_data predicted growth from standard time_series libraries
difference = 0.0
for item in country_list:
    #take this list 1) sort it 2) save the average
    before_list = country_list[item]['pre_basic_diffusion_number']
    average = 0.0
    max = 2001
    time_series1 = {}
    doc = 'C:\Documents and Settings\Luke\Desktop\\bullwhipped\out\%s_train.csv' % (item)
    f = csv.writer(open(doc,'wb'), delimiter =',', quotechar='\'', quoting=csv.QUOTE_MINIMAL)
    for record in before_list:
        year = record[0]
        growth_pct = record[1]
        time_series1[year] = growth_pct
        sum_series1 = sum(time_series1.itervalues())
        avg_series1 = sum_series1/len(time_series1)
        f.writerow([year, time_series1[year]])


    #take this list 1) sort it 2) save the average 3) write to file
    doc = 'C:\Documents and Settings\Luke\Desktop\\bullwhipped\out\%s_test.csv' % (item)
    f = csv.writer(open(doc,'wb'), delimiter =',', quotechar='\'', quoting=csv.QUOTE_MINIMAL)
    after_list = country_list[item]['post_basic_diffusion_number']
    time_series2 = {}
    for record in after_list:
        year = record[0]
        growth_pct = record[1]
        time_series2[year] = growth_pct
        sum_series2 = sum(time_series2.itervalues())
        avg_series2 = sum_series2/len(time_series2)
        f.writerow([year, time_series2[year]])

    #compare the average
    print item + " " + str(avg_series1) + ',' + str(avg_series2)
    if(avg_series2 !=0):
        difference += avg_series2/avg_series1
    else:
        continue

growth_factor = difference/len(country_dict)





if __name__ == '__main__':
    main()
