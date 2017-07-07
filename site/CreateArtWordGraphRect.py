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

def createArtWordGraph(artdict):
    words=[]
    rates=[]
    for item in sorted(artdict,key=lambda tup: tup[0]):
        
        words.append(item[0])
        rates.append(item[1])

    df=pd.DataFrame({'Artists':words,'WordRate':rates})
    if len(df)<51:
        df= df.sort('WordRate')
    else:
        df= df.sort('WordRate')[50:]
    words = df['Artists'].tolist()
    rates=df['WordRate'].tolist()
    
    hover = HoverTool(
            tooltips=[
                ("Word:", "@y"),
                
            ]
        )      

              
    p = figure(y_range=words,x_range=[0,max(rates)*1.2],tools=[hover])
    p.rect(y=words,x=[0 for i in range(len(rates))], height=.5, width=[rate*2 for rate in rates],
            color="gold") 
            

    
#    p = Bar(df,'Artists',values='WordRate',
#              color="gold", bar_width=1,tools=[hover],legend=False)
    script, div = components(p)
    return script,div
            


