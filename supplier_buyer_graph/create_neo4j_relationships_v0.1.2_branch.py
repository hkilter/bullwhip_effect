#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      Luke
#
# Created:     12/11/2012
# Copyright:   (c) Luke 2012
# Licence:     <your licence>
#-------------------------------------------------------------------------------
#!/usr/bin/env python

from py2neo import neo4j
from py2neo import gremlin
import string, os, csv
import simplejson as json

def main():
    pass

#change to present working directory
os.chdir('C:\Documents and Settings\Luke\Desktop\supplier_buyer_graph')

#database connection
db = neo4j.GraphDatabaseService("http://ec2-23-21-228-70.compute-1.amazonaws.com:7474/db/data/")

#dictionary of all of the nodes
neo_index = csv.reader(open('graph_nodes.txt'), delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

neo_dict ={}

for company in neo_index:
    neo_dict[company[0]] = int(company[1])

table = csv.reader(open('relationships.csv'), delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
next(table)

for row in table:
    try:
        #subject
        user = "%s" % (row[0])
        node_start = neo_dict[user]

        #object
        user_sells = row[12]
        user_buys = row[13]
        strategy = row[2]

        #predicates
        #may be plural
        supplier_to = 'supply_of'
        buyer_of = 'buyer_of'

        #create lists from csv
        reader = csv.reader([user_sells], delimiter=',',skipinitialspace=True)
        for r in reader:
            seller_list = r

        reader2 = csv.reader([user_buys], delimiter=',',skipinitialspace=True)
        for r in reader2:
            buyer_list = r

        #simulation of relationships
            #global variables
            num_disruptive_range_business = 21
            total_disruptive_range_capital = 4301
            landline_population= 1000000000
            wireless_population= 4700000000

            #get the properties of the starting node, get the properties of the ending node
            #case or if/then add_link
            b = db.get_node(node_start)
            temp_dict = b.get_properties()
            model = temp_dict['b2b_b2c']
            name = temp_dict['name']
            start_role = temp_dict['roles']
            starting_funds= temp_dict['starting_funds_millions']
            business_model = temp_dict['strategy_name']
            #if the business is disruptive range, it needs funds to survive
            LINK_VARIANCE = starting_funds*30
            LINK_MAX = (float((LINK_VARIANCE)/total_disruptive_range_capital)) * num_disruptive_range_business

            def draw_consumer_links(node_start, seller_list, buyer_list, business_model, start_role):
                for buyer in seller_list:
                    node_end = neo_dict[buyer]
                    gremlin_script = "g.addEdge(g.v(%s),g.v(%s), 'supplier_of', [name: '%s'])" % (node_start, node_end, buyer)
                    print gremlin_script
                    #gremlin.execute(gremlin_script, db)

                link_count = 0
                for seller in buyer_list:
                    strategy_table = csv.reader(open('graph_strategy.txt'), delimiter='\t',  quotechar='"', quoting=csv.QUOTE_MINIMAL)
                    for item in strategy_table:
                        node_end = item[0]
                        b_c = db.get_node(node_end)
                        b_c_dict = b_c.get_properties()
                        b2b_b2c = b_c_dict['b2b_b2c']
                        role = b_c_dict['roles']
                        if((item[1]== business_model) and (node_start != node_end) and (b2b_b2c =='B' or b2b_b2c=='B, C') and (role !='network')):
                            node_start = str(node_start)
                            if(business_model =='Disruptive Range' and (link_count >= LINK_MAX)):
                                break
                            else:
                                continue
                            gremlin_script2 = "g.addEdge(g.v(%s), g.v(%s), 'buyer_of', ['name': '%s') " % (node_start, node_end, seller)
                            link_count = link_count + 1
                            print gremlin_script2
                            #gremlin.execute(gremlin_script2, db)
                        else:
                            continue
                return


            def draw_business_links(node_start, seller_list, buyer_list):
                return

            if model =='B':
                draw_business_links(node_start, seller_list, buyer_list)
            elif model=='C':
                draw_consumer_links(node_start, seller_list, buyer_list, business_model, start_role)
            else:
                draw_business_links(node_start, seller_list, buyer_list)
                draw_consumer_links(node_start, seller_list, buyer_list, business_model, start_role)
    except:
        print "error" + user
        continue


if __name__ == '__main__':
    main()
