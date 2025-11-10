from flask import Flask, request, render_template, flash
from markupsafe import Markup

import os
import json



app = Flask(__name__)


@app.route('/')
def home():
    return render_template('home.html')
    
    
    
@app.route("/p1")
def render_page1():
   earthquakes = get_earthquake_locations()
   return render_template('page1.html', earthquake_options=earthquakes)
   

    
@app.route("/p2")
def render_page2():
    magnitudes = magnitude_over_time()
    return render_template('page2.html', magnitudes=magnitudes)



@app.route("/p3")
def render_page3():
   earthquakes = get_earthquake_locations()
   return render_template('page3.html', earthquake_options=earthquakes)
     
    
    
@app.route('/showFact')
def render_fact():
    earthquake_locations = get_earthquake_locations()
    location = request.args.get('location')
    highest_mag_in_location = highest_magnitude_earthquake(location)
    fact = "In " + location + " the highest magnitude earthquake to happen in 2016 is " + str(highest_mag_in_location)
    return render_template('page1_extend.html', earthquake_options=earthquake_locations, funFact=fact)
    
@app.route('/showFact2')
def render_fact2():
    earthquake_locations = get_earthquake_locations()
    location = request.args.get('location')
    highest_mag_in_location = highest_magnitude_earthquake(location)
    fact = "In " + location + " the highest magnitude earthquake to happen in 2016 is " + str(highest_mag_in_location)
    return render_template('page3_extend.html', earthquake_options=earthquake_locations, funFact=fact)
    
    
def get_earthquake_locations():
    """returns the locations of all the earthquakes."""
    with open('earthquakes.json') as earthquake_data:
        earthquakes = json.load(earthquake_data)
    locations=[]
    for earthquake in earthquakes:
        if earthquake["location"]["name"] not in locations:
            locations.append(earthquake["location"]["name"])
    options=""
    for loc in locations:
        options += Markup("<option value=\"" + loc + "\">" + loc + "</option>") #Use Markup so <, >, " are not escaped lt, gt, etc.
    return options
    
    
def highest_magnitude_earthquake(location):
    """Returns the highest magnitude earthquake to happen in that location."""
    with open('earthquakes.json') as earthquake_data:
        earthquakes = json.load(earthquake_data)
    highest = 0
    for earthquake in earthquakes:
        if earthquake["location"]["name"] == location and earthquake["impact"]["magnitude"] > highest:
            highest = earthquake["impact"]["magnitude"]
            
    return highest
    
def magnitude_over_time():
    """ makes the graph data """
    with open('earthquakes.json') as earthquake_data:
        earthquakes = json.load(earthquake_data)
        
    earthquake_mags = []
    for earthquake in earthquakes:
        earthquake_mags.append({"x": earthquake["time"]["epoch"], "y": earthquake["impact"]["magnitude"]})
        
    return Markup(earthquake_mags)
 
 
    

if __name__ == '__main__':
    app.run(debug=True) # change to False when running in production
