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

def createArtGraph():
    artists = pd.read_csv("/Users/christopherhedenberg/Downloads/projects/RapThesaurus/ArtistTSNECleaned2.csv")
    dec_list = artists['YearGrouped'].as_matrix()
    
    
    
    
    color_dict={1980:"#%02x%02x%02x" % (200, 100, 150),1990:"#%02x%02x%02x" % (100, 200, 150),2000:"#%02x%02x%02x" % (150, 200, 250),2010:"#%02x%02x%02x" % (150, 150, 200)}
    

    hover = HoverTool(
            tooltips=[
                ("", "@desc"),
            ]
        )      
    #TOOLS="hover,crosshair,pan,wheel_zoom,zoom_in,zoom_out,box_zoom,undo,redo,reset,tap,save,box_select,poly_select,lasso_select,"
    
    p = figure(tools=[hover])
     
    
    for item in list(set(dec_list)):
        artlist= artists[artists['YearGrouped']==item]['0'].as_matrix()
        comp1 = artists[artists['YearGrouped']==item]['Comp1'].as_matrix()
        comp2 = artists[artists['YearGrouped']==item]['Comp2'].as_matrix()
        radii = 1
        source = ColumnDataSource(
            data=dict(
                x=list(comp1),
                y=list(comp2),
                desc=list(artlist),
            )
        )
        p.scatter('x', 'y', radius=radii,
              fill_color=color_dict[item], fill_alpha=0.6,
              line_color=None,source=source,legend=str(item))

    show(p)    
#    script, div = components(p)
#    return script,div
createArtGraph()   
