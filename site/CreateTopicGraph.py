# -*- coding: utf-8 -*-
"""
Created on Thu Jun  8 14:14:00 2017

@author: christopherhedenberg
"""

import pandas as pd
from bokeh.charts import Donut,output_file
from bokeh.embed import components
from bokeh.plotting import figure,ColumnDataSource, show
import numpy as np
from bokeh.models import HoverTool
from bokeh.models import Range1d
from bokeh.charts.utils import df_from_json
from bokeh.sampledata.olympics2014 import data
def createTopicGraph():
    words = pd.read_csv("/Users/christopherhedenberg/Downloads/projects/RapThesaurus/ModelOutput/TopicCountTotal.csv")
    words = words.drop('Unnamed: 0',axis=1)    
    words.columns=['Topic','Count','Word']

    # original example
    d = Donut(words, label=['Topic'], values='Count',
              text_font_size='8pt', hover_text='word_count')


    script, div = components(d)
    return script,div
    