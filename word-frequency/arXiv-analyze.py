'''
Launch bokeh server with:

bokeh serve --show arXiv-analyze.py

'''

######################################################################################################
## Modules
######################################################################################################
print ('Loading modules...')
import numpy as np
import os.path
#import pickle
import pandas
from os.path import dirname, join
from bokeh.plotting import figure
from bokeh.layouts import layout, widgetbox
from bokeh.models import ColumnDataSource, Div
from bokeh.models.widgets import Select, TextInput
from bokeh.io import curdoc
#from matplotlib.pyplot import cm

######################################################################################################
## Functions
######################################################################################################
## Build dictionary of frequently used words (per quarter)
def build_dictionary():  
    from math import ceil
    import os.path

    invDictList=[]
    #for q in range(len(topWords)):
    for q in range(len(dfTopWords.columns)):
        year  = 1992  + int(ceil((q+1.)/4)-1)        
        #topWordsquarter=topWords[q]
        keys=dfTopWords.iloc[:,q].tolist()
        values=dfTopWordsFreqs.iloc[:,q].tolist()
        topWordsquarter=[(v,k) for k,v in zip(keys,values)]
        #for s in topWordsquarter[-10:-1]: print(str(s))    

        # topWordsquarter is a list of tuples [(key, value)..], need to reverse, then build dictionary
        topWordsquarterReversed=[]
        for t in topWordsquarter:
            topWordsquarterReversed.append(tuple(reversed(t)))  
        invDict=dict(topWordsquarterReversed)
        invDictList.append(invDict) 
        
    return invDictList

## generate a score based on word frequency
def getPhraseScore(phrase): 
    words=phrase.lower().split()    
    
    #score=[0]*len(topWords)
    #for q in range(len(topWords)):
    score=[0]*len(dfTopWords.columns)
    for q in range(len(dfTopWords.columns)):
        for word in words:
            if word in invDictList[q]: 
                score[q] += invDictList[q].get(word)                
            else:
                score[q] = 0
                break;
        score[q]=score[q]/len(words) # normalize by number of words in phrase
    score=score/NRecQuarter # normalize by number of words records
    ## remove bins with low statistics (data before 1995)
    score=np.delete(score,delList)
    
    ## let's do some smoothing
    NS=3           
    scoreSmoothed=np.zeros(len(score))
    for i in range(len(score)):
        i1=max(i-NS,0)
        i2=min(i+NS,len(score))
        scoreSmoothed[i]=np.mean(score[i1:i2], dtype=np.float32)

    return scoreSmoothed

## extract input data
def get_data():
    phrases=[]
    for ti in t: phrases.append(ti.value)
    
    ## setup time axis
    quarters=np.arange(len(dfTopWords.columns))
    x=quarters/4.+1992

    ## remove bins with low statistics (data before 1995)
    x=np.delete(x,delList)        

    ## loop through each phrase and call scoring function
    x2,y2=[],[]    
    for phrase in phrases:
        x2.append(x)
        if phrase != '':            
            y=getPhraseScore(phrase)            
            y2.append(y)
        else: y2.append(x*0)

    return phrases, x2, y2

## update
def update():
    ## check guide mode and load appropriate data
    if guide.value=="Hot":                
        topics=['rydberg','single photon non linearity','topological','open dynamics','biological coherence','']
        for i in range(6): t[i].value=topics[i]
        infoText='info-HotTopics.html'    
    elif guide.value=="Spikes":        
        topics=['sudden death','error correction','','','','']
        for i in range(6): t[i].value=topics[i]
        infoText='info-Spikes.html'
    elif guide.value=="Breakthroughs":
        topics=['experimental teleportation photon','phase transition lattice superfluid mott insulator','synthetic magnetic fields','','','']
        for i in range(6): t[i].value=topics[i]
        infoText='info-Breakthroughs.html'
    else:
        infoText='info-RoamFree.html'
    info.text=open(join(dirname(__file__), infoText)).read()

    ## get the input data and turn it into scores
    phrases, x2, y2 = get_data()
    ## set plot data
    for i in range(6):
        source[i].data=dict(x=x2[i],y=y2[i])


######################################################################################################
## Create structures
######################################################################################################
## HTML
desc = Div(text=open(join(dirname(__file__), "description.html")).read(), width=1250)
info = Div(text='', width=1250)
## Select input controls
guide = Select(title="Guide", value="Hot",
               options=open(join(dirname(__file__), 'topic-themes.txt')).read().split())
## Text input control
t=[]
source=[]
for i in range(6):
    t.append( TextInput( title="Topic {}".format(i+1) ) )
    source.append( ColumnDataSource(data=dict(x=[], y=[])) )
## Plot figure
p = figure(plot_height=500, plot_width=700, title="", toolbar_location="above")
p.background_fill_color="SlateGray"
p.background_fill_alpha=0.05
c=['red','blue','green','cyan','magenta','black']
for i in range(6):
    p.line(x='x', y='y', line_width=4,color=c[i],legend='topic {}'.format(i+1),source=source[i])
p.legend.location  = "top_left"
p.xaxis.axis_label = 'Year'
p.yaxis.axis_label = 'Score'    
p.title.text       = "arXiv:quant-ph"
    
######################################################################################################
## setup control callback
######################################################################################################
controls = [guide, t[0], t[1], t[2], t[3], t[4], t[5]]
for control in controls:
    control.on_change('value', lambda attr, old, new: update())

######################################################################################################
## Layout
######################################################################################################
sizing_mode = 'fixed'  # 'scale_width' also looks nice with this example
inputs = widgetbox(*controls, sizing_mode=sizing_mode)
l = layout([
    [desc],
    [inputs, p],
    [info],
], sizing_mode=sizing_mode)

######################################################################################################
## Launch!
######################################################################################################
#from bokeh.io import output_file
#output_file('test.html', title='Bokeh Plot', autosave=False, mode='cdn', root_dir=None)

## Pickle? Pickle
print ('Loading data...')
path = os.path.dirname(os.getcwd())+'/DATA/OBJ/'
#NRecQuarter = pickle.load( open( path + 'NRecQuarter' + '.pkl' , "rb" ) )
#topWords = pickle.load( open( path + 'topWords5k' + '.pkl', "rb" ) )
NRecQuarter = pandas.read_csv(path + 'NRecQuarter.csv').iloc[0].tolist()
dfTopWords = pandas.read_csv(path + 'topWords-words.csv')
dfTopWordsFreqs = pandas.read_csv(path + 'topWords-freqs.csv')
## Build dictionary
print ('Building dictionary...')
invDictList = build_dictionary()
## basic formatting
NRecQuarter=np.asarray(NRecQuarter,dtype=np.float32)
NRecQuarter[np.where(NRecQuarter == 0)[0]]=0.1
delList=[0,1,2,3,4,5,6,7,8,9,10,11,len(NRecQuarter)-2,len(NRecQuarter)-1]    
## initial values
print ('Initializing...')
update()  
curdoc().add_root(l)
curdoc().title = "Go Science Yourself"

'''
from bokeh.embed import file_html
from bokeh.resources import JSResources
from bokeh.util.browser import view
# Use inline resources, render the html and open
js_resources = JSResources(mode='inline')
title = "Bokeh - Gapminder Bubble Plot"
html = file_html(l, resources=(js_resources, None), title=title)

output_file = 'gapminder.html'
with open(output_file, 'w') as f:
    f.write(html)
view(output_file)
'''

'''
# Use inline resources, render the html and open
js_resources = JSResources(mode='inline')
title = "Bokeh - Gapminder Bubble Plot"
html = file_html(layout, resources=(js_resources, None), title=title, template=template)

output_file = 'gapminder.html'
with open(output_file, 'w') as f:
    f.write(html)
view(output_file)
'''