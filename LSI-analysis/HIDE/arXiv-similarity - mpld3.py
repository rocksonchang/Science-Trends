'''
arXiv-similarity.py --- 16 June 2016
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
from datetime import datetime
import numpy as np
import os.path
from math import ceil, floor

#################################################################################################
## load LSI model
#################################################################################################
Nfeat=100 #2,10,20, 30,100(seems to have problems above 100 topics)
print( '\nLoading LSI model with {} features ... '.format(Nfeat))
fname='model_{}feature.lsi'.format(Nfeat)
path=os.path.dirname(os.getcwd())+'\\OBJ\\LSI\\'+fname
lsi = models.LsiModel.load(path)

#################################################################################################
## Load dictionary and corpus
#################################################################################################
print( '\nLoading dictionary and corpus ... ')
fname ='fullDictionary.dict' 
path=os.path.dirname(os.getcwd())+'\\OBJ\\LSI\\'+fname
dictionary = corpora.Dictionary.load(path)

root=os.path.dirname(os.getcwd())+'\\OBJ\\LSI\\'
corpus = corpora.MmCorpus(root+'fullCorpus.mm')

#################################################################################################
## Index corpus and save
#################################################################################################
print( '\nCreating corpus index ... ')
#index = similarities.MatrixSimilarity( lsi[corpus] ) # transform corpus to LSI space and index it
fname='corpus.index'
path=os.path.dirname(os.getcwd())+'\\OBJ\\LSI\\'+fname
#index.save(path)
index = similarities.MatrixSimilarity.load(path)

#################################################################################################
## Pull article titles
#################################################################################################
years=range(1992,2017)
print( '\nLoading article data for years {} to {} ... '.format(years[0], years[-1]) )
titles, dates = [], []
for year in years:
	fname='arXiv-meta-{}.xml'.format(year)
	path=os.path.dirname(os.getcwd())+'\\DATA\\'+fname
	for event, elem in ET.iterparse(path): 		
		if elem.tag == 'title':
			titles.append(elem.text)
		if elem.tag == 'date':
			dates.append(elem.text)
## convert date
Q=[]
for date in dates:
	data=datetime.strptime(date,'%Y-%m-%d')			
	Q.append(data.year+data.month/12.)	

#################################################################################################
## setup query
#################################################################################################
query = "Error correction"
query = "mott insulator phase transition"
#query = "The response of a particle in a periodic potential effective mass condensate"
vec_bow = dictionary.doc2bow( obo.removeStopwords(obo.stripNonAlphaNum(query),obo.stopwords) )
vec_lsi = lsi[vec_bow]
sims = index[vec_lsi] # perform a similarity query against the corpus
sims = sorted(enumerate(sims), key=lambda item: -item[1])
print '\n'
print 'QUERY: ' + query
Ntop=30
print 'TOP {} hits: '.format(Ntop) + query
#for s in sims[:Ntop]:
	#print s, title[s[0]]
## prepare data for plotting -- article index, score, date, title
iArr=[x[0] for x in sims[:Ntop]] 
sArr=[x[1] for x in sims[:Ntop]]	
xArr=[Q[i] for i in iArr]
labels=[titles[i] for i in iArr]

#################################################################################################
## Create scatter plot of articles projected onto LSI topics
#################################################################################################
print( '\nGenerating scatter plot of data for years {} to {} ... '.format(years[0], years[-1]) )
fig, ax = plt.subplots(2, subplot_kw=dict(axisbg='#EEEEEE'),figsize=(12, 12))
scatter = ax[0].scatter(xArr, sArr,                                         
                     alpha=0.3,
                     cmap=plt.cm.jet)
ax[0].grid(color='white', linestyle='solid')
ax[0].set_xlim([1992,2016]), ax[0].set_ylim([0,1])
ax[0].set_title("Scatter of arXiv:quant-ph papers matching query: " + query, size=20)
ax[0].set_xlabel('Submission date')
ax[0].set_ylabel('Similarity score')
## tooltips!
tooltip = mpld3.plugins.PointLabelTooltip(scatter, labels=labels)
mpld3.plugins.connect(fig, tooltip)

#################################################################################################
## Create scatter plot of articles projected onto LSI topics
#################################################################################################
years=range(1992,2017)
sYear=np.zeros(len(years))
for x,s in zip(xArr,sArr):
	xInd=floor(x-1992)
	sYear[xInd] += s
ax[1].bar(years,sYear)
ax[1].set_xlim([1992,2016])
ax[1].set_xlabel('Submission year')
ax[1].set_ylabel('Sum of scores')

mpld3.show()

