# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
# %% [markdown]
# # NASA Mars News
# 
# 
# %% [markdown]
# - Scrape the Mars News Site and collect the latest News Title and Paragraph Text. Assign the text to variables that you can reference later.

# %%
# Dependencies
from bs4 import BeautifulSoup as bs
import requests
import pymongo
import pandas as pd
from splinter import Browser
from webdriver_manager.chrome import ChromeDriverManager

def scrape_info():
# %%
# Initialize PyMongo to work with MongoDBs
    conn = 'mongodb://127.0.0.1:27017'
    client = pymongo.MongoClient(conn)


    # %%
    # Define database and collection
    db = client.mars_db

    # Drops collection if available to remove duplicates
    db.news.drop()
    collection = db.news


    # %%
    # Setup splinter
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)


    # %%
    # URL of page to be scraped
    url = 'https://redplanetscience.com/'
    browser.visit(url)


    # %%
    html = browser.html
    soup = bs(html, 'html.parser')

    results = soup.find_all('div', class_="list_text")

    for result in results:
    # scrape the article header 
        news_title = result.find('div', class_='content_title').text

    # scrape the article subheader
        news_des = result.find('div', class_='article_teaser_body').text


    # print article data
        print('-----------------')
        print(news_title)
        print(news_des)
    
    # Dictionary to be inserted into MongoDB
        post = {
            'news_title': news_title,
            'description': news_des,
            }

    
    # Insert dictionary into MongoDB as a document
        collection.insert_one(post)


    # %%
    # Display the MongoDB records created above
    articles = db.news.find()
    for article in articles:
        print(article)


    # %%
    browser.quit()

    # %% [markdown]
    # ## JPL Mars Space Images - Featured Image

    # %%
    # Define database and collection
    db = client.mars_db

    # Drops collection if available to remove duplicates
    db.images1.drop()
    collection = db.images1


    # %%
    # Setup splinter
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)
    url2 = 'https://spaceimages-mars.com/'
    browser.visit(url2)


    # %%
    html = browser.html
    soup = bs(html, 'html.parser')

    results2 = soup.find_all('div', class_="header")

    for result in results2:
    # scrape the article header 
        featured_image_url = soup.find_all('img')[1]["src"]
        img1_url = url2 + featured_image_url

        # print article data
        print('-----------------')
        print(img1_url)


    # Dictionary to be inserted into MongoDB
    post = {'image1_url': img1_url}

    # Insert dictionary into MongoDB as a document
    collection.insert_one(post)


    # %%
    # Display the MongoDB records created above
    images = db.images1.find()
    for image in images:
        print(image)


    # %%
    browser.quit()

    # %% [markdown]
    # ## Mars Facts

    # %%
    #Define Mars Facts webpage
    url="https://galaxyfacts-mars.com/"


    # %%
    #Use Pandas to scrape the tables 
    tables = pd.read_html(url)
    tables


    # %%
    #Convert to a dataframe the first table that contains the mars-earth comparison facts
    df = tables[0]
    df.head(10)


    # %%
    #Rename the titles with the first row data
    df=df.rename(columns=df.iloc[0])
    df = df.iloc[1: , :]
    df


    # %%
    #Convert the data to a HTML table string
    html_table = df.to_html('facts.html',index=False)
    html_table

    # %% [markdown]
    # ## Mars Hemispheres

    # %%
    # Define database and collection
    db = client.mars_db

    # Drops collection if available to remove duplicates
    db.images2.drop()
    collection = db.images2


    # %%
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)


    # %%
    url = 'https://marshemispheres.com/'
    browser.visit(url)


    # %%
    html = browser.html
    soup = bs(html, 'html.parser')

    products = soup.find_all('div', class_='item')

    url_list = []

    for product in products:
        img_url = product.find('a')['href']
        url_list.append(img_url)

    image_url_list = ['https://marshemispheres.com/' + url for url in url_list]

    image_url_list


    # %%
    products2 = soup.find_all('div', class_='description')

    title_list = []

    for product in products2:
        title = product.find('h3').text
        title_list.append(title)
        
    title_list


    # %%
    titles_and_urls = zip(title_list, image_url_list)

    result_list = dict(titles_and_urls)
        
    print(result_list)


    # %%
    # Dictionary to be inserted into MongoDB

    hemisphere_image_urls =[
        {"title_image": "Cerberus Hemisphere Enhanced", "img2_url": "https://marshemispheres.com/cerberus.html"},
        {"title_image": "Schiaparelli Hemisphere Enhanced", "img2_url": "https://marshemispheres.com/schiaparelli.html"},
        {"title_image": "Syrtis Major Hemisphere Enhanced", "img2_url": "https://marshemispheres.com/syrtis.html"},
        {"title_image": "Valles Marineris Hemisphere Enhanced", "img2_url": "https://marshemispheres.com/valles.html"}]

    # Insert dictionary into MongoDB as a document
    collection.insert_many(hemisphere_image_urls)


    # %%
    # Display the MongoDB records created above
    images = db.images2.find()
    for image in images:
        print(image)


    # %%
    browser.quit()


    # %%
    return mars_data


