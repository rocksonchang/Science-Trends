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

## load LSI model
#lsi = models.LsiModel.load('model_2feature.lsi')
lsi = models.LsiModel.load('model.lsi')

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

## plot stuff
fig, ax = plt.subplots(subplot_kw=dict(axisbg='#EEEEEE'),figsize=(18, 12))
scatter = ax.scatter(x, y,                                         
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

