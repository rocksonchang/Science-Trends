'''
arXiv-metadata-genDictionary.py --- 11 June 2016
-------------------------------------------------
This script has been coded for Python 2.7
Import ordered xml data, and build a dictionary of words from the entire data set of record descriptions (abstracts)

'''
#!/usr/bin/python3.5

#################################################################################################
#################################################################################################

## import some packages
from gensim import corpora
import obo
try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET

## specify range of data
years=range(1992,2017)
fileName='fullDictionary.dict'

## build dictionary from stream, clean up as we go
print( '\nGenerating dictionary for years {} to {} ... '.format(years[0], years[-1]) )
doc_stream = ( obo.removeStopwords(obo.stripNonAlphaNum(elem.text),obo.stopwords)
				for year in years					
			   		for event, elem in ET.iterparse('RAW/arXiv-meta-{}.xml'.format(year)) 
			   			if elem.tag == 'description' )
dictionary=corpora.Dictionary(doc_stream)
print('Finished!')
print(dictionary)
## save to file
dictionary.save(fileName) 
print('Dictionary saved as {}'.format(fileName))

'''
## some output checks
i=-1
for d in dictionary.token2id:
	i+=1
	if i<20:
		print d

for i in range(0,15):
	print dictionary.get(i)


new_doc = "Human computer interaction"
new_vec = dictionary.doc2bow(new_doc.lower().split())
print new_vec
for k in new_vec:
	print dictionary.get(k[0])
'''