'''
arXiv-metadata-reorder.py --- 22 Aug 2016
-------------------------------------------------
Modifed paths to run on Mac OS

arXiv-metadata-reorder.py --- 25 June 2016
-------------------------------------------------
This script has been coded for Python 2.7.

This script takes the raw XML data (divided into 4 blocks), re-orders them by date, and exports 
a new XML file for each year.  

Raw metadata consists of the following entries:
	dc:title
	dc:creator (authors)
	dc:subject (keywords)
	dc:description (abstract)
	dc:date (date of submission)
	dc:identifier (final publishing locations)

Input:
arXiv-meta-block{}}.xml   -- dump of XML data into blocks

Output:
arXiv-meta-{}.xml   -- XML data sorted by date and dumped by year

Some future improvements:
- Currently, only keeping title, subject, description, date and identifier.  Maybe one day I'll
want to look at authors and keywords as well.
'''

#################################################################################################
#################################################################################################
from xml.dom import minidom
from xml.dom.minidom import Document
from itertools import chain # don't think I need chain anymore, delete
from datetime import datetime
import os.path
## throwing down some code I don't yet understand regarding non-ascii characters in the database
# http://chase-seibert.github.io/blog/2014/01/12/python-unicode-console-output.html
import sys
import codecs
sys.stdout = codecs.getwriter('utf8')(sys.stdout)
sys.stderr = codecs.getwriter('utf8')(sys.stderr)


#################################################################################################
#################################################################################################
## Records on local memory -- a list of tuples
myListofTuples=[]
## Run through raw data blocks
for block in range(1,5):
	#sys.stdout.write("Loading raw data: Block %d of 4  \r" % (block) )
	#sys.stdout.flush()
	print("Loading raw data: Block %d of 4  \r" % (block) )

	fname ='arXiv-meta-block{}.xml'.format(block)
	#path=os.path.dirname(os.getcwd())+'\\DATA\\'+fname
	path=os.path.dirname(os.getcwd())+'/DATA/RAW/'+fname

	## parse XML data with MiniDOM
	data = minidom.parse(path)	
	## pull out desired data from records, do some basic formatting
	creators=[]
	addys=[]
	titles=[]
	descriptions=[]
	dates=[]
	
	for rec in data.getElementsByTagName('record'):		
		## error checking if arXiv entry has been deleted
		hstatus = rec.getElementsByTagName("header")[0].getAttribute('status')
		if hstatus!='deleted':			
			t_creators=()
			for c in rec.getElementsByTagName("dc:creator"):			
				t_creators=t_creators+(c.firstChild.data,)
			rec_dates=[]
			for d in rec.getElementsByTagName("dc:date"):
				rec_dates.append(d.firstChild.data)		
			rec_ids=[]
			for i in rec.getElementsByTagName("dc:identifier"):
				rec_ids.append(i.firstChild.data)			
			#print(rec.getElementsByTagName("dc:title")[0].firstChild.data) 

			## append data from this record into a larger running array across all blocks
			creators.append(t_creators)
			addys.append(rec.getElementsByTagName("identifier")[0].firstChild.data)
			titles.append(rec.getElementsByTagName("dc:title")[0].firstChild.data)
			descriptions.append(rec.getElementsByTagName("dc:description")[0].firstChild.data)
			dates.append(rec_dates[0]) # take date first submitted as date.

		'''
		## output some stuff to check		
		print(titles)
		for c in rec_creators:
			print(c)
		print(dates)
		#for d in dates:
		#	print(d)
		print('\n')	
		'''
	
	## Compile block data
	for i in chain(range(0,len(dates))):
	
		date    = datetime.strptime(dates[i],'%Y-%m-%d')				
		addy    = addys[i]
		creator = creators[i]
		title   = titles[i]
		desc    = descriptions[i]
		
		myListofTuples.append((date,addy,title,creator,desc))

#################################################################################################
#################################################################################################
## Sort records by date of first submission
sortedList=sorted(myListofTuples, key=lambda d: d[0])

#################################################################################################
#################################################################################################
## Write sorted data into new XML file, one for each year
previousYear=myListofTuples[0][0].year # first entry
fname="arXiv-meta-{}.xml".format(previousYear)
#path=os.path.dirname(os.getcwd())+'\\DATA\\'+fname
path=os.path.dirname(os.getcwd())+'/DATA/SORTED/'+fname
f = open(path, "w")
doc = Document()
ListRecords = doc.createElement('ListRecords')
doc.appendChild(ListRecords)

## iterate through sorted records
sys.stdout.write("Writing year %d  \r" % (previousYear) )
sys.stdout.flush()
for rec in sortedList:
	year = rec[0].year	
	## check when we've reached a new year
	if year != previousYear:
		print('Writing year {} ...'.format(year))
		#sys.stdout.write("Writing year %d  \r" % (year) )
		#sys.stdout.flush()

		## write previous data and close file
		f.write(doc.toxml(encoding='utf-8'))
		f.close()
		## start a new file
		previousYear=year # new previous entry
		fname="arXiv-meta-{}.xml".format(previousYear)
		path=os.path.dirname(os.getcwd())+'/DATA/SORTED/'+fname
		f = open(path, "w")
		doc = Document()
		ListRecords = doc.createElement('ListRecords')
		doc.appendChild(ListRecords)

		
	
	## structure XML

	record = doc.createElement('record')
	ListRecords.appendChild(record)

	header = doc.createElement('header')
	record.appendChild(header)
	identifier = doc.createElement('identifier')
	header.appendChild(identifier)
	identifierData = doc.createTextNode(rec[1])
	identifier.appendChild(identifierData)
	
	## metadata and children

	metadata = doc.createElement('metadata')
	record.appendChild(metadata)
	
	title = doc.createElement('title')
	metadata.appendChild(title)
	titleData =doc.createTextNode(rec[2])
	title.appendChild(titleData)
	
	description = doc.createElement('description')
	metadata.appendChild(description)	
	descriptionData =doc.createTextNode(rec[4])
	description.appendChild(descriptionData)
	
	date = doc.createElement('date')
	metadata.appendChild(date)	
	dateData =doc.createTextNode(rec[0].strftime('%Y-%m-%d'))
	date.appendChild(dateData)

## write and close
f.write(doc.toxml(encoding='utf-8'))
f.close()
