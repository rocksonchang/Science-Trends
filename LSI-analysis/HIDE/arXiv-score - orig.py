#################################################################################################
#################################################################################################
## load some packages
from gensim import corpora, models, similarities
try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET
import obo
import logging
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
import matplotlib.pyplot as plt 
import mpld3
import numpy as np
import pickle

## load LSI model
Nfeat=20 #2,10,20, 30,100,300 (seems to have problems above 100 topics)
lsi = models.LsiModel.load('model_{}feature.lsi'.format(Nfeat))
## load dictionary and corppus
dictionary = corpora.Dictionary.load('fullDictionary.dict')
corpus = corpora.MmCorpus('fullCorpus.mm')
print(corpus)

## print topics
'''
lsi.print_topics(num_topics=50,num_words=8)
print('\n')
print lsi.show_topic(0,topn=50)
print('\n')
print lsi.show_topic(1,topn=50)
print('\n')
'''


print('\n')
years=range(1992,2017)
scores=[]
scores2=[]
title=[]

tfidf = models.TfidfModel(corpus)
corpus_tfidf = tfidf[corpus]
corpus_lsi = lsi[corpus_tfidf]

## extract weight distribution for each document
scoreList=[]
dArr=[]
for doc in corpus_lsi:
	score=[x[1] for x in doc]	
	scoreList.append(score)		
	d=dict(doc)
	sd=sorted(d,key=d.get,reverse=True)
	dArr.append( (sd[0],d[sd[0]]) )
for d in dArr[0:30]:
	print d


## calculate the average weight per topic per year
i=-1
xx1=[]
xx2=[]
for year in years:	# per year
	print(year)
	scoreYear1=np.zeros(Nfeat)
	scoreYear2=np.zeros(Nfeat)
	ii=-1
	for event, elem in ET.iterparse('RAW/arXiv-meta-{}.xml'.format(year)): # per topic
		#if elem.tag == 'description':						
		if elem.tag == 'title':
			#title.append(elem.text)		
			i+=1
			ii+=1
			scoreYear1=scoreYear1+np.asarray(scoreList[i]) # running sum of weights per topic in this year
			scoreYear2=scoreYear2+abs(np.asarray(scoreList[i]))						
	xx1.append( list(scoreYear1/(ii+1.) ) ) # average weight per topic this year
	xx2.append( list(scoreYear2/(ii+1.) ) ) 	

## pickle
with open('obj/'+ 'scoresA1_{}feature'.format(Nfeat) + '.pkl', 'wb') as f:
	pickle.dump(xx1, f, pickle.HIGHEST_PROTOCOL)
with open('obj/'+ 'scoresA2_{}feature'.format(Nfeat) + '.pkl', 'wb') as f:
	pickle.dump(xx1, f, pickle.HIGHEST_PROTOCOL)
