import cgi
import datetime
import urllib
import webapp2#from google.appengine.ext import webapp
#from google.appengine.ext.webapp.util import run_wsgi_app
import re
from google.appengine.ext import db
from google.appengine.api import users
from google.appengine.ext.db import stats
from math import sqrt

import logging
from urlparse import urljoin

import index
import trainingData

# set of movies
m_list=['Avengers','The Dark Knight','Iron Man','Fight Club','Bourne Ultimatum',
        'Twilight','The Notebook','Titanic','Pride and Prejudice','Bridesmaid',
        'American Pie','The Hangover','Horrible Bosses','Delhi Belly',
        'Inception','The Prestige','The Illusionist','Sherlock Holmes','Usual Suspects',
        'Harry Potter','The Hobbit','Avatar','Life of Pie','Spider Man'
        ]
flag=0

# Euclidian distance similarity metric
def sim_distance(prefs,person1,person2):
    # Get the list of shared_items
    sum_of_squares=0
    for item in prefs[person1]:
        if item in prefs[person2]:
            sum_of_squares=sum_of_squares+(prefs[person1][item]-prefs[person2][item])**2
    return 1/(1+sum_of_squares)

# Pearson correlation coefficient for p1 and p2
def sim_pearson(prefs,p1,p2):
    # Get the list of mutually rated items
    si={}
    for item in prefs[p1]:
        if item in prefs[p2]: si[item]=1

    #number of similar elements
    n=len(si)

    #if they are no ratings in common, return 0
    if n==0:
        return 0

    #PCC = COV(A,B)/ SD(A)*SD(B)
    #COV(A,B)= E(A.B) - E(A).E(B)   ->for a random variable, if each outcome is equally probable(ie., 1/n) then Expected value= MEAN
    
    sumA=sum([prefs[p1][it] for it in si])
    sumB=sum([prefs[p2][it] for it in si])
    pSum=sum([prefs[p1][it]*prefs[p2][it] for it in si]) #productsum(A.B)
    
    sumASq=sum([pow(prefs[p1][it],2) for it in si])
    sumBSq=sum([pow(prefs[p2][it],2) for it in si])
    

    COV=float(pSum-sumA*sumB)/(n)
    SDA=float(sumASq-pow(sumA,2))/(n)
    SDB=float(sumBSq-pow(sumB,2))/(n)

    if SDA==0 or SDB==0 or COV==0: return 0.01
         
    pcc=COV/(SDA*SDB)
    return pcc

#Find top n similar tupples, for a given tupple
def topMatches(prefs,similarity,person,n):
    scores=[]
    for p in prefs:
        if p != person:
            scores.append([similarity(prefs,p,person),p])
    scores.sort()
    scores.reverse()
    return scores[0:n]

#Find top n similar tupples, for each tupple
def SimilarItems(Table,n):      #Table = 2D dictionary like userFeatureTable
    result={}
    for item in Table:
        scores=topMatches(Table,sim_pearson,item,n)# Find the most n similar items to this one
        result[item]=scores
    return result

#input: Table,similarity function,username
#each tupple/entity represents a user
def getUserBased(prefs,similarity,person): 
    wtsum={}    #weighted sum   
    simsum={}   #similarity sum
    scores={}
    for p in prefs:
        if p==person: continue
        sim=similarity(prefs,p,person)      #Find similarity score of given user with every other user
        if sim<=0: continue  #ignore scores of zero or lower
        for it in prefs[p]:
            if it in prefs[person]:  continue
            if it not in wtsum: wtsum[it]=0.0   #total.setdefault(it,0)
            if it not in simsum: simsum[it]=0.0 #simSum.setdefault(it,0)
            wtsum[it]+=sim*prefs[p][it]
            simsum[it]+=sim

    #Normalize (weighted average)
    for it in wtsum:         
        if simsum[it]!=0:   scores[it] = wtsum[it]/simsum[it]
        else: scores[it]=0
    return scores

#-------------------------------------------------------
#Transform-> Now each tupple/entity represents an item.
def transformPrefs(prefs):
    result={}
    for person in prefs:
        for item in prefs[person]:
            if item not in result: result[item]={} #result.setdefault(item,{})
            result[item][person]=prefs[person][item]#Flip item and person
    return result

def calculateItemBasedRecom(prefs,SimItems,user):
    wtsum={}
    simsum={}
    scores={}
    for it in prefs[user]:           #movies rated by the user
        if it=='age'or it=='sex': continue
        for sit in SimItems[it]:     #similar items list [similarity score,movie]
            if sit[1] in prefs[user]: continue
            if sit[1] not in wtsum: wtsum[sit[1]]=0.0
            if sit[1] not in simsum: simsum[sit[1]]=0.0
            wtsum[sit[1]]+=sit[0]*prefs[user][it]
            simsum[sit[1]]+=sit[0]
        
    for it in wtsum:
        if simsum[it]!=0:   scores[it] = wtsum[it]/simsum[it]
        else: scores[it]=0
    return scores

def getItemBased(prefs,user,n):
    itemPrefs=transformPrefs(prefs)         #People who liked X also liked Y
    SimItems=SimilarItems(itemPrefs,n)
    scores=calculateItemBasedRecom(prefs,SimItems,user)
    return scores

def getContentBased(prefs, itemtags, user, n):
    SimItems=SimilarItems(itemtags,n)
    scores=calculateItemBasedRecom(prefs,SimItems,user)
    return scores

#-------------------------------------------------------
def getscoredlist(prefs, itemtags, user):
    totalscores=dict([(m,0) for m in itemtags])
    
    ubased=getUserBased(prefs,sim_pearson,user)
    ibased=getItemBased(prefs,user,10)      #find top n=10 similar items to each item while performing calculations
    cbased=getContentBased(prefs,itemtags,user,10)

    weights=[(1.0,ubased),
             (1.0,ibased),
             (1.0,cbased)]
        
    for (weight,scores) in weights:
        for m in itemtags:
            if m not in scores: continue    #scores only contain items not rated by user
            totalscores[m]+=weight*scores[m]
    return totalscores  #Note items rated by user got a score of 0 in totalscores.

#-------------------------------------------------------
class Critic(db.Model):
  name = db.StringProperty()
  feature = db.StringProperty() #age,sex,movie_names
  value = db.FloatProperty()    #feature value

class Tag(db.Model):
  movie = db.StringProperty()
  genre = db.StringProperty()
  share = db.FloatProperty()

def prepare_data():
    db.delete(Critic.all(keys_only=True))
    db.delete(Tag.all(keys_only=True))
    for p in trainingData.userFeatureTable:
        for f in trainingData.userFeatureTable[p]:
            element=Critic(key_name=p+f,name=p,feature=f,value=float(trainingData.userFeatureTable[p][f]))
            element.put()
    for m in trainingData.itemFeatureTable:
        for g in trainingData.itemFeatureTable[m]:
            element=Tag(key_name=m+g,movie=m,genre=g,share=float(trainingData.itemFeatureTable[m][g]))
            element.put()    
    
def table1_to_dic():
  q = Critic.all()
  prefs={}
  for e in q:#.run(limit=4):
    if e.name not in prefs: prefs[e.name]={}
    prefs[e.name][e.feature]=float(e.value)
  return prefs        

def table2_to_dic():
  q = Tag.all()
  itemtags={}
  for ob in q:
    if ob.movie not in itemtags: itemtags[ob.movie]={}
    itemtags[ob.movie][ob.genre]=float(ob.share)
  return itemtags

#-------------------------------------------------------------------------------------------------------
class MainPage(webapp2.RequestHandler):
  def get(self):
    global flag
    if flag==0:
        prepare_data()
        flag=1    
    self.response.out.write(index.a)

class Submit(webapp2.RequestHandler):
  def post(self):
    name1=cgi.escape(self.request.get('u_name'))
    age1=cgi.escape(self.request.get('age'))
    sex1=cgi.escape(self.request.get('sex'))
    movie1=cgi.escape(self.request.get('m_name'))
    rating1=cgi.escape(self.request.get('rating'))

    logging.info(name1+' '+age1+' '+sex1+' '+movie1+' '+rating1+'\n')

    name1='_'.join(name1.split())
    
    if name1=='username' or movie1=='from above list' or rating1=='out of 5' or age1=='age in years' or sex1=='sex':
        self.response.out.write('<h3>No Field should be empty</h3>')
        return

    itemtags=table2_to_dic()
    if float(age1)>100 or float(age1)<0 or float(rating1) >5 or float(rating1)<0 or (movie1 not in itemtags):
        self.response.out.write('<b><h2>Invalid entry!</h2></b>')
        return

    try:
        element=Critic(key_name=name1+'age', name=name1, feature='age' ,value=float(age1))
        element.put()
        element=Critic(key_name=name1+'sex', name=name1, feature='sex', value=float(sex1))
        element.put()
        element=Critic(key_name=name1+movie1, name=name1, feature=movie1, value=float(rating1))
        element.put()
        self.response.out.write('<b><h2>Entry successfull!</h2></b>')
    except:
        self.response.out.write('<b><h2>Could not enter data</h2></b>')

class get_recommendations(webapp2.RequestHandler):  
  def post(self):
    self.response.out.write('<html><body bgcolor="white"><b><h2>Recommendations</h2></b><pre>')
    user=cgi.escape(self.request.get('u_name'))
    prefs=table1_to_dic()
    itemtags=table2_to_dic()
    if user not in prefs:
        self.response.out.write('<b>Invalid username!</b>')
        return

    scores=getscoredlist(prefs,itemtags,user)      #{ m1: .94, m2: .34}
    rankedresults=sorted([(score,movie) for (movie, score) in scores.items()], reverse=1)
    for i in range(4):
        self.response.out.write(str(rankedresults[i][0])+' '+rankedresults[i][1]+'\n')
    self.response.out.write('</pre></body></html>')    

class View_ratings(webapp2.RequestHandler):  
  def post(self):
    self.response.out.write('<html><body bgcolor="white"><b><h2>Profile</h2></b><pre>')
    user=cgi.escape(self.request.get('u_name'))
    prefs=table1_to_dic()
    if user not in prefs:
        self.response.out.write('<b>Invalid username!</b>')
        return
    for f in prefs[user]:
        if f=='sex':
            if prefs[user][f]==0: self.response.out.write(f+'  '+'Male'+'\n')
            else: self.response.out.write(f+'  '+'Female'+'\n')
        else: self.response.out.write(f+'  '+str(prefs[user][f])+'\n')
                
app1 = webapp2.WSGIApplication([('/', MainPage),('/sub', Submit)],
                              debug=True)
app2 = webapp2.WSGIApplication([('/', MainPage),('/sign', View_ratings)],
                              debug=True)
app3 = webapp2.WSGIApplication([('/', MainPage),('/recom', get_recommendations)],
                              debug=True)
