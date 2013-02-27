#-------------------------------------------------------------------------------
# Name:        treepredcit
# Purpose:       
#
# Author:      Toby Segaran in Programming Collective Intelligence
#
# Created:     17/04/2012
# Copyright:   (c) Luke 2012
# Licence:     GPL
#-------------------------------------------------------------------------------
#!/usr/bin/env python

def main():
    pass

from PIL import Image,ImageDraw
import nltk

#reads a data object

# reads in a data object
# Tableau Software.?Tale of 100?. Tablau Software company web site.  http://www.tableausoftware.com/public/gallery/taleof100, accessed March 2012.
#company,founded_year, timeTo50million, timeOf50millin, industry, market1, market2, reached500million
company_data=[['Activision',1979, 4, 1983,'video games','gaming','None','Yes'],
['Actuate',1993,7,2000,'software','business intelligence','None','No'],
['Adobe',1982,6,1988,'software','document management','None','Yes'],
['Advent',1983,15,1998,'private equity','investment','None','No'],
['ANSYS',1970,26,1996,'software','engineering simulation','None','No'],
['Art Technology',1991,10,2001,'software','on demand optimization','None','No'],
['Autodesk',1982,5,1987,'software','design software','None','Yes'],
['Blackbaud',1982,17,1999,'software','fundraising','None','No'],
['Blackboard',1997,5,2002,'software ','education','None','Yes'],
['BMC',1980,8,1988,'software','business intelligence','None','Yes'],
['CA',1974,9,1983,'software','business intelligence','None','Yes'],
['Cadence',1983,6,1989,'software','design software','None','No'],
['Checkpoint',1993,5,1998,'security','security ','None','No'],
['China Digital',2004,4,2008,'software','IT Services','None','yes'],
['CIBER',1974,20,1994,'IT','consulting','None','Yes'],
['Citrix',1989,8,1997,'software','software','None','Yes'],
['Cognizant',1994,5,1999,'IT','consulting','None','Yes'],
['CommVault',1996,8,2004,'software','business intelligence','None','No'],
['Compuware',1973,12,1985,'software','IT Services','None','Yes'],
['Concur',1993,10,2003,'software','SaaS','None','No'],
['Deltek',1983,15,1998,'software','business intelligence','None','No'],
['DemandTec',1999,10,2009,'software','SaaS','None','No'],
['Digital River',1994,8,2002,'software, Hardware','IT Services','None','No'],
['DivX',2000,7,2007,'software','Video Content Delivery','None','No'],
['Echelon',1989,11,2000,'hardware','network hardware','None','No'],
['Electronic Arts',1982,6,1988,'video games','gaming','None','Yes'],
['EPIQ',1988,16,2004,'tech solutions','legal consulting','None','No'],
['i2',1989,8,1997,'software','supply chain','None','No'],
['Informatica',1993,7,2000,'software','data warehousing','None','No'],
['International Game',1971,10,1981,'hardware, software','gaming','None','Yes'],
['Interwoven',1995,6,2001,'software','content management system','None','No'],
['Intuit',1983,8,1991,'software','business software','None','Yes'],
['JDA',1985,12,1997,'software','business software','consulting','Yes'],
['LongTop',1996,12,2008,'software','trading applications','None','No'],
['Macrovision',1983,17,2000,'hardware, software','Video Content Delivery','Video Hardware','No'],
['Manhattan Assoc',1990,9,1999,'software','supply chain','None','No'],
['McAfee',1989,6,1995,'security','security','None','Yes'],
['MedAssets',1999,5,2004,'hardware, software','IT Services','business hardware','Yes'],
['Mentor Graphics',1981,4,1985,'software','design software','None','Yes'],
['MICROS',1977,14,1991,'hardware, software','point of sale software','business hardware','Yes'],
['Microsoft',1975,8,1983,'software','operating system','business software','Yes'],
['MicroStrategy',1989,9,1998,'software','business intelligence','None','Yes'],
['MSC Software',1963,25,1988,'software','design software','None','No'],
['National Instruments',1976,14,1990,'software','business software','None','Yes'],
['Netezza',2000,8,2008,'software, hardware','data warehousing','None','No'],
['Nice Systems',1986,11,1997,'software','security','None','Yes'],
['Novell',1983,3,1986,'software','business network software','None','Yes'],
['Nuance',1992,9,2001,'software','consulting','speech recognition','Yes'],
['Omniture',1996,11,2007,'software','marketing and analytics','None','No'],
['Open Text',1991,8,1999,'software','business content management','None','Yes'],
['OpenTV',1996,6,2002,'software','Video device Operating System','None','No'],
['OPNET',1986,17,2003,'software','network analytics','None','No'],
['Oracle',1977,10,1987,'hardware, software','business software','business hardware','Yes'],
['Parametric',1985,7,1992,'software','product development software','design software','Yes'],
['Pegasystems',1983,15,1998,'software','product development software','None','No'],
['Progress',1981,10,1991,'software','business software','None','Yes'],
['Quality Systems',1974,29,2003,'software','IT Services','None','No'],
['Quest',1987,13,2000,'unknown','none','None','Yes'],
['Rackspace',1998,6,2004,'hardware','IT Services','None','Yes'],
['RealNetworks',1994,5,1999,'software','audio content delivery','video content delivery','No'],
['RedHat',1993,9,2002,'software','operating system','business software','Yes'],
['Renaissance Learning',1986,13,1999,'software','education','None','No'],
['Retalix',1982,20,2002,'software','point of sale software','None','No'],
['Salesforce',1999,5,2004,'software','customer relationship management','platform as a service','Yes'],
['Sourcefire',2001,7,2008,'software, hardware','security','business hardware','No'],
['SPSS',1975,14,1989,'software','analytics','research','No'],
['SuccessFactors',2001,7,2008,'software','business software','None','No'],
['SuperMicro',1993,9,2002,'hardware','business hardware','None','Yes'],
['Sybase',1984,6,1990,'software','business software','None','Yes'],
['Symantec',1982,8,1990,'software','security','None','Yes'],
['Synaptics',1986,15,2001,'hardware','user interface','None','Yes'],
['Synopsys',1986,6,1992,'software, programming','design software','design hardware','Yes'],
['Take-Two',1993,6,1999,'video games','gaming','None','Yes'],
['TeleCom Systems',1987,13,2000,'unknown','none','None','No'],
['Taleo',1999,6,2005,'software','recruiting','staff management','No'],
['Ultimate Software',1990,9,1999,'software','staff management','None','No'],
['VanceInfo',1995,13,2008,'software','IT systems','None','No'],
['VASCO',1991,15,2006,'softwaer','security','None','No'],
['Verisign',1995,4,1999,'internet','security','business software','Yes'],
['Websense',1994,9,2003,'software','content management system','None','No'],
['Wind River',1983,14,1997,'software','operating systems','business software','No']]



class decisionnode:
    def __init__(self,col=-1,value=None,results=None,tb=None,fb=None):
        self.col=col
        self.value=value
        self.results=results
        self.tb=tb
        self.fb=fb

# Divides a set on a specific column. Can handle numeric
# or nominal values

def divideset(rows,column,value):
   # Make a function that tells us if a row is in
   # the first group (true) or the second group (false)

   split_function=None
   if isinstance(value,int) or isinstance(value,float):
      split_function=lambda row:row[column]>=value
   else:
      split_function=lambda row:row[column]==value

   # Divide the rows into two sets and return them
   set1=[row for row in rows if split_function(row)]
   set2=[row for row in rows if not split_function(row)]
   return (set1,set2)

# Create counts of possible results (the last column of
# each row is the result)
def uniquecounts(rows):
   results={}
   for row in rows:
      # The result is the last column
      r=row[len(row)-1]
      if r not in results: results[r]=0
      results[r]+=1
   return results

# Probability that a randomly placed item will
# be in the wrong category
def giniimpurity(rows):
  total=len(rows)
  counts=uniquecounts(rows)
  imp=0
  for k1 in counts:
    p1=float(counts[k1])/total
    for k2 in counts:
      if k1==k2: continue
      p2=float(counts[k2])/total
      imp+=p1*p2
  return imp

# Entropy is the sum of p(x)log(p(x)) across all
# the different possible results
def entropy(rows):
   from math import log
   log2=lambda x:log(x)/log(2)
   results=uniquecounts(rows)
   # Now calculate the entropy
   ent=0.0
   for r in results.keys(  ):
      p=float(results[r])/len(rows)
      ent=ent-p*log2(p)
   return ent

def buildtree(rows,scoref=entropy):
  if len(rows)==0: return decisionnode(  )
  current_score=scoref(rows)

  # Set up some variables to track the best criteria
  best_gain=0.0
  best_criteria=None
  best_sets=None

  column_count=len(rows[0])-1
  for col in range(0,column_count):
    # Generate the list of different values in
    # this column
    column_values={}
    for row in rows:
       column_values[row[col]]=1
    # Now try dividing the rows up for each value
    # in this column
    for value in column_values.keys(  ):
      (set1,set2)=divideset(rows,col,value)

      # Information gain
      p=float(len(set1))/len(rows)
      gain=current_score-p*scoref(set1)-(1-p)*scoref(set2)
      if gain>best_gain and len(set1)>0 and len(set2)>0:
        best_gain=gain
        best_criteria=(col,value)
        best_sets=(set1,set2)

  # Create the sub-branches
  if best_gain>0:
    trueBranch=buildtree(best_sets[0])
    falseBranch=buildtree(best_sets[1])
    return decisionnode(col=best_criteria[0],value=best_criteria[1],
                        tb=trueBranch,fb=falseBranch)
  else:
    return decisionnode(results=uniquecounts(rows))

def printtree(tree,indent=''):
   # Is this a leaf node?
   if tree.results!=None:
      print str(tree.results)
   else:
      # Print the criteria
      print str(tree.col)+':'+str(tree.value)+'? '

      # Print the branches
      print indent+'T->',
      printtree(tree.tb,indent+'  ')
      print indent+'F->',
      printtree(tree.fb,indent+'  ')

def getwidth(tree):
  if tree.tb==None and tree.fb==None: return 1
  return getwidth(tree.tb)+getwidth(tree.fb)

def getdepth(tree):
  if tree.tb==None and tree.fb==None: return 0
  return max(getdepth(tree.tb),getdepth(tree.fb))+1

#Draws the decision tree , *remember to add a directory path in function argument
def drawtree(tree,jpeg='tree.jpg'):
  w=getwidth(tree)*100
  h=getdepth(tree)*100+120

  img=Image.new('RGB',(w,h),(255,255,255))
  draw=ImageDraw.Draw(img)

  drawnode(draw,tree,w/2,20)
  img.save(jpeg,'JPEG')


def drawnode(draw,tree,x,y):
  if tree.results==None:
    # Get the width of each branch
    w1=getwidth(tree.fb)*100
    w2=getwidth(tree.tb)*100

    # Determine the total space required by this node
    left=x-(w1+w2)/2
    right=x+(w1+w2)/2

    # Draw the condition string
    draw.text((x-20,y-10),str(tree.col)+':'+str(tree.value),(0,0,0))

    # Draw links to the branches
    draw.line((x,y,left+w1/2,y+100),fill=(255,0,0))
    draw.line((x,y,right-w2/2,y+100),fill=(255,0,0))

    # Draw the branch nodes
    drawnode(draw,tree.fb,left+w1/2,y+100)
    drawnode(draw,tree.tb,right-w2/2,y+100)
  else:
    txt=' \n'.join(['%s:%d'%v for v in tree.results.items()])
    draw.text((x-20,y),txt,(0,0,0))

def classify(observation,tree):
  if tree.results!=None:
    return tree.results
  else:
    v=observation[tree.col]
    branch=None
    if isinstance(v,int) or isinstance(v,float):
      if v>=tree.value: branch=tree.tb
      else: branch=tree.fb
    else:
      if v==tree.value: branch=tree.tb
      else: branch=tree.fb
    return classify(observation,branch)

def prune(tree,mingain):
  # If the branches aren't leaves, then prune them
  if tree.tb.results==None:
    prune(tree.tb,mingain)
  if tree.fb.results==None:
    prune(tree.fb,mingain)

  # If both the subbranches are now leaves, see if they
  # should merged
  if tree.tb.results!=None and tree.fb.results!=None:
    # Build a combined dataset
    tb,fb=[],[]
    for v,c in tree.tb.results.items(  ):
      tb+=[[v]]*c
    for v,c in tree.fb.results.items(  ):
      fb+=[[v]]*c

# Test the reduction in entropy
    delta=entropy(tb+fb)-(entropy(tb)+entropy(fb)/2)
    if delta<mingain:
      # Merge the branches
      tree.tb,tree.fb=None,None
      tree.results=uniquecounts(tb+fb)

def mdclassify(observation,tree):
  if tree.results!=None:
    return tree.results
  else:
    v=observation[tree.col]
    if v==None:
      tr,fr=mdclassify(observation,tree.tb),mdclassify(observation,tree.fb)
      tcount=sum(tr.values(  ))
      fcount=sum(fr.values(  ))
      tw=float(tcount)/(tcount+fcount)
      fw=float(fcount)/(tcount+fcount)
      result={}
      for k,v in tr.items(): result[k]=v*tw
      for k,v in fr.items(): result[k]=result.setdefault(k,0)+(v*fw)
      return result
    else:
      if isinstance(v,int) or isinstance(v,float):
        if v>=tree.value: branch=tree.tb
        else: branch=tree.fb
      else:
        if v==tree.value: branch=tree.tb
        else: branch=tree.fb
      return mdclassify(observation,branch)

def variance(rows):
  if len(rows)==0: return 0
  data=[float(row[len(row)-1]) for row in rows]
  mean=sum(data)/len(data)
  variance=sum([(d-mean)**2 for d in data])/len(data)
  return variance

if __name__ == '__main__':
    main()
