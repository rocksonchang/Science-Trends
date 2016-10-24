'''
arXiv-metadata-process.py --- 29 June 2016
-------------------------------------------------
This script has been coded for Python 2.7.

This script takes the ordered XML data, extracts the text (titles and abstracts), and identifies 
the most frequently used words in each quarter.  Word processing consists of eliminating common 
english words (stop words) and stripping non-standard characters.  

Input: 
arXiv-meta-{}.xml   -- XML data sorted by date and dumped by year

Output:
NRecQuarter.pkl   -- number of records per quarter
topWords5k.pkl    -- 5000 most frequent words per quarter

Some future improvements:
- check out the beautiful soup package for cleaning up data.  Need something that can do a better
job parsing latex.
'''


#################################################################################################
#################################################################################################
from xml.dom import minidom
import itertools  # do I need this?
from datetime import datetime
import time
import os.path
from math import ceil
import obo
import pickle # to export a python structure
## handling of non-ascii characters in the database
# http://chase-seibert.github.io/blog/2014/01/12/python-unicode-console-output.html
import sys
import codecs
sys.stdout = codecs.getwriter('utf8')(sys.stdout)
sys.stderr = codecs.getwriter('utf8')(sys.stderr)


#################################################################################################
#################################################################################################
## load data
print ('\nLoading XML data...')
#creators=[]
addys=[]
titles=[]
descriptions=[]
dates=[]

## scan through each year
years=range(1992,2017)
NRecYear=[0]*(len(years))	
for x in range(len(years)):	
	fname ='arXiv-meta-{}.xml'.format(years[x])	
	#path=os.path.dirname(os.getcwd())+'\\DATA\\'+fname
	path=os.path.dirname(os.getcwd())+'/DATA/SORTED/'+fname
	## parse XML data
	data = minidom.parse(path)		
	for rec in data.getElementsByTagName('record'):			
		NRecYear[x]+=1
		## extract data 
		#t_creators=()
		#for c in rec.getElementsByTagName("dc:creator"):			
		#t_creators=t_creators+(c.firstChild.data,)
		rec_dates=[]
		for d in rec.getElementsByTagName("date"):
			rec_dates.append(d.firstChild.data)		
		rec_ids=[]
		for i in rec.getElementsByTagName("identifier"):
			rec_ids.append(i.firstChild.data)					
		#print(rec.getElementsByTagName("dc:title")[0].firstChild.data)			

		## append data from this record into a larger running array across all blocks
		#creators.append(t_creators)
		addys.append(rec.getElementsByTagName("identifier")[0].firstChild.data)
		titles.append(rec.getElementsByTagName("title")[0].firstChild.data)
		descriptions.append(rec.getElementsByTagName("description")[0].firstChild.data)
		dates.append(rec_dates[0]) # take date first submitted as date.
	print ('Loading year: {}; Num. entries: {}'.format(years[x],NRecYear[x]))
## output some stuff to check	
#print('\n')		
#for i in range(len(titles)): print(titles[i]);	print(dates[i]); print(descriptions[i]); print('\n');
print('\n')

#################################################################################################
#################################################################################################
## Identify most frequently used words in each quarter
print ('Extracting text, identifying most frequently used words each quarter...')
NRec=sum(NRecYear)
topWords=[]
NRecRunning=0
year0=years[0]
NRecQuarter=[0]*len(years)*4

## run through each year
for x in range(len(years)):	
	fulltextQuarter=['']*4
	for i in range(NRecYear[x]):
		rec=i+NRecRunning						
		desc=descriptions[rec]
		
		title=titles[rec]
		text=title+desc

		## identify quarter ...
		date=datetime.strptime(dates[rec],'%Y-%m-%d')		
		Q=int(ceil(date.month/3.)-1)
		ind = 4*(date.year-year0)+Q
		NRecQuarter[ind]+=1
		## ... and dump all text into same bin
		fulltextQuarter[Q]=fulltextQuarter[Q]+text		
	## figure out how many records per quarter	
	NRecRunning=NRecRunning+NRecYear[x]
	
	## clean up text and identify most frequent words using obo package
	for q in range(4):
		desc_fullwordlist = obo.stripNonAlphaNum(fulltextQuarter[q])
		desc_wordlist = obo.removeStopwords(desc_fullwordlist,obo.stopwords)	
		desc_dictionary = obo.wordListToFreqDict(desc_wordlist)
		desc_sorteddict = obo.sortFreqDict(desc_dictionary)

		topWords.append(desc_sorteddict[:5000])			
		print ('Year: {}; Quarter: Q{}; Num. entries: {}'.format(years[x],q+1,NRecQuarter[4*(date.year-year0)+q]))				
		
		for s in desc_sorteddict[:10]: print(str(s))
		print('\n')
	
print('\n')
	
#################################################################################################
#################################################################################################
## Pickle
#with open('obj/'+ 'NRecQuarter' + '.pkl', 'wb') as f:
'''
path=os.path.dirname(os.getcwd())+'\\OBJ\\'
with open(path + 'NRecQuarter' + '.pkl', 'wb') as f:
	pickle.dump(NRecQuarter, f, pickle.HIGHEST_PROTOCOL)
with open(path + 'topWords5k' + '.pkl', 'wb') as f:
	pickle.dump(topWords, f, pickle.HIGHEST_PROTOCOL)
'''