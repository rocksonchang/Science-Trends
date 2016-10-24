'''
arXiv-dynamics.py --- 16 June 2016
-------------------------------------------------
This script has been coded for Python 2.7

Uses dictionary from  arXiv-genDictionary.py,
Uses corpus from  arXiv-genCorpus.py,
Uses LSI model from arXiv-genLSIModel.py

'''

#################################################################################################
## load some packages
#################################################################################################
#from gensim import corpora, models, similarities
from gensim import models
import matplotlib.pyplot as plt 
import mpld3
import numpy as np
import pickle
import os.path

#################################################################################################
## load LSI model and document scores per year
#################################################################################################
Nfeat=20 #2,10,20, 30,100(seems to have problems above 100 topics)
print( '\nLoading LSI model with {} features ... '.format(Nfeat))
root=os.path.dirname(os.getcwd())+'\\OBJ\\LSI\\'
lsi = models.LsiModel.load(root+'model_{}feature.lsi'.format(Nfeat))
scores = pickle.load( open( root+"scores1_{}feature.pkl".format(Nfeat), "rb" ) )

fig=plt.figure(figsize=(8,8))
#topicList=(3, 4, 37, 49,54,65,70,77,85,97,104,110,121,122,131,138,172,225,243,266)
years=range(1995,2017)
topicList=range(Nfeat)
i=0
for topic in topicList:
	i+=1	
	clr=((i-1)/len(topicList),0.6, 1-(i-1.)/len(topicList))
	score=[x[topic] for x in scores]	
	del score[0:3]	
	#score=score/np.mean(score)
	plt.plot(years,score,'o-',color=clr,label=topic)	
	
	a=lsi.show_topic(topic,topn=10) 
	print '# {}: '.format(topic)
	#print [str(x[0]) for x in a]
	tmp = [str(x[0]) for x in a]
	tmp2 =' '.join(sorted(tmp))
	print tmp2
	print('\n')
	plt.ion()
	plt.show()
	raw_input()
	plt.cla()	

'''
for ii in topicList:
	a=lsi.show_topic(ii,topn=20) # mega decline
	tmp = [str(x[0]) for x in a]
	print '# {}: '.format(ii)
	print (tmp)
	print('\n')

'''

'''
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
'''
