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
    words = pd.read_csv("/Users/christopherhedenberg/Downloads/projects/RapThesaurus/ModelOutput/WordTopicFreqTSNETop1000.csv")
    word= words['Word'].as_matrix()
    topic_list = words['Topic'].as_matrix()
    comp1 = words['Comp1'].as_matrix()
    comp1 = comp1/max(comp1)
    comp2 = words['Comp2'].as_matrix()
    comp2 = comp2/max(comp2)
    radii = .025
    color_dict={'club':'#DE64FF', 'men':'#6062A7', 'neighborhood':'#E89334', 'gangs':'#EC2E42', 'family':'#FFFF64', 'cops':'#6062A7', 'drugs':'#0E0336', 
                 'money':'#5AAB6A', 'violence':'#042505', 'sex':'#C1EC2E', 'curses':'#2EECB8', 'religion':'#2EE6EC', 'poverty':'#2E8DEC', 'prison':'#CECAD0', 
                 'rap':'#6062A7', 'cars':'#591212', 'love':'#0E0336', 'women':'#401221', 'hustle':'#97A4BA', 'stuntin':'#97A4BA', 'clothes':'#97A4BA','Other':'#97A4BA'}
    
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
#,x_range=(-1,.2),y_range=(-.1,.1)
    p = figure(tools=[hover])

    
    p.scatter('x', 'y', radius=radii, fill_alpha=0.6,fill_color=colors,
              line_color=None,source=source)


    script, div = components(p)
    return script,div
    
