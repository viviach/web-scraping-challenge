from re import template
from flask import Flask, render_template, redirect
import pymongo
from flask_pymongo import PyMongo
import scrape_mars

# Create an instance of Flask
app = Flask(__name__)

# Create connection variable
conn = 'mongodb://localhost:27017'

# Pass connection to the pymongo instance.
client = pymongo.MongoClient(conn)

# Define database and collection
db = client.mars_db

# Route to render index.html template using data from Mongo
@app.route("/")
def index():
    # Find one record of data from the mongo database
    news_title = db.news.find_one()
    description = db.news.find_one()
    img1_url=db.images1.find()
    img2_url = db.images2.find()
    title_image = db.images2.find()
    mars_diameter=db.facts.find()
    earth_diameter=db.facts.find()
    mars_mass=db.facts.find()
    earth_mass=db.facts.find()
    mars_moons=db.facts.find()
    earth_moons=db.facts.find()
    mars_distance=db.facts.find()
    earth_distance=db.facts.find()
    mars_year=db.facts.find()
    earth_year=db.facts.find()
    mars_temp=db.facts.find()
    earth_temp=db.facts.find()
    # Return template and data
    return render_template("index.html", 
    news_title=news_title, description=description, 
    img1_url=img1_url, img2_url=img2_url, title_image=title_image,
    mars_diameter=mars_diameter,earth_diameter=earth_diameter, 
    mars_mass=mars_mass, earth_mass=earth_mass,
    mars_distance=mars_distance, earth_distance=earth_distance,
    mars_moons=mars_moons, earth_moons=earth_moons,
    mars_year=mars_year, earth_year=earth_year, 
    mars_temp=mars_temp, earth_temp=earth_temp )


# Route that will trigger the scrape function
@app.route("/scrape")
def scrape():

    # Run the scrape function
    mars_data = scrape_mars.scrape_info()


    # Redirect back to home page
    return redirect("/")


if __name__ == "__main__":
   app.run(debug=True) 
