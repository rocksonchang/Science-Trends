'''
arXiv-metadata-genCorpus.py --- 11 June 2016
-------------------------------------------------
This script has been coded for Python 2.7
Generate LSI model from dictionary and corpus.

'''
#!/usr/bin/python3.5

#################################################################################################
#################################################################################################

## import some packages
from gensim import corpora, models, similarities
## logging
import logging
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)


Nfeat=20
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
lsi = models.LsiModel(corpus_tfidf, id2word=dictionary, num_topics=Nfeat) # initialize an LSI transformation
corpus_lsi = lsi[corpus_tfidf]
'''
i=-1
for doc in corpus_lsi:
	i+=1
	if i <10:
		print doc, '\n'
	else:
		break

print '\n'
'''
#lsi.print_topics(10)

## save
lsi.save('model_{}feature.lsi'.format(Nfeat)) # same for tfidf, lda, ...
