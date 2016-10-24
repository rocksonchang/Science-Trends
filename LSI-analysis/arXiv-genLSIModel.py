'''
arXiv-genLSIModel.py --- 16 June 2016
-------------------------------------------------
This script has been coded for Python 2.7

Generates tfidf and LSI models from dictionary and corpus using GenSim package.

The term-frequency, inverse document frequency model (tfidf) takes the corpus (bow representation) 
and converts it into a representation of term weights.

The latent semantic index model (LSI) takes the corpus in a weighted representation (such as tfidf)
and converts it into a representation in terms of a number of found topics.  These topics are
linear superpositions of the terms in the original corpus, and are found from performing a 
singular value decomposition (SVD) of the term-weight - document matrix.  The LSI model allows to 
rank topics based on their singular values, and thus provides a way of reducing the dimensions of 
the problem (baesd on sparsity).

Input: 
fullDictionary.dict   -- dictionary of words from all metadata
fullCorpus.mm   -- corpus of all meta data (bag-of-words representation using dictionary)

Output:
model_{}feature.tfidf -- model for tfidf representation 
model_{}feature.lsi  -- model for LSI representation with a variable number of features (topics)

'''
#################################################################################################
## import some packages
#################################################################################################
print( 'Loading modules ... ')
from gensim import corpora, models, similarities
import logging
import os.path
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

#################################################################################################
## load dictionary, corpus - bag of words representation
#################################################################################################
print( 'Loading dictionary and corpus ... ')
root=os.path.dirname(os.getcwd())+'\\OBJ\\LSI\\'
dictionary = corpora.Dictionary.load(root+'fullDictionary.dict')
corpus = corpora.MmCorpus(root+'fullCorpus.mm')
print corpus

#################################################################################################
## Tfidf model (topic frequency, inverse document frequency)
#################################################################################################
print( '\nGenerating Tfidf model ... ')
tfidf = models.TfidfModel(corpus)
corpus_tfidf = tfidf[corpus]

#################################################################################################
## LSI model with Nfeat features
#################################################################################################
Nfeat=100
print( '\nGenerating LSI model with {} features ... '.format(Nfeat))
lsi = models.LsiModel(corpus_tfidf, id2word=dictionary, num_topics=Nfeat) # initialize an LSI transformation
corpus_lsi = lsi[corpus_tfidf]
print( '\nLSI Topics ...')
lsi.print_topics(200)

#################################################################################################
## save
#################################################################################################
fname='model_{}feature.lsi'.format(Nfeat)
path=os.path.dirname(os.getcwd())+'\\OBJ\\LSI\\'+fname
print( 'Saving LSI model as {} ... ').format(fname)
lsi.save(path) # same for tfidf, lda, ...

fname='model.tfidf'.format(Nfeat)
path=os.path.dirname(os.getcwd())+'\\OBJ\\LSI\\'+fname
print( 'Saving TFIDF model as {} ... ').format(fname)
tfidf.save(path)
print('Finished!')

#################################################################################################
## diagnostics
#################################################################################################
import numpy as np
import matplotlib.pyplot as plt
y=lsi.projection.s
x=np.arange(Nfeat)
plt.plot(x,y,'ro')
plt.show()
'''

for doc in corpus_tfidf:
    print(doc)

i=-1
for doc in corpus_lsi:
	i+=1
	if i <10:
		print doc, '\n'
	else:
		break

print '\n'
'''
