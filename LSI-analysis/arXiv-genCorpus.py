'''
arXiv-genCorpus.py --- 16 June 2016
-------------------------------------------------
This script has been coded for Python 2.7

Takes dictionary generated by arXiv-genDictionary.py, and generates a corpus of all article descriptions

Input: 
arXiv-meta-{}.xml -- dump of XML data into annual blocks
fullDictionary.dict   -- dictionary of words from all metadata

Output:
fullCorpus.mm   -- corpus of all meta data (bag-of-words representation using dictionary)

'''
#################################################################################################
## import some packages
#################################################################################################
print( 'Loading modules ... ')
from gensim import corpora
import os.path
import obo
try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET

#################################################################################################
## Load dictionary
#################################################################################################
print( 'Loading dictionary ... ')
fname ='fullDictionary.dict' 
#path=os.path.dirname(os.getcwd())+'\\DATA\\OBJ\\LSI\\'+fname
path=os.path.dirname(os.getcwd())+'/DATA/OBJ/LSI/'+fname
dictionary = corpora.Dictionary.load(path)

#################################################################################################
## build corpus one document at a time
#################################################################################################
years=range(1992,2017) ## specify range of data
print( 'Generating corpus for years {} to {} ... '.format(years[0], years[-1]) )
class MyCorpus(object):
    def __iter__(self):        	
    	for year in years:       
            fname ='arXiv-meta-{}.xml'.format(year) 
            #path=os.path.dirname(os.getcwd())+'\\DATA\\'+fname        	
            path=os.path.dirname(os.getcwd())+'/DATA/SORTED/'+fname          
            for event, elem in ET.iterparse(path): 
		   		if elem.tag == 'description':
					desc = obo.removeStopwords(obo.stripNonAlphaNum(elem.text),obo.stopwords)            
					yield dictionary.doc2bow(desc)
corpus = MyCorpus()  # doesn't load the corpus into memory!

#################################################################################################
## save to file
#################################################################################################
fname='fullCorpus.mm'
path=os.path.dirname(os.getcwd())+'\\OBJ\\LSI\\'+fname
print('Saving corpus as {} ... '.format(fname))
#corpora.MmCorpus.serialize(path, corpus)
print('Finished!')

#################################################################################################
## diagonostics
#################################################################################################

## output somethings
for vector in corpus:  # load one vector into memory at a time
    print(vector)
    print '\n'
