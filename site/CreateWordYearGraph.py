# -*- coding: utf-8 -*-
"""
Created on Thu Jun  8 14:14:00 2017

@author: christopherhedenberg
"""

import pandas as pd
from bokeh.charts import Histogram
from bokeh.embed import components
from bokeh.plotting import figure,ColumnDataSource, show
import numpy as np
from bokeh.models import HoverTool
import pickle

def createWordYearGraph(word,worddict):
    years= [i for i in range(1990,2018)]
    yrs=[]
    rates=[]
    rates_graph=[]
    for item in sorted(worddict,key=lambda tup: tup[0]):
        yrs.append(item[0])
        rates.append(item[1])
    for i in range(len(years)):
        if years[i] in yrs:
            rates_graph.append(rates[yrs.index(years[i])])
        else:
            rates_graph.append(0)
    
    
    
    source = ColumnDataSource(
            data=dict(
                x=list(years),
                y=list(rates_graph),
            )
        )
    hover = HoverTool(
            tooltips=[
                ("Year:", "@x"),
                ("Rate / Verse:", "@y"),
            ]
        )      
    #TOOLS="hover,crosshair,pan,wheel_zoom,zoom_in,zoom_out,box_zoom,undo,redo,reset,tap,save,box_select,poly_select,lasso_select,"
#,x_range=(-1,.2),y_range=(-.1,.1)
    p = figure(tools=[hover])

    
    p.line('x', 'y',
              line_color="gold", line_width=4,source=source)
    p.circle('x', 'y',
         fill_color="gold",radius=.25,source=source)


    script, div = components(p)
    return script,div

