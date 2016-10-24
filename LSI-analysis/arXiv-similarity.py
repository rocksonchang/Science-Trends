'''
arXiv-similarity.py --- 17 June 2016
-------------------------------------------------
This script has been coded for Python 2.7

This script performs a similarity search of a desired query.  To do this, a similarity matrix
of the full corpus (the learning set) is prepared.  The query is then transformed into the 
same LSI representation and then compared to the corpus using the function "index".  This function
returns a list of the similarity of the search query to all of the documents in the corpus.  

The similarity list is ordered, and the top results and plotted.  Plots are creatd with the 
bokeh package.

Launch bokeh server with:

bokeh serve --show arXiv-similarity.py

Input: 
model_{}feature.lsi  -- model for LSI representation with a variable number of features (topics)
fullDictionary.dict   -- dictionary of words from all metadata
fullCorpus.mm   -- corpus of all meta data (bag-of-words representation using dictionary)
arXiv-meta-{}.xml -- dump of XML data into annual blocks

Output:
corpus_{}feature.index -- similarity matrix index for full corpus based on LSI model with Nfeat features

'''

#################################################################################################
## load some packages
#################################################################################################
print( 'Loading modules ... ')
from gensim import corpora, models, similarities
try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET
import obo
import logging
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

from bokeh.plotting import figure
from bokeh.layouts import layout, widgetbox
from bokeh.models import ColumnDataSource, Div, HoverTool, Range1d
from bokeh.models.widgets import Select, TextInput
from bokeh.io import curdoc
from os.path import dirname, join
import pickle 

from datetime import datetime
import numpy as np
import os.path
from math import ceil, floor

#################################################################################################
## load LSI model
#################################################################################################
Nfeat=100 #2,10,20, 30,100(seems to have problems above 100 topics)
print( '\nLoading LSI model with {} features ... '.format(Nfeat))
fname='model_{}feature.lsi'.format(Nfeat)
path=os.path.dirname(os.getcwd())+'\\OBJ\\LSI\\'+fname
lsi = models.LsiModel.load(path)
lsi.print_topics(200)
#################################################################################################
## Load dictionary and corpus
#################################################################################################
print( '\nLoading dictionary and corpus ... ')
fname ='fullDictionary.dict' 
path=os.path.dirname(os.getcwd())+'\\OBJ\\LSI\\'+fname
dictionary = corpora.Dictionary.load(path)

root=os.path.dirname(os.getcwd())+'\\OBJ\\LSI\\'
corpus = corpora.MmCorpus(root+'fullCorpus.mm')

#################################################################################################
## Index corpus and save
#################################################################################################
print( '\nCreating similarity matrix index ... ')
#index = similarities.MatrixSimilarity( lsi[corpus] ) # transform corpus to LSI space and index it
fname='corpus_{}feature.index'.format(Nfeat)
path=os.path.dirname(os.getcwd())+'\\OBJ\\LSI\\'+fname
#index.save(path)
index = similarities.MatrixSimilarity.load(path)

#################################################################################################
## Pull article titles and dates
#################################################################################################
years=range(1992,2017)
print( '\nLoading article data for years {} to {} ... '.format(years[0], years[-1]) )
titles, dates = [], []
for year in years:
	fname='arXiv-meta-{}.xml'.format(year)
	path=os.path.dirname(os.getcwd())+'\\DATA\\'+fname
	for event, elem in ET.iterparse(path): 		
		if elem.tag == 'title':
			titles.append(elem.text)
		if elem.tag == 'date':
			dates.append(elem.text)
## convert date
year=[]
for date in dates:
	data=datetime.strptime(date,'%Y-%m-%d')			
	year.append(data.year+data.month/12.)	
## records per quarter
path = os.path.dirname(os.getcwd())+'\\OBJ\\'
NRecQuarter = pickle.load( open( path + 'NRecQuarter' + '.pkl' , "rb" ) )

#################################################################################################
## Perform query
#################################################################################################
query = "quantum simulation phase transition"
query = "quantum error correction shor"
query = "three dimensional doppler cooling theory helium"
#query = "response particle periodic potential effective mass dynamics bose einstein condensate"
query = "anderson localization matter waves"
Ntop=300
print ( '\n' )
print ( 'QUERY: ' + query )
print ( 'TOP {} hits: '.format(Ntop) + query )

## find similarity of query to articles in corpus
vec_bow = dictionary.doc2bow( obo.removeStopwords(obo.stripNonAlphaNum(query),obo.stopwords) )
vec_lsi = lsi[vec_bow]
sims = index[vec_lsi] # perform a similarity query against the corpus
sims = sorted(enumerate(sims), key=lambda item: -item[1])

#################################################################################################
## Prepare data for plotting
#################################################################################################
## prepare data for scatter plot -- article index, score, date, titles
iArr      = [x[0] for x in sims[:Ntop]] 
sArr      = [x[1] for x in sims[:Ntop]]	
dArr      = [year[i] for i in iArr]
labelsArr = [titles[i] for i in iArr]
datesArr  = [dates[i] for i in iArr]

## prepare data for line plot -- data binned into quarters
years=np.arange(1992,2017,0.25)
sYear=np.zeros(len(years))
for x,s in zip(dArr,sArr):
	xInd=floor( 4*(x-1992) )
	sYear[xInd] += s
#y=sYear/NRecQuarter

## clean up data, remove low stat quarters
y=sYear
delList=[0,1,2,3,4,5,6,7,8,9,10,11,len(NRecQuarter)-2,len(NRecQuarter)-1]    
x=np.delete(years,delList)
y=np.delete(y,delList)

## let's do some smoothing
NS=5
ySmoothed=np.zeros(len(x))
for i in range(len(x)):
    i1=max(i-NS,0)
    i2=min(i+NS,len(x))
    ySmoothed[i]=np.mean(y[i1:i2], dtype=np.float32)

######################################################################################################
## Bokeh
######################################################################################################
## HTML description
desc  = Div(text=open(join(dirname(__file__), "description.html")).read(), width=1250)
desc2 = Div(text=query, width=1250)

## Create Column Data Source that will be used by the plot
source = ColumnDataSource(data=dict(x=[], y=[], title=[], date=[]))
source.data = dict( x=dArr, y=sArr, title=labelsArr, date=datesArr )

## Plot figure - scatter plot
hover = HoverTool(tooltips=[    ("Title", "@title"), ("Date", "@date")    ])
p = figure(plot_height=400, plot_width=700, title="", tools='box_zoom, pan, reset')
p.add_tools(hover)
p.circle(x="x", y="y", source=source, size=7, color="grey", line_color=None, fill_alpha=0.9)
p.xaxis.axis_label = 'Year'
p.yaxis.axis_label = 'Similarity'    
p.title.text       = "Top {} matches".format(Ntop)
p.set(y_range=Range1d(0, 1))

## Plot figure - line plot of sum of top scores
p2 = figure(plot_height=400, plot_width=700, title="", toolbar_location=None)
p2.circle(x=x, y=y, size=7, color="grey", line_color=None, fill_alpha=0.5)
p2.line(x=x, y=ySmoothed, line_width=4,color='blue',legend=None)
p2.title.text       = "Moving sum of top {} matches".format(Ntop)
p2.xaxis.axis_label = 'Year'
p2.yaxis.axis_label = 'Sum of top similarity scores'    

######################################################################################################
## Layout
######################################################################################################
sizing_mode = 'fixed'  # 'scale_width' also looks nice with this example
l = layout([
	[desc],
	[desc2],
    [p],
    [p2],    
], sizing_mode=sizing_mode)

curdoc().add_root(l)
curdoc().title = "Go Science Yourself (LSI Version)"
#print curdoc()
#from bokeh.resources import CDN
#from bokeh.embed import file_html
#html = file_html(l, CDN, "my plot")