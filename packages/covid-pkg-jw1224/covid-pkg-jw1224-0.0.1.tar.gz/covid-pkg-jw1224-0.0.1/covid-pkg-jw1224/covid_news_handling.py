'''
This module handles the news articles for the Covid Dashboard.
It retrieves the articles using an API request and then adds them to a list in order to be displayed.
'''

import requests
import json
from typing import List

covid_terms = "Covid COVID-19 coronavirus"
domains = "bbc.co.uk, theguardian.com, telegraph.co.uk, independent.co.uk, dailymail.co.uk"
news_articles = []
deleted_articles = []


def news_API_request(covid_terms: str, domains: str) -> List:
    '''Sends an API request for news given specific Covid-19 related terms and domains'''
    complete_URL = f"https://newsapi.org/v2/everything?language=en&q={covid_terms}&domains={domains}&sortBy=publishedAt&apiKey=b87f970d167a4eb7b34e6b8482756383"
    results = requests.get(complete_URL).json()
    articles = results["articles"]

    return articles

    


def update_news() -> List:
    '''Updates the current list of news articles'''
    news_results = news_API_request(covid_terms, domains)
    for result in news_results:
        skip = False
        for article in news_articles:
            if result['title'] == article['title']:
                skip = True
        for del_art in deleted_articles:
            if result['title'] == del_art:
                skip = True
        if skip == True:
            continue
        else:
            news_articles.append(result)
    for news in news_articles:
        news['content'] = news['url']
    return news_articles
        
def delete_news(news_title: str):
    '''Adds any deleted article to a blacklist'''
    deleted_articles.append(news_title)    

