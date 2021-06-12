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
    img2_url = db.images2.find()
    title_image = db.images2.find()
    # Return template and data
    return render_template("index.html", news_title=news_title, description=description, img2_url=img2_url, title_image=title_image )


# Route that will trigger the scrape function
#@app.route("/scrape")
#def scrape():

    # Run the scrape function
#    mars_data = scrape_mars.scrape_info()

    # Update the Mongo database using update and upsert=True
#    db.update({}, mars_data, upsert=True)

    # Redirect back to home page
#    return redirect("/")


if __name__ == "__main__":
   app.run(debug=True) 
