# Dependencies
from bs4 import BeautifulSoup
from splinter import Browser
import requests
import pymongo
import pandas as pd
from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
from webdriver_manager.chrome import ChromeDriverManager
import time

def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {"executable_path": "chromedriver.exe"}
    return Browser("chrome", **executable_path, headless=False)

def scrape():
    browser = init_browser()
    
    ##### __NASA Mars News__ #####
    # URL of page to be scraped
    url = 'https://mars.nasa.gov/news/'
    # Retrieve page with the requests module
    response = requests.get(url)
    # Create BeautifulSoup object; parse with 'html.parser'
    soup = BeautifulSoup(response.text, 'html.parser')
    # Collect the latest News Title assign the text to a variable that can be referenced later.
    news_title = soup.find_all('div', class_='content_title')[0].text
    # Collect the latest paragragph and assign the text to a variable that can be referenced later.
    news_p = soup.find_all('div', class_='rollover_description_inner')[0].text
    # Close the browser after scraping
    browser.quit()


    #### __JPL Mars Space Images - Featured Image__ ####
    browser = init_browser()
    # Setup Splinter
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)
    # Set up browser to connect to url and scrape
    url = 'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/index.html'
    browser.visit(url)
    # Click on FULL IMAGE button
    browser.links.find_by_partial_text('FULL IMAGE').click()
    # Create Browser and BeautifulSoup object; parse with 'html.parser'
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    # Delay code to allow link to open before trying to scrape
    time.sleep(1)
    # Scrape page to find the featured Mars image
    mars_image = soup.find('img', class_='fancybox-image')
    url = mars_image['src']
    featured_image_url = 'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/' + url
    # Close the browser after scraping
    browser.quit()



    ##### __Mars Facts__ #####
    browser = init_browser()
    # Use Pandas to scrape the table and convert the data to a HTML table string
    url = 'https://space-facts.com/mars/'
    mars_table = pd.read_html(url)
    mars_data_df = mars_table[0]
    mars_html_table = mars_data_df.to_html(classes='table table-striped' 'table-bordered', index=False, header = False, border=1)
    # #Close the browser after scraping
    browser.quit()



    ##### __Mars Hemispheres__ #####
    browser = init_browser()
    # Setup splinter
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)
    # Set up browser to connect to url to scrape
    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)
    # Setup empty list
    hemisphere_image_urls = []
    # Get list of hemispheres
    for i in range(4):
        hemisphere = {}
        
        time.sleep(1)
      
        # Click on each hemispher enhanced link
        browser.find_by_css("a.product-item h3")[i].click()
        
        # Scrape page to find Hemisphere title
        hemisphere["title"] = browser.find_by_css("h2.title").text
        
        # Locate sample jpg image & scrape url
        sample_element = browser.find_link_by_text("Sample").first
        hemisphere["img_url"] = sample_element["href"]

        # download = soup.find('div', class_ = 'downloads')
        # image_url = download.ul.li.a["href"]
        # hemisphere["image_url"] = image_url
        
        # Add data to hemisphere dictionary
        hemisphere_image_urls.append(hemisphere)
        
        # Navigate back to Products page to continue through range
        browser.back()

    # Close the browser after scraping
    browser.quit()



    # Python dictionary containing all of the scraped data.
    mars_data = {
        "news_title": news_title,
        "news_p": news_p,
        "featured_image_url": featured_image_url,
        "mars_html_table": mars_html_table,
        "hemisphere_image_urls": hemisphere_image_urls
    }

    # Close remaing browser
    browser.quit()
    # Return results
    return mars_data