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
from bokeh.models import Range1d

def createWordGraph():
    words = pd.read_csv("/Users/christopherhedenberg/Downloads/projects/RapThesaurus/ModelOutput/WordTopicFreqTSNEv3.csv")
    word= words['Word'].as_matrix()
    topic_list = words['Topic'].as_matrix()
    comp1 = words['Comp1'].as_matrix()/2E26
    comp2 = words['Comp2'].as_matrix()/2E26
    freq = words['Frequency'].as_matrix()
    maxfreq = max(freq)
    radii = [.1*freq[i]/maxfreq for i in range(len(freq))]
    color_dict={'club':'##DE64FF', 'men':'#6062A7', 'neighborhood':'#E89334', 'gangs':'#EC2E42', 'family':'#FFFF64', 'cops':'#6062A7', 'drugs':'#6479FF', 
                 'money':'#5AAB6A', 'violence':'#9E2EEC', 'sex':'#C1EC2E', 'curses':'#6062A7', 'religion':'#6062A7', 'poverty':'#6062A7', 'prison':'#6062A7', 
                 'rap':'#6062A7', 'cars':'#6062A7', 'love':'#6062A7', 'women':'#6062A7', 'hustle':'#6062A7', 'stuntin':'#6062A7', 'clothes':'#6062A7'}
    
    colors = [color_dict[topic] for topic in topic_list]
    
    
    
    
    source = ColumnDataSource(
            data=dict(
                x=list(comp1),
                y=list(comp2),
                desc=list(word),
            )
        )
    hover = HoverTool(
            tooltips=[
                ("", "@desc"),
            ]
        )      
    #TOOLS="hover,crosshair,pan,wheel_zoom,zoom_in,zoom_out,box_zoom,undo,redo,reset,tap,save,box_select,poly_select,lasso_select,"

    p = figure(tools=[hover],x_range=(0,.2),y_range=(-.1,.1))

    
    p.scatter('x', 'y', radius=radii, fill_alpha=0.6,fill_color=colors,
              line_color=None,source=source)

    script, div = components(p)
    return script,div
    