
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
    # Define database
    db = client.mars_db


    # %%
    # Drops collection if available to remove duplicates, insert collection
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

    #find all division and class with news    
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
    # define tthe collection and Drops collection if available to remove duplicates
    db.images1.drop()
    collection = db.images1


    # %%
    # Setup splinter
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)
    url2 = 'https://spaceimages-mars.com/'
    browser.visit(url2)


    # %%
    #use browser and besutiful soup to read the website   
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
    # define the collection and Drops collection if available to remove duplicates
    db.facts.drop()
    collection = db.facts


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
    #convert the dataframe into a dictionary with the rows as keys
    data=df.to_dict('records')
    data


    # %%
    #insert the data in the collection
    collection.insert_many(data)


    # %%
    #Convert the data to a HTML table string
    html_table = df.to_html('facts.html',index=False)
    html_table

    # %% [markdown]
    # ## Mars Hemispheres

    # %%
    # define the collection adn Drops collection if available to remove duplicates
    db.images2.drop()
    collection = db.images2


    # %%
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)


    # %%
    url = 'https://marshemispheres.com/'
    browser.visit(url)
    #browser.links.find_by_partial_text('Hemisphere Enhanced').click()


    # %%
    #use browser and besutiful soup to read the website 
    html = browser.html
    soup = bs(html, 'html.parser')
    products1 = soup.find_all('div', class_='item')

    #collect all the routes of hemispheres images

    url_list=[]

    for product in products1:
        link = product.find('a')["href"]
        url_list.append(link)
        
    image_url_list = ['https://marshemispheres.com/' + url for url in url_list]
    image_url_list 


    # %%
    #retrieve all the links of the full images and titles of hemispheres images
    img2_url=[]
    title_list = []

    for url in image_url_list:
        html = browser.html
        soup = bs(html, 'html.parser')
        browser.visit(url)
        img_url = soup.find_all('div', id="wide-image", class_="wide-image-wrapper")
        for img in img_url:
            img2= img.find('img', class_='wide-image')['src']
            img2_url.append(img2)
        html = browser.html
        soup = bs(html, 'html.parser')
        browser.visit(url)
        img_title = soup.find_all('div', class_="cover")
        for title in img_title:
            title= title.find('h2', class_='title').text
            title_list.append(title)
                
    img2_links= ['https://marshemispheres.com/' + url for url in img2_url]
    img2_links


    # %%
    title_list


    # %%
    # Dictionary to be inserted into MongoDB

    hemisphere_image_urls =[
        {"title_image": "Cerberus Hemisphere Enhanced", "img2_url": "https://marshemispheres.com/images/39d3266553462198bd2fbc4d18fbed17_cerberus_enhanced.tif_thumb.png"},
        {"title_image": "Schiaparelli Hemisphere Enhanced", "img2_url": "https://marshemispheres.com/images/08eac6e22c07fb1fe72223a79252de20_schiaparelli_enhanced.tif_thumb.png"},
        {"title_image": "Syrtis Major Hemisphere Enhanced", "img2_url": "https://marshemispheres.com/images/55a0a1e2796313fdeafb17c35925e8ac_syrtis_major_enhanced.tif_thumb.png"},
        {"title_image": "Valles Marineris Hemisphere Enhanced", "img2_url": "https://marshemispheres.com/images/4e59980c1c57f89c680c0e1ccabbeff1_valles_marineris_enhanced.tif_thumb.png"}]

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



    # %%

    return hemisphere_image_urls

