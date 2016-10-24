'''
arXiv-scatter.py --- 16 June 2016
-------------------------------------------------
This script has been coded for Python 2.7

Visualize article data using a LSI model with two topics.

Uses dictionary from  arXiv-genDictionary.py,
Uses corpus from  arXiv-genCorpus.py,
Uses LSI model from arXiv-genLSIModel.py

'''
#################################################################################################
## load some packages
#################################################################################################
print( 'Loading modules ... ')
from gensim import corpora, models, similarities
try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET
import obo
import logging
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
import os.path
import matplotlib.pyplot as plt 
import mpld3

#################################################################################################
## load LSI model
#################################################################################################
Nfeat=2
print( '\nLoading LSI model with {} features ... '.format(Nfeat))
fname='model_{}feature.lsi'.format(Nfeat)
path=os.path.dirname(os.getcwd())+'\\OBJ\\LSI\\'+fname
lsi = models.LsiModel.load(path)

#print( '\nLoading TFIDF model with {} features ... '.format(Nfeat))
#fname='model_{}feature.tfidf'.format(Nfeat)
#path=os.path.dirname(os.getcwd())+'\\OBJ\\LSI\\'+fname
#tfidf = models.TfidfModel.load(path)

#################################################################################################
## load dictionary and corpus
#################################################################################################
print( '\nLoading dictionary and corpus ...')
root=os.path.dirname(os.getcwd())+'\\OBJ\\LSI\\'
dictionary = corpora.Dictionary.load(root+'fullDictionary.dict')
corpus = corpora.MmCorpus(root+'fullCorpus.mm')
print(corpus)

#################################################################################################
## Load article data and find overlap with LSI topics
#################################################################################################
years=range(1992,1995)
years=range(1995,1998)
years=range(1998,2001)
years=range(2001,2004)
years=range(2004,2007)
years=range(2007,2010)
years=range(2010,2013)
years=range(2013,2017)
print( '\nLoading article data for years {} to {} ... '.format(years[0], years[-1]) )
scoreList, title = [],[]
for year in years:
	fname='arXiv-meta-{}.xml'.format(year)
	path=os.path.dirname(os.getcwd())+'\\DATA\\'+fname
	for event, elem in ET.iterparse(path): 
		if elem.tag == 'description':			
			query=elem.text
			queryStripped=obo.removeStopwords(obo.stripNonAlphaNum(query),obo.stopwords)
			vec_bow = dictionary.doc2bow(queryStripped)
			vec_lsi = lsi[vec_bow]
			score=(vec_lsi[0][1], vec_lsi[1][1])
			scoreList.append(score)
		if elem.tag == 'title':
			title.append(elem.text)
x=[a[0] for a in scoreList]
y=[a[1] for a in scoreList]

#################################################################################################
## Create scatter plot of articles projected onto LSI topics
#################################################################################################
print( '\nGenerating scatter plot of data for years {} to {} ... '.format(years[0], years[-1]) )
fig, ax = plt.subplots(subplot_kw=dict(axisbg='#EEEEEE'),figsize=(18, 12))
scatter = ax.scatter(x, y,                                         
                     alpha=0.3,
                     cmap=plt.cm.jet)
ax.grid(color='white', linestyle='solid')
ax.set_xlim([-1,8]), ax.set_ylim([-6,6])
ax.set_title("Scatter of arXiv:quant-ph papers ({} to {})".format(years[0],years[-1]), size=20)
ax.set_xlabel('LSI topic 1')
ax.set_ylabel('LSI topic 2')
## tooltips!
labels = title
tooltip = mpld3.plugins.PointLabelTooltip(scatter, labels=labels)
mpld3.plugins.connect(fig, tooltip)

#################################################################################################
## Display results
#################################################################################################
print('\nLSI topics:\n')
print lsi.show_topic(0,topn=10)
print('\n')
print lsi.show_topic(1,topn=10)
print('\n')
mpld3.show()

