'''
arXiv-score.py --- 16 June 2016
-------------------------------------------------
This script has been coded for Python 2.7

Uses dictionary from  arXiv-genDictionary.py,
Uses corpus from  arXiv-genCorpus.py,
Uses LSI model from arXiv-genLSIModel.py

'''

#################################################################################################
## load some packages
#################################################################################################
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
import os.path


#################################################################################################
## load LSI model
#################################################################################################
Nfeat=200 #2,10,20, 30,100(seems to have problems above 100 topics)
print( '\nLoading LSI model with {} features ... '.format(Nfeat))
fname='model_{}feature.lsi'.format(Nfeat)
path=os.path.dirname(os.getcwd())+'\\OBJ\\LSI\\'+fname
lsi = models.LsiModel.load(path)

print( '\nLoading TFIDF model with {} features ... '.format(Nfeat))
fname='model_{}feature.tfidf'.format(Nfeat)
path=os.path.dirname(os.getcwd())+'\\OBJ\\LSI\\'+fname
tfidf = models.TfidfModel.load(path)

#################################################################################################
## load dictionary and corpus
#################################################################################################
print( '\nLoading dictionary and corpus ...')
root=os.path.dirname(os.getcwd())+'\\OBJ\\LSI\\'
dictionary = corpora.Dictionary.load(root+'fullDictionary.dict')
corpus = corpora.MmCorpus(root+'fullCorpus.mm')
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

#################################################################################################
## regenerate corpus LSI representation
#################################################################################################
print( '\nRegenerating corpus in LSI representation ...')
#tfidf = models.TfidfModel(corpus)
corpus_tfidf = tfidf[corpus]
corpus_lsi = lsi[corpus_tfidf]

#################################################################################################
## extract weight distribution for each document AND find highest weighted topic?
#################################################################################################
print( '\nExtracting weight of each document ...')
scoreList, dArr = [],[]
for doc in corpus_lsi:
	score=[x[1] for x in doc]	
	scoreList.append(score)		

#################################################################################################
## calculate score per year
#################################################################################################
print( '\nCalculating score for each topic per year ...')
i=-1
xx1,xx2=[],[]
years=range(1992,2017)
for year in years:	# per year
	print(year)
	scoreYear1=np.zeros(Nfeat) # score 1: average across all articles for a given topic
	scoreYear2=np.zeros(Nfeat) # score 2: average of abs value 

	ii=-1
	fname ='arXiv-meta-{}.xml'.format(year)
	path=os.path.dirname(os.getcwd())+'\\DATA\\'+fname	
	for event, elem in ET.iterparse(path): # per topic		
		if elem.tag == 'title': # if record found
			#title.append(elem.text)		
			i+=1
			ii+=1
			scoreYear1=scoreYear1+np.asarray(scoreList[i]) # running sum of weights per topic in this year
			scoreYear2=scoreYear2+abs(np.asarray(scoreList[i]))						
	xx1.append( list(scoreYear1/(ii+1.) ) ) # average weight per topic this year
	xx2.append( list(scoreYear2/(ii+1.) ) ) 	

#################################################################################################
## pickle
#################################################################################################
print( '\nSaving scores to file ...')
root=os.path.dirname(os.getcwd())+'\\OBJ\\LSI\\'
with open(root+ 'scores1_{}feature'.format(Nfeat) + '.pkl', 'wb') as f:
	pickle.dump(xx1, f, pickle.HIGHEST_PROTOCOL)
with open(root+ 'scores2_{}feature'.format(Nfeat) + '.pkl', 'wb') as f:
	pickle.dump(xx1, f, pickle.HIGHEST_PROTOCOL)
print( 'Finished!')