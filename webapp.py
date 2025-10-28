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
    return render_template('page2.html')



@app.route("/p3")
def render_page3():
    return render_template('page3.html')
     
    
    
@app.route('/showFact')
def render_fact():
    earthquake_locations = get_earthquake_locations()
    location = request.args.get('location')
    highest_mag_in_location = highest_magnitude_earthquake(location)
    fact = "In " + location + " the highest magnitude earthquake to happen is " + highest_mag_in_location + "."
    return render_template('page1.html', earthquake_options=earthquake_locations, funFact=fact)
    
    
def get_earthquake_locations():
    """Return the html code for the drop down menu.  Each option is a state abbreviation from the demographic data."""
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
    """Return the name of a county in the given state with the highest percent of under 18 year olds."""
    with open('earthquakes.json') as earthquake_data:
        earthquakes = json.load(earthquake_data)
    highest=0
    location = ""
    for earthquake in earthquakes and earthquake["location"]["name"] == location:
        if earthquake["impact"]["magnitude"] > highest:
            highest = earthquake["impact"]["magnitude"]
            location = earthquake["location"]["name"]
    return highest
 
 
    

if __name__ == '__main__':
    app.run(debug=True) # change to False when running in production
