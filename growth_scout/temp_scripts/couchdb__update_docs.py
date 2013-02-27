#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      Luke
#
# Created:     10/08/2012
# Copyright:   (c) Luke 2012
# Licence:     <your licence>
#-------------------------------------------------------------------------------
#!/usr/bin/env python
# template code from http://segfault.in/2010/11/playing-with-python-and-couchdb/

import couchdb
from couchdb.client import Server, Document
from couchdb.mapping import TextField, DateTimeField, ListField
from couchdb.design import ViewDefinition

server = couchdb.Server('http://localhost:5984')
db = server['jobtobedone_test']

# get list of databases
for db in server:
    print db

# get documents within database
for docid in db:
    eml = db.get(docid)

some_dic = {}

for adoc in some_dic.keys():
    doc = db.get(adoc)
    doc['sent_type'] = some_dic[adoc]
    db.save(doc)


#not currently working
rows = db.view('_all_docs', keys=['key1', 'key2', 'missing'], include_docs=True)
docs = [row.doc for row in rows]

#create a view
    #pass javascript
code = '''function(doc) { if(doc.frm == "vinod@example.com") emit(doc.frm, null); }'''
results = db.query(code)

for res in results:
   print res.key

rpt_view = ViewDefinition('reports', 'fromemail', '''function(doc) { if(doc.frm == "vinod@example.com") emit(doc.frm, null); }''')
rpt_view.sync(db)

for res in db.view("_design/reports/_view/fromemail"):
        print res.id, res.key

#class of document for updating
class Jobtobedone(Document):
  frm  = TextField()
  to = ListField(TextField())
  sub = TextField()
  added = DateTimeField(default=datetime.now())

