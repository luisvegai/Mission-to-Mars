#!/usr/bin/env python
# coding: utf-8

# Import Splinter and BeautifulSoup
from splinter import Browser
from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import datetime as dt
import time
import re

def scrape_all():
    # Initiate headless driver for deployment
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path)
    # browser = Browser("chrome", executable_path="chromedriver", headless=True)
    news_title, news_paragraph = mars_news(browser)
# Run all scraping functions and store results in dictionary
    data = {
        "news_title": news_title,
        "news_paragraph": news_paragraph,
        "featured_image": featured_image(browser),
        "facts": mars_facts(),
        "last_modified": dt.datetime.now(),
        "h_im": hem_images(browser),
        "t_im": thu_images(browser)
    }
    browser.quit()
    return data


def mars_news(browser):

    # Visit the mars nasa news site
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)

    # Optional delay for loading the page
    browser.is_element_present_by_css("ul.item_list li.slide", wait_time=1)

    # Convert the browser html to a soup object and then quit the browser
    html = browser.html
    news_soup = BeautifulSoup(html, 'html.parser')
   
    # Add try/except for error handling
    try:
        slide_elem = news_soup.select_one("ul.item_list li.slide")
        # Use the parent element to find the first 'a' tag and save it as 'news_title'
        news_title = slide_elem.find("div", class_="content_title").get_text()
        # Use the parent element to find the paragraph text
        news_p = slide_elem.find("div", class_="article_teaser_body").get_text()
        return news_title, news_p
    except AttributeError:
        return None, None


def featured_image(browser):
    # Visit URL
    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)

    # Find and click the full image button
    full_image_elem = browser.find_by_id('full_image')
    full_image_elem.click()

    # Find the more info button and click that
    browser.is_element_present_by_text('more info', wait_time=1)
    more_info_elem = browser.links.find_by_partial_text('more info')
    more_info_elem.click()

    # Parse the resulting html with soup
    html = browser.html
    img_soup = BeautifulSoup(html, 'html.parser')

    try:
        # Find the relative image url
        img_url_rel = img_soup.select_one('figure.lede a img').get("src")
        # img_url_rel
        # Use the base URL to create an absolute URL
        img_url = f'https://www.jpl.nasa.gov{img_url_rel}'
        return img_url
    except:
        return None


def mars_facts():
    # Add try/except for error handling
    try:
        # Use 'read_html' to scrape the facts table into a dataframe
        df = pd.read_html('http://space-facts.com/mars/')[0]

    except BaseException:
        return None

    # Assign columns and set index of dataframe
    df.columns=['Description', 'Mars']
    df.set_index('Description', inplace=True)

    # Convert dataframe into HTML format, add bootstrap
    return df.to_html()


def hem_images(browser):
    # Visit URL
    url = 'https://2u-data-curriculum-team.s3.amazonaws.com/dataviz-online-content/module_10/Astropedia+Search+Results+_+USGS+Astrogeology+Science+Center.htm'
    browser.visit(url)

    imf_dict=[]
    for el in range(4):
        more_info_elem = browser.find_by_css('img[class="thumb"]')
        more_info_elem = list(more_info_elem)
        more_info_elem[el].click()
        time.sleep(2)
        html = browser.html
        img_soup = BeautifulSoup(html, 'html.parser')
        try:
            imga_all = img_soup.select('div.downloads ul li a')
            imga_l=imga_all[1]['href']
        #    print(imga_l)
            imgt = img_soup.find('h2').text
        #    print(imgt)
            case = {'title': imgt, 'img_url': imga_l }
            imf_dict.append(case)
            browser.back()
        except:
            browser.back()
        return imf_dict

def thu_images(browser):
    # Visit URL
    url = 'https://2u-data-curriculum-team.s3.amazonaws.com/dataviz-online-content/module_10/Astropedia+Search+Results+_+USGS+Astrogeology+Science+Center.htm'
    browser.visit(url)

    html = browser.html
    img_soup = BeautifulSoup(html, 'html.parser')
    try:
        imgt_all = img_soup.select('div.item img.thumb')
        imt_dict = []
        for it in imgt_all:
            its = it['src'].replace(" ", "%20")
            its_url = f'https://2u-data-curriculum-team.s3.amazonaws.com/dataviz-online-content/module_10{its[1:]}'
        #    print(it_url)
            ita =it['alt']
        #    print(ita)
            case = {'title': ita, 'img_url': its_url }
            imt_dict.append(case)
    except:
        imt_dict = imt_dict
    return imt_dict

if __name__ == "__main__":
    # If running as script, print scraped data
    print(scrape_all())
