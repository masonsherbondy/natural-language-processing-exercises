from bs4 import BeautifulSoup
import numpy as np
import pandas as pd
import requests
import time
import os


def get_blog_articles():
    
    '''
    This function acquires the blog articles from the Codeup Blog
    '''

    if os.ispath.file('codeup_blog_2022-02-04.json'):    # set up if-conditional to see if json file is available
        blogs = pd.read_json('codeup_blog_2022-02-04.json')    # load the json file with pandas if so
    
    else:    # otherwise...
    
        url = 'https://codeup.com/blog/'    # define url to scrape
        headers = {'User-Agent': 'Codeup Data Server'}    # define headers
        response = requests.get(url, headers = headers)    # get a response from the server
        html = response.text    # assign variable to text requested
        soup = BeautifulSoup(html)    # convert html into a good soup

        entry_titles = soup.select('.entry-title')    # select .entry-title elements
        output = []    # set an empty list

        for n in range(len(entry_titles)):    # commence loop to run through list of .entry-title elements
            link = entry_titles[n].a['href']    # get link
            title = entry_titles[n].a.text    # get title
            response = requests.get(link, headers = headers)    # get response with requests library
            html = response.text    # get html
            soup = BeautifulSoup(html)    # water the soup
            corpus = soup.select('.entry-content')    # get the corpus
            content = corpus[0].text.strip()    # get the content of the corpus
            publish_date = soup.select('.published')    # get publish date
            date = publish_date[0].text    # get date

            article_info = {               # create dictionary
                'publish_date': date,
                'article': title,
                'content': content,
                'link': link
            }

            output.append(article_info)    # add dictionary to the list

        blogs = pd.DataFrame(output)    # create dataframe from accumulated info

        today = time.strftime('%Y-%m-%d')    # set today's date in a variable
        blogs.to_json(f'codeup_blog_{today}.json')    # cache data in a json file using the date as part of the file name
    
    return blogs



def get_news_articles(category):        

    '''
    This function acquires the news articles from the inshorts website for a specificied category of news. Also, this function conveniently only works for the business category
    '''
    
    url = f'https://inshorts.com/en/read/{category}'    # define url
    headers = {'User-Agent': 'Codeup Data Server'}     # define headers
    response = requests.get(url, headers = headers)    # get a response from the server
    html = response.text    # assign variable to text requested
    soup = BeautifulSoup(html)    # convert html
    
    output = []    # set an empty list to fill with dictionaries
    
    cards = soup.select('.news-card')    # select all news-cards
    
    # commence loop
    for n in range(len(cards)):
        headline = cards[n].find('span', itemprop = 'headline').text    # get headline
        corpus = cards[n].find('div', itemprop = 'articleBody').text    # get corpus
        date = cards[n].find('span', clas = 'date').text    # get date
        author = cards[n].find('span', class_ = 'author').text    # get author
        source = cards[n].find('a', class_ = 'source')['href'].strip()    # get source link
    
        article_info = {'publish_date': date,    # create dictionary from gathered values
                        'article': headline,
                        'content': corpus,
                        'author': author,
                        'source': source
                       }
        
        output.append(article_info)    # add dictionaries to list
    
    inshorts = pd.DataFrame(output)    # plug dataframe
    
    return inshorts


def get_news(category):
    
    '''
    This function acquires the news articles from the inshorts website for a specificied category of news
    '''
    
    url = f'https://inshorts.com/en/read/{category}'    # define url
    headers = {'User-Agent': 'Codeup Data Server'}     # define headers
    response = requests.get(url, headers = headers)    # get a response from the server
    html = response.text    # assign variable to text requested
    soup = BeautifulSoup(html)    # convert html
    
    output = []    # set an empty list to fill with dictionaries
    
    cards = soup.select('.news-card')    # select all news-cards
    
    # commence loop
    for n in range(len(cards)):
        headline = cards[n].find('span', itemprop = 'headline').text    # get headline
        corpus = cards[n].find('div', itemprop = 'articleBody').text    # get corpus
        date = cards[n].find('span', clas = 'date').text    # get date
        author = cards[n].find('span', class_ = 'author').text    # get author
    
        article_info = {'category': category,    # create dictionary from gathered values
                        'publish_date': date,    
                        'article': headline,
                        'content': corpus,
                        'author': author,
                       }
        
        output.append(article_info)    # add dictionaries to list
    
    inshorts = pd.DataFrame(output)    # plug dataframe
    
    return inshorts


def get_inshorts():
    
    '''
    This function loops through the aforementioned categories and scrapes news article info from these pages
    '''
    
    if os.ispath.file('inshorts_nadir.csv'):    # set up if-conditional to see if a .csv is available
        inshorts = pd.read_csv('inshorts_nadir.csv', index_col = 0)    # load dataframe if it is
    
    else:    # otherwise...

        categories = ['business', 'sports', 'technology', 'entertainment']    # set a list of desired categories
        inshorts = pd.DataFrame()    # set an empty frame
        for cat in categories:    # commence loop
            df = get_news(cat)    # render dataframe from news article data
            inshorts = pd.concat([inshorts, df])    # concatenate dataframes
    
    return inshorts