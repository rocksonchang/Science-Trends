'''
arXiv-genDictionary.py --- 16 June 2016
-------------------------------------------------
This script has been coded for Python 2.7

Import ordered xml data, and build a dictionary of words from the entire data set of 
record descriptions (abstracts).

Some basic word clean up is performed using the OBO package before creation of the dictionary
-- strip non alpha numeric characters
-- remove common words

Input: 
arXiv-meta-{}.xml -- dump of XML data into annual blocks

Output:
fullDictionary.dict   -- dictionary of words from all metadata

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
## build dictionary from stream, clean up as we go
#################################################################################################
years=range(1992,2017) ## specify range of data
print( 'Generating dictionary for years {} to {} ... '.format(years[0], years[-1]) )
root=os.path.dirname(os.getcwd())+'\\DATA\\'
doc_stream = ( obo.removeStopwords(obo.stripNonAlphaNum(elem.text),obo.stopwords)
				for year in years					
			   		for event, elem in ET.iterparse( root + 'arXiv-meta-{}.xml'.format(year) ) 
			   			if elem.tag == 'description' )
dictionary=corpora.Dictionary(doc_stream)
print(dictionary)

#################################################################################################
## save to file
#################################################################################################
fname='fullDictionary.dict' 
print('Saving dictionary as {} ...'.format(fname))
path=os.path.dirname(os.getcwd())+'\\OBJ\\LSI\\'+fname
dictionary.save(path) 
print('Finished!')

#################################################################################################
## diagonostics
#################################################################################################
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