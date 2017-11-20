# -*- coding: utf-8 -*-
"""
Created on Thu Jan  5 15:39:58 2017

@author: n0267335
"""

from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World!'