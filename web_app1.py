from flask import Flask, request, render_template

from PIL import Image
import csv
import math
import pygal
import PlotGDP3

app = Flask(__name__)

@app.route('/')
def home_page():
    return render_template('Home.html', chart = None, inyear=2010)

@app.route('/', methods = ['POST'])
def display_map():
    input_year=request.form['year']
    worldmap_chart=PlotGDP3.test_render_world_map(input_year)
    # creating a object
    chart = worldmap_chart.render_data_uri()
    return render_template( 'Home.html', chart = chart, inyear=input_year)

if __name__=='__main__':
   app.run()
