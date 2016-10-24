#################################################################################################
#################################################################################################
#from pprint import pprint  # pretty-printer

## load some packages
'''
from gensim import corpora, models, similarities
try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET
'''
from gensim import corpora, models, similarities
import logging
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

'''
## load dictionary, corpus - bag of words representation
dictionary = corpora.Dictionary.load('fullDictionary.dict')
corpus = corpora.MmCorpus('fullCorpus.mm')
print corpus

## Tfidf model
tfidf = models.TfidfModel(corpus)
corpus_tfidf = tfidf[corpus]
#for doc in corpus_tfidf:
    #print(doc)

## LSI model
lsi = models.LsiModel(corpus_tfidf, id2word=dictionary, num_topics=50) # initialize an LSI transformation
corpus_lsi = lsi[corpus_tfidf]

print '\n'
lsi.print_topics(50)
## save
lsi.save('model.lsi') # same for tfidf, lda, ...
'''

'''
## load article titles
title=[]
date=[]
years=range(1992,2017)
for year in years:       
    for event, elem in ET.iterparse('arXiv-meta-{}.xml'.format(year)): 
		if elem.tag == 'title':
			title.append(elem.text)
		if elem.tag == 'date':
			date.append(elem.text)

lsi = models.LsiModel.load('model.lsi')
lsi.print_topics(num_topics=50,num_words=8)

dictionary = corpora.Dictionary.load('fullDictionary.dict')
corpus = corpora.MmCorpus('fullCorpus.mm')
tfidf = models.TfidfModel(corpus)
corpus_tfidf = tfidf[corpus]
corpus_lsi = lsi[corpus_tfidf]
'''

'''
index = similarities.MatrixSimilarity(lsi[corpus])
index.save('simTest.index')
#index = similarities.MatrixSimilarity.load('/simTest.index')
'''
#lsi = models.LsiModel.load('model_2feature.lsi')
lsi = models.LsiModel.load('model.lsi')
dictionary = corpora.Dictionary.load('fullDictionary.dict')
corpus = corpora.MmCorpus('fullCorpus.mm')
print(corpus)

#lsi.print_topics(num_topics=50,num_words=8)
'''
print('\n')
print lsi.show_topic(0,topn=50)
print('\n')
print lsi.show_topic(1,topn=50)
print('\n')
'''

query = 'Bose einstein condensate lattice'
query = 'optical quantum computing entangled'
query = 'bose hubbard model'
query = 'super conducting quantum interference device squid'
query = 'cavity atom computing entangled'

try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET
import obo
years=range(1992,1995)
years=range(1995,1998)
years=range(1998,2001)
years=range(2001,2004)
years=range(2004,2007)
years=range(2007,2010)
years=range(2010,2013)
years=range(2013,2017)
scoreList=[]
title=[]
for year in years:
	for event, elem in ET.iterparse('arXiv-meta-{}.xml'.format(year)): 
		if elem.tag == 'description':
			#queryList.append(elem.text)
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

import matplotlib.pyplot as plt 
import mpld3
fig, ax = plt.subplots(subplot_kw=dict(axisbg='#EEEEEE'),figsize=(18, 12))
scatter = ax.scatter(x, y, y,                                         
                     alpha=0.3,
                     cmap=plt.cm.jet)
ax.grid(color='white', linestyle='solid')
ax.set_xlim([-1,8]), ax.set_ylim([-6,6])

ax.set_title("Scatter Plot (with tooltips!)", size=20)

labels = ['point {0}'.format(i + 1) for i in range(len(x))]
labels = title
tooltip = mpld3.plugins.PointLabelTooltip(scatter, labels=labels)
mpld3.plugins.connect(fig, tooltip)

mpld3.show()

'''
query=queryList[15]
queryStripped=obo.removeStopwords(obo.stripNonAlphaNum(query),obo.stopwords)
print(query)

#vec_bow = dictionary.doc2bow(query.lower().split())
vec_bow = dictionary.doc2bow(queryStripped)
vec_lsi = lsi[vec_bow]
a=vec_lsi
b=[(a[0][1], a[1][1])]
b.append((a[0][1], a[1][1]))
print(b)
for aa in a[0:2]:
	topics=lsi.show_topic(aa[0])		
	newtopic=[(str(x[0]), '{:0.3f}'.format(x[1])) for x in topics]	
	print aa, ': ', newtopic

	#pprint (aa, ': ', newtopic)
#print max(vec_lsi,key=lambda item: abs(item[1]))
print('\n')
print(lsi.print_topic(  max(vec_lsi,key=lambda item: abs(item[1]))  [0]))
#sims=index[vec_lsi]
#print(list(enumerate(sims)))
'''
'''
print '\n'
i=-1
indArr=[]
for doc in corpus_lsi: # both bow->tfidf and tfidf->lsi transformations are actually executed here, on the fly
	i+=1	
	d=dict(doc)
	sd=sorted(d,key=d.get)
	maxsd=sd[-1]  # index
	#d[maxsd]     # value
	if maxsd==45:
		indArr.append(i)
		print('val: {}, i: {}, date: {}, title: {}'.format(d[maxsd],i,date[i], title[i]))	
'''		