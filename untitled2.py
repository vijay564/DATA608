# -*- coding: utf-8 -*-
"""
Created on Sun Mar 15 10:29:25 2020

@author: rajuc
"""
conda install ploty

import ploty 
from dash.react import Dash

my_app = Dash('my app')

from dash_components import h1, PlotlyGraph, TextInput

my_app.layout = h1('Hello')

my_app.server.run(debug=True)