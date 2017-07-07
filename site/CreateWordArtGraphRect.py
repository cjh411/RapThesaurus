# -*- coding: utf-8 -*-
"""
Created on Thu Jun  8 14:14:00 2017

@author: christopherhedenberg
"""

import pandas as pd
from bokeh.charts import Bar
from bokeh.embed import components
from bokeh.plotting import figure,ColumnDataSource, show
import numpy as np
from bokeh.models import HoverTool
import pickle
wordArt=pickle.load(open("/Users/christopherhedenberg/Downloads/projects/RapThesaurus/ModelOutput/WordArtPickle/WordArtDict.p",'rb'))

def createWordArtGraph(worddict):
    arts=[]
    rates=[]
    for item in sorted(worddict,key=lambda tup: tup[0]):
        arts.append(item[0])
        rates.append(item[1])

    df=pd.DataFrame({'Artists':arts,'WordRate':rates})
    df= df.sort('WordRate')
    words=df['Artists'].tolist()
    rates=df['WordRate'].tolist()
    
    
    hover = HoverTool(
            tooltips=[
                ("Artist:", "@y"),
            ]
        )      


    
              
    p = figure(y_range=words,x_range=[0,max(rates)*1.2],tools=[hover])
    p.rect(y=words,x=[0 for i in range(len(rates))], height=.5, width=[rate*2 for rate in rates],
            color="gold") 
    script, div = components(p)
    return script,div


