#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "Davide Locatelli"
__status__ = "Production"

"""
These tests cover Sentrade usage.
"""

from result import SentradeResultPage
from search import SentradeHomePage
from dash.testing.application_runners import import_app

def test_aapl_ticker_search_graph_title(browser):
  home_page = SentradeHomePage(browser)
  result_page = SentradeResultPage(browser)
  TICKER = "AAPL"

  # Given the Sentrade home page is displayed
  home_page.load()

  # When the user searches for TICKER
  home_page.search(TICKER)
  
  # Assert that the graph title is TICKER
  assert result_page.result_count_for_graph(TICKER) == 1

def test_aapl_ticker_search_graph_subtitle(browser):
  home_page = SentradeHomePage(browser)
  result_page = SentradeResultPage(browser)
  TICKER = "AAPL"

  # Given the Sentrade home page is displayed
  home_page.load()

  # When the user searches for TICKER
  home_page.search(TICKER)
  
  # Assert the graph subtitle pertain to TICKER
  companies = {
            "AMZN" : "Amazon.com Inc.",
            "AAPL"  : "Apple Inc.", 
            "FB"    : "Facebook Inc.",
            "GOOG"  : "Alphabet Inc.",
            "MSFT"  : "Microsoft Corporation",
            "NFLX"  : "Netflix Inc.",
            "TSLA"  : "Tesla Inc.",
            "UBER"  : "Uber Technologies Inc."
        }

  assert result_page.result_count_for_graph(companies[TICKER]) == 1

def test_aapl_ticker_search_news_count(browser):
  home_page = SentradeHomePage(browser)
  result_page = SentradeResultPage(browser)
  TICKER = "AAPL"

  # Given the Sentrade home page is displayed
  home_page.load()

  # When the user searches for TICKER
  home_page.search(TICKER)
  
  # Assert there are 10 headlines
  assert result_page.result_count_for_news() == 10


def test_aapl_ticker_search_news_pertinence(browser):
  home_page = SentradeHomePage(browser)
  result_page = SentradeResultPage(browser)
  TICKER = "AAPL"

  # Given the Sentrade home page is displayed
  home_page.load()

  # When the user searches for TICKER
  home_page.search(TICKER)
  
  # Assert there are pertinent headlines
  companies = {
            "AMZN" : "Amazon",
            "AAPL"  : "Apple", 
            "FB"    : "Facebook",
            "GOOG"  : "Alphabet",
            "MSFT"  : "Microsoft",
            "NFLX"  : "Netflix",
            "TSLA"  : "Tesla",
            "UBER"  : "Uber"
        }

  assert result_page.result_contents_for_news(companies[TICKER])

def test_aapl_ticker_search_news_color(browser):
  home_page = SentradeHomePage(browser)
  result_page = SentradeResultPage(browser)
  TICKER = "AAPL"

  # Given the Sentrade home page is displayed
  home_page.load()

  # When the user searches for TICKER
  home_page.search(TICKER)
  assert result_page.colored_contents_for_news()
'''
def test_graph_range_buttons(browser):
  home_page = SentradeHomePage(browser)
  result_page = SentradeResultPage(browser)
  TICKER = "AAPL"

  # Given the Sentrade home page is displayed
  home_page.load()

  # When the user searches for TICKER
  home_page.search(TICKER)
  assert result_page.click_buttons()
'''

def test_aapl_ticker_search_tweets_count(browser):
  home_page = SentradeHomePage(browser)
  result_page = SentradeResultPage(browser)
  TICKER = "AAPL"

  # Given the Sentrade home page is displayed
  home_page.load()

  # When the user searches for TICKER
  home_page.search(TICKER)
  
  # Assert there are 10 tweets
  assert result_page.result_count_for_tweets() == 10


def test_aapl_ticker_search_tweets_pertinence(browser):
  home_page = SentradeHomePage(browser)
  result_page = SentradeResultPage(browser)
  TICKER = "AAPL"

  # Given the Sentrade home page is displayed
  home_page.load()

  # When the user searches for TICKER
  home_page.search(TICKER)
  
  # Assert there are pertinent tweets
  companies = {
            "AMZN" : "Amazon",
            "AAPL"  : "Apple", 
            "FB"    : "Facebook",
            "GOOG"  : "Alphabet",
            "MSFT"  : "Microsoft",
            "NFLX"  : "Netflix",
            "TSLA"  : "Tesla",
            "UBER"  : "Uber"
        }

  assert result_page.result_contents_for_tweets(companies[TICKER])

def test_aapl_ticker_search_tweets_color(browser):
    home_page = SentradeHomePage(browser)
    result_page = SentradeResultPage(browser)
    TICKER = "AAPL"

    # Given the Sentrade home page is displayed
    home_page.load()

    # When the user searches for TICKER
    home_page.search(TICKER)
    assert result_page.colored_contents_for_tweets()

def test_aapl_ticker_search_finance_data(browser):
    home_page = SentradeHomePage(browser)
    result_page = SentradeResultPage(browser)
    TICKER = "AAPL"

    # Given the Sentrade home page is displayed
    home_page.load()

    # When the user searches for TICKER
    home_page.search(TICKER)
    assert result_page.result_count_for_finance() == 1

def test_aapl_ticker_search_sentiment_data(browser):
    home_page = SentradeHomePage(browser)
    result_page = SentradeResultPage(browser)
    TICKER = "AAPL"

    # Given the Sentrade home page is displayed
    home_page.load()

    # When the user searches for TICKER
    home_page.search(TICKER)
    assert result_page.result_count_for_sentiment() == 1

#######################
def test_amzn_ticker_search_graph_title(browser):
  home_page = SentradeHomePage(browser)
  result_page = SentradeResultPage(browser)
  TICKER = "AMZN"

  # Given the Sentrade home page is displayed
  home_page.load()

  # When the user searches for TICKER
  home_page.search(TICKER)
  
  # Assert that the graph title is TICKER
  assert result_page.result_count_for_graph(TICKER) == 1

def test_amzn_ticker_search_graph_subtitle(browser):
  home_page = SentradeHomePage(browser)
  result_page = SentradeResultPage(browser)
  TICKER = "AMZN"

  # Given the Sentrade home page is displayed
  home_page.load()

  # When the user searches for TICKER
  home_page.search(TICKER)
  
  # Assert the graph subtitle pertain to TICKER
  companies = {
            "AMZN" : "Amazon.com Inc.",
            "AAPL"  : "Apple Inc.", 
            "FB"    : "Facebook Inc.",
            "GOOG"  : "Alphabet Inc.",
            "MSFT"  : "Microsoft Corporation",
            "NFLX"  : "Netflix Inc.",
            "TSLA"  : "Tesla Inc.",
            "UBER"  : "Uber Technologies Inc."
        }

  assert result_page.result_count_for_graph(companies[TICKER]) == 1

def test_amzn_ticker_search_news_count(browser):
  home_page = SentradeHomePage(browser)
  result_page = SentradeResultPage(browser)
  TICKER = "AMZN"

  # Given the Sentrade home page is displayed
  home_page.load()

  # When the user searches for TICKER
  home_page.search(TICKER)
  
  # Assert there are 10 headlines
  assert result_page.result_count_for_news() == 10


def test_amzn_ticker_search_news_pertinence(browser):
  home_page = SentradeHomePage(browser)
  result_page = SentradeResultPage(browser)
  TICKER = "AMZN"

  # Given the Sentrade home page is displayed
  home_page.load()

  # When the user searches for TICKER
  home_page.search(TICKER)
  
  # Assert there are pertinent headlines
  companies = {
            "AMZN" : "Amazon",
            "AAPL"  : "Apple", 
            "FB"    : "Facebook",
            "GOOG"  : "Alphabet",
            "MSFT"  : "Microsoft",
            "NFLX"  : "Netflix",
            "TSLA"  : "Tesla",
            "UBER"  : "Uber"
        }

  assert result_page.result_contents_for_news(companies[TICKER])

def test_amzn_ticker_search_news_color(browser):
  home_page = SentradeHomePage(browser)
  result_page = SentradeResultPage(browser)
  TICKER = "AMZN"

  # Given the Sentrade home page is displayed
  home_page.load()

  # When the user searches for TICKER
  home_page.search(TICKER)
  assert result_page.colored_contents_for_news()

def test_amzn_ticker_search_tweets_count(browser):
  home_page = SentradeHomePage(browser)
  result_page = SentradeResultPage(browser)
  TICKER = "AMZN"

  # Given the Sentrade home page is displayed
  home_page.load()

  # When the user searches for TICKER
  home_page.search(TICKER)
  
  # Assert there are 10 tweets
  assert result_page.result_count_for_tweets() == 10


def test_amzn_ticker_search_tweets_pertinence(browser):
  home_page = SentradeHomePage(browser)
  result_page = SentradeResultPage(browser)
  TICKER = "AMZN"

  # Given the Sentrade home page is displayed
  home_page.load()

  # When the user searches for TICKER
  home_page.search(TICKER)
  
  # Assert there are pertinent tweets
  companies = {
            "AMZN" : "Amazon",
            "AAPL"  : "Apple", 
            "FB"    : "Facebook",
            "GOOG"  : "Alphabet",
            "MSFT"  : "Microsoft",
            "NFLX"  : "Netflix",
            "TSLA"  : "Tesla",
            "UBER"  : "Uber"
        }

  assert result_page.result_contents_for_tweets(companies[TICKER])

def test_amzn_ticker_search_tweets_color(browser):
    home_page = SentradeHomePage(browser)
    result_page = SentradeResultPage(browser)
    TICKER = "AMZN"

    # Given the Sentrade home page is displayed
    home_page.load()

    # When the user searches for TICKER
    home_page.search(TICKER)
    assert result_page.colored_contents_for_tweets()

def test_amzn_ticker_search_finance_data(browser):
    home_page = SentradeHomePage(browser)
    result_page = SentradeResultPage(browser)
    TICKER = "AMZN"

    # Given the Sentrade home page is displayed
    home_page.load()

    # When the user searches for TICKER
    home_page.search(TICKER)
    assert result_page.result_count_for_finance() == 1

def test_amzn_ticker_search_sentiment_data(browser):
    home_page = SentradeHomePage(browser)
    result_page = SentradeResultPage(browser)
    TICKER = "AMZN"

    # Given the Sentrade home page is displayed
    home_page.load()

    # When the user searches for TICKER
    home_page.search(TICKER)
    assert result_page.result_count_for_sentiment() == 1
###################
def test_fb_ticker_search_graph_title(browser):
  home_page = SentradeHomePage(browser)
  result_page = SentradeResultPage(browser)
  TICKER = "FB"

  # Given the Sentrade home page is displayed
  home_page.load()

  # When the user searches for TICKER
  home_page.search(TICKER)
  
  # Assert that the graph title is TICKER
  assert result_page.result_count_for_graph(TICKER) == 1

def test_fb_ticker_search_graph_subtitle(browser):
  home_page = SentradeHomePage(browser)
  result_page = SentradeResultPage(browser)
  TICKER = "FB"

  # Given the Sentrade home page is displayed
  home_page.load()

  # When the user searches for TICKER
  home_page.search(TICKER)
  
  # Assert the graph subtitle pertain to TICKER
  companies = {
            "AMZN" : "Amazon.com Inc.",
            "AAPL"  : "Apple Inc.", 
            "FB"    : "Facebook Inc.",
            "GOOG"  : "Alphabet Inc.",
            "MSFT"  : "Microsoft Corporation",
            "NFLX"  : "Netflix Inc.",
            "TSLA"  : "Tesla Inc.",
            "UBER"  : "Uber Technologies Inc."
        }

  assert result_page.result_count_for_graph(companies[TICKER]) == 1

def test_fb_ticker_search_news_count(browser):
  home_page = SentradeHomePage(browser)
  result_page = SentradeResultPage(browser)
  TICKER = "FB"

  # Given the Sentrade home page is displayed
  home_page.load()

  # When the user searches for TICKER
  home_page.search(TICKER)
  
  # Assert there are 10 headlines
  assert result_page.result_count_for_news() == 10


def test_fb_ticker_search_news_pertinence(browser):
  home_page = SentradeHomePage(browser)
  result_page = SentradeResultPage(browser)
  TICKER = "FB"

  # Given the Sentrade home page is displayed
  home_page.load()

  # When the user searches for TICKER
  home_page.search(TICKER)
  
  # Assert there are pertinent headlines
  companies = {
            "AMZN" : "Amazon",
            "AAPL"  : "Apple", 
            "FB"    : "Facebook",
            "GOOG"  : "Alphabet",
            "MSFT"  : "Microsoft",
            "NFLX"  : "Netflix",
            "TSLA"  : "Tesla",
            "UBER"  : "Uber"
        }

  assert result_page.result_contents_for_news(companies[TICKER])

def test_fb_ticker_search_news_color(browser):
  home_page = SentradeHomePage(browser)
  result_page = SentradeResultPage(browser)
  TICKER = "FB"

  # Given the Sentrade home page is displayed
  home_page.load()

  # When the user searches for TICKER
  home_page.search(TICKER)
  assert result_page.colored_contents_for_news()

def test_fb_ticker_search_tweets_count(browser):
  home_page = SentradeHomePage(browser)
  result_page = SentradeResultPage(browser)
  TICKER = "FB"

  # Given the Sentrade home page is displayed
  home_page.load()

  # When the user searches for TICKER
  home_page.search(TICKER)
  
  # Assert there are 10 tweets
  assert result_page.result_count_for_tweets() == 10


def test_fb_ticker_search_tweets_pertinence(browser):
  home_page = SentradeHomePage(browser)
  result_page = SentradeResultPage(browser)
  TICKER = "FB"

  # Given the Sentrade home page is displayed
  home_page.load()

  # When the user searches for TICKER
  home_page.search(TICKER)
  
  # Assert there are pertinent tweets
  companies = {
            "AMZN" : "Amazon",
            "AAPL"  : "Apple", 
            "FB"    : "Facebook",
            "GOOG"  : "Alphabet",
            "MSFT"  : "Microsoft",
            "NFLX"  : "Netflix",
            "TSLA"  : "Tesla",
            "UBER"  : "Uber"
        }

  assert result_page.result_contents_for_tweets(companies[TICKER])

def test_fb_ticker_search_tweets_color(browser):
    home_page = SentradeHomePage(browser)
    result_page = SentradeResultPage(browser)
    TICKER = "FB"

    # Given the Sentrade home page is displayed
    home_page.load()

    # When the user searches for TICKER
    home_page.search(TICKER)
    assert result_page.colored_contents_for_tweets()

def test_fb_ticker_search_finance_data(browser):
    home_page = SentradeHomePage(browser)
    result_page = SentradeResultPage(browser)
    TICKER = "FB"

    # Given the Sentrade home page is displayed
    home_page.load()

    # When the user searches for TICKER
    home_page.search(TICKER)
    assert result_page.result_count_for_finance() == 1

def test_fb_ticker_search_sentiment_data(browser):
    home_page = SentradeHomePage(browser)
    result_page = SentradeResultPage(browser)
    TICKER = "FB"

    # Given the Sentrade home page is displayed
    home_page.load()

    # When the user searches for TICKER
    home_page.search(TICKER)
    assert result_page.result_count_for_sentiment() == 1
###################
def test_goog_ticker_search_graph_title(browser):
  home_page = SentradeHomePage(browser)
  result_page = SentradeResultPage(browser)
  TICKER = "GOOG"

  # Given the Sentrade home page is displayed
  home_page.load()

  # When the user searches for TICKER
  home_page.search(TICKER)
  
  # Assert that the graph title is TICKER
  assert result_page.result_count_for_graph(TICKER) == 1

def test_goog_ticker_search_graph_subtitle(browser):
  home_page = SentradeHomePage(browser)
  result_page = SentradeResultPage(browser)
  TICKER = "GOOG"

  # Given the Sentrade home page is displayed
  home_page.load()

  # When the user searches for TICKER
  home_page.search(TICKER)
  
  # Assert the graph subtitle pertain to TICKER
  companies = {
            "AMZN" : "Amazon.com Inc.",
            "AAPL"  : "Apple Inc.", 
            "FB"    : "Facebook Inc.",
            "GOOG"  : "Alphabet Inc.",
            "MSFT"  : "Microsoft Corporation",
            "NFLX"  : "Netflix Inc.",
            "TSLA"  : "Tesla Inc.",
            "UBER"  : "Uber Technologies Inc."
        }

  assert result_page.result_count_for_graph(companies[TICKER]) == 1

def test_goog_ticker_search_news_count(browser):
  home_page = SentradeHomePage(browser)
  result_page = SentradeResultPage(browser)
  TICKER = "GOOG"

  # Given the Sentrade home page is displayed
  home_page.load()

  # When the user searches for TICKER
  home_page.search(TICKER)
  
  # Assert there are 10 headlines
  assert result_page.result_count_for_news() == 10


def test_goog_ticker_search_news_pertinence(browser):
  home_page = SentradeHomePage(browser)
  result_page = SentradeResultPage(browser)
  TICKER = "GOOG"

  # Given the Sentrade home page is displayed
  home_page.load()

  # When the user searches for TICKER
  home_page.search(TICKER)
  
  # Assert there are pertinent headlines
  companies = {
            "AMZN" : "Amazon",
            "AAPL"  : "Apple", 
            "FB"    : "Facebook",
            "GOOG"  : "Alphabet",
            "MSFT"  : "Microsoft",
            "NFLX"  : "Netflix",
            "TSLA"  : "Tesla",
            "UBER"  : "Uber"
        }

  assert result_page.result_contents_for_news(companies[TICKER])

def test_goog_ticker_search_news_color(browser):
  home_page = SentradeHomePage(browser)
  result_page = SentradeResultPage(browser)
  TICKER = "GOOG"

  # Given the Sentrade home page is displayed
  home_page.load()

  # When the user searches for TICKER
  home_page.search(TICKER)
  assert result_page.colored_contents_for_news()

def test_goog_ticker_search_tweets_count(browser):
  home_page = SentradeHomePage(browser)
  result_page = SentradeResultPage(browser)
  TICKER = "GOOG"

  # Given the Sentrade home page is displayed
  home_page.load()

  # When the user searches for TICKER
  home_page.search(TICKER)
  
  # Assert there are 10 tweets
  assert result_page.result_count_for_tweets() == 10


def test_goog_ticker_search_tweets_pertinence(browser):
  home_page = SentradeHomePage(browser)
  result_page = SentradeResultPage(browser)
  TICKER = "GOOG"

  # Given the Sentrade home page is displayed
  home_page.load()

  # When the user searches for TICKER
  home_page.search(TICKER)
  
  # Assert there are pertinent tweets
  companies = {
            "AMZN" : "Amazon",
            "AAPL"  : "Apple", 
            "FB"    : "Facebook",
            "GOOG"  : "Alphabet",
            "MSFT"  : "Microsoft",
            "NFLX"  : "Netflix",
            "TSLA"  : "Tesla",
            "UBER"  : "Uber"
        }

  assert result_page.result_contents_for_tweets(companies[TICKER])

def test_goog_ticker_search_tweets_color(browser):
    home_page = SentradeHomePage(browser)
    result_page = SentradeResultPage(browser)
    TICKER = "GOOG"

    # Given the Sentrade home page is displayed
    home_page.load()

    # When the user searches for TICKER
    home_page.search(TICKER)
    assert result_page.colored_contents_for_tweets()

def test_goog_ticker_search_finance_data(browser):
    home_page = SentradeHomePage(browser)
    result_page = SentradeResultPage(browser)
    TICKER = "GOOG"

    # Given the Sentrade home page is displayed
    home_page.load()

    # When the user searches for TICKER
    home_page.search(TICKER)
    assert result_page.result_count_for_finance() == 1

def test_goog_ticker_search_sentiment_data(browser):
    home_page = SentradeHomePage(browser)
    result_page = SentradeResultPage(browser)
    TICKER = "GOOG"

    # Given the Sentrade home page is displayed
    home_page.load()

    # When the user searches for TICKER
    home_page.search(TICKER)
    assert result_page.result_count_for_sentiment() == 1
###################
def test_msft_ticker_search_graph_title(browser):
  home_page = SentradeHomePage(browser)
  result_page = SentradeResultPage(browser)
  TICKER = "MSFT"

  # Given the Sentrade home page is displayed
  home_page.load()

  # When the user searches for TICKER
  home_page.search(TICKER)
  
  # Assert that the graph title is TICKER
  assert result_page.result_count_for_graph(TICKER) == 1

def test_msft_ticker_search_graph_subtitle(browser):
  home_page = SentradeHomePage(browser)
  result_page = SentradeResultPage(browser)
  TICKER = "MSFT"

  # Given the Sentrade home page is displayed
  home_page.load()

  # When the user searches for TICKER
  home_page.search(TICKER)
  
  # Assert the graph subtitle pertain to TICKER
  companies = {
            "AMZN" : "Amazon.com Inc.",
            "AAPL"  : "Apple Inc.", 
            "FB"    : "Facebook Inc.",
            "GOOG"  : "Alphabet Inc.",
            "MSFT"  : "Microsoft Corporation",
            "NFLX"  : "Netflix Inc.",
            "TSLA"  : "Tesla Inc.",
            "UBER"  : "Uber Technologies Inc."
        }

  assert result_page.result_count_for_graph(companies[TICKER]) == 1

def test_msft_ticker_search_news_count(browser):
  home_page = SentradeHomePage(browser)
  result_page = SentradeResultPage(browser)
  TICKER = "MSFT"

  # Given the Sentrade home page is displayed
  home_page.load()

  # When the user searches for TICKER
  home_page.search(TICKER)
  
  # Assert there are 10 headlines
  assert result_page.result_count_for_news() == 10


def test_msft_ticker_search_news_pertinence(browser):
  home_page = SentradeHomePage(browser)
  result_page = SentradeResultPage(browser)
  TICKER = "MSFT"

  # Given the Sentrade home page is displayed
  home_page.load()

  # When the user searches for TICKER
  home_page.search(TICKER)
  
  # Assert there are pertinent headlines
  companies = {
            "AMZN" : "Amazon",
            "AAPL"  : "Apple", 
            "FB"    : "Facebook",
            "GOOG"  : "Alphabet",
            "MSFT"  : "Microsoft",
            "NFLX"  : "Netflix",
            "TSLA"  : "Tesla",
            "UBER"  : "Uber"
        }

  assert result_page.result_contents_for_news(companies[TICKER])

def test_msft_ticker_search_news_color(browser):
  home_page = SentradeHomePage(browser)
  result_page = SentradeResultPage(browser)
  TICKER = "MSFT"

  # Given the Sentrade home page is displayed
  home_page.load()

  # When the user searches for TICKER
  home_page.search(TICKER)
  assert result_page.colored_contents_for_news()

def test_msft_ticker_search_tweets_count(browser):
  home_page = SentradeHomePage(browser)
  result_page = SentradeResultPage(browser)
  TICKER = "MSFT"

  # Given the Sentrade home page is displayed
  home_page.load()

  # When the user searches for TICKER
  home_page.search(TICKER)
  
  # Assert there are 10 tweets
  assert result_page.result_count_for_tweets() == 10


def test_msft_ticker_search_tweets_pertinence(browser):
  home_page = SentradeHomePage(browser)
  result_page = SentradeResultPage(browser)
  TICKER = "MSFT"

  # Given the Sentrade home page is displayed
  home_page.load()

  # When the user searches for TICKER
  home_page.search(TICKER)
  
  # Assert there are pertinent tweets
  companies = {
            "AMZN" : "Amazon",
            "AAPL"  : "Apple", 
            "FB"    : "Facebook",
            "GOOG"  : "Alphabet",
            "MSFT"  : "Microsoft",
            "NFLX"  : "Netflix",
            "TSLA"  : "Tesla",
            "UBER"  : "Uber"
        }

  assert result_page.result_contents_for_tweets(companies[TICKER])

def test_msft_ticker_search_tweets_color(browser):
    home_page = SentradeHomePage(browser)
    result_page = SentradeResultPage(browser)
    TICKER = "MSFT"

    # Given the Sentrade home page is displayed
    home_page.load()

    # When the user searches for TICKER
    home_page.search(TICKER)
    assert result_page.colored_contents_for_tweets()

def test_msft_ticker_search_finance_data(browser):
    home_page = SentradeHomePage(browser)
    result_page = SentradeResultPage(browser)
    TICKER = "MSFT"

    # Given the Sentrade home page is displayed
    home_page.load()

    # When the user searches for TICKER
    home_page.search(TICKER)
    assert result_page.result_count_for_finance() == 1

def test_msft_ticker_search_sentiment_data(browser):
    home_page = SentradeHomePage(browser)
    result_page = SentradeResultPage(browser)
    TICKER = "MSFT"

    # Given the Sentrade home page is displayed
    home_page.load()

    # When the user searches for TICKER
    home_page.search(TICKER)
    assert result_page.result_count_for_sentiment() == 1
###################
def test_nflx_ticker_search_graph_title(browser):
  home_page = SentradeHomePage(browser)
  result_page = SentradeResultPage(browser)
  TICKER = "NFLX"

  # Given the Sentrade home page is displayed
  home_page.load()

  # When the user searches for TICKER
  home_page.search(TICKER)
  
  # Assert that the graph title is TICKER
  assert result_page.result_count_for_graph(TICKER) == 1

def test_nflx_ticker_search_graph_subtitle(browser):
  home_page = SentradeHomePage(browser)
  result_page = SentradeResultPage(browser)
  TICKER = "NFLX"

  # Given the Sentrade home page is displayed
  home_page.load()

  # When the user searches for TICKER
  home_page.search(TICKER)
  
  # Assert the graph subtitle pertain to TICKER
  companies = {
            "AMZN" : "Amazon.com Inc.",
            "AAPL"  : "Apple Inc.", 
            "FB"    : "Facebook Inc.",
            "GOOG"  : "Alphabet Inc.",
            "MSFT"  : "Microsoft Corporation",
            "NFLX"  : "Netflix Inc.",
            "TSLA"  : "Tesla Inc.",
            "UBER"  : "Uber Technologies Inc."
        }

  assert result_page.result_count_for_graph(companies[TICKER]) == 1

def test_nflx_ticker_search_news_count(browser):
  home_page = SentradeHomePage(browser)
  result_page = SentradeResultPage(browser)
  TICKER = "NFLX"

  # Given the Sentrade home page is displayed
  home_page.load()

  # When the user searches for TICKER
  home_page.search(TICKER)
  
  # Assert there are 10 headlines
  assert result_page.result_count_for_news() == 10


def test_nflx_ticker_search_news_pertinence(browser):
  home_page = SentradeHomePage(browser)
  result_page = SentradeResultPage(browser)
  TICKER = "NFLX"

  # Given the Sentrade home page is displayed
  home_page.load()

  # When the user searches for TICKER
  home_page.search(TICKER)
  
  # Assert there are pertinent headlines
  companies = {
            "AMZN" : "Amazon",
            "AAPL"  : "Apple", 
            "FB"    : "Facebook",
            "GOOG"  : "Alphabet",
            "MSFT"  : "Microsoft",
            "NFLX"  : "Netflix",
            "TSLA"  : "Tesla",
            "UBER"  : "Uber"
        }

  assert result_page.result_contents_for_news(companies[TICKER])

def test_nflx_ticker_search_news_color(browser):
  home_page = SentradeHomePage(browser)
  result_page = SentradeResultPage(browser)
  TICKER = "NFLX"

  # Given the Sentrade home page is displayed
  home_page.load()

  # When the user searches for TICKER
  home_page.search(TICKER)
  assert result_page.colored_contents_for_news()

def test_nflx_ticker_search_tweets_count(browser):
  home_page = SentradeHomePage(browser)
  result_page = SentradeResultPage(browser)
  TICKER = "NFLX"

  # Given the Sentrade home page is displayed
  home_page.load()

  # When the user searches for TICKER
  home_page.search(TICKER)
  
  # Assert there are 10 tweets
  assert result_page.result_count_for_tweets() == 10


def test_nflx_ticker_search_tweets_pertinence(browser):
  home_page = SentradeHomePage(browser)
  result_page = SentradeResultPage(browser)
  TICKER = "NFLX"

  # Given the Sentrade home page is displayed
  home_page.load()

  # When the user searches for TICKER
  home_page.search(TICKER)
  
  # Assert there are pertinent tweets
  companies = {
            "AMZN" : "Amazon",
            "AAPL"  : "Apple", 
            "FB"    : "Facebook",
            "GOOG"  : "Alphabet",
            "MSFT"  : "Microsoft",
            "NFLX"  : "Netflix",
            "TSLA"  : "Tesla",
            "UBER"  : "Uber"
        }

  assert result_page.result_contents_for_tweets(companies[TICKER])

def test_nflx_ticker_search_tweets_color(browser):
    home_page = SentradeHomePage(browser)
    result_page = SentradeResultPage(browser)
    TICKER = "NFLX"

    # Given the Sentrade home page is displayed
    home_page.load()

    # When the user searches for TICKER
    home_page.search(TICKER)
    assert result_page.colored_contents_for_tweets()

def test_nflx_ticker_search_finance_data(browser):
    home_page = SentradeHomePage(browser)
    result_page = SentradeResultPage(browser)
    TICKER = "NFLX"

    # Given the Sentrade home page is displayed
    home_page.load()

    # When the user searches for TICKER
    home_page.search(TICKER)
    assert result_page.result_count_for_finance() == 1

def test_nflx_ticker_search_sentiment_data(browser):
    home_page = SentradeHomePage(browser)
    result_page = SentradeResultPage(browser)
    TICKER = "NFLX"

    # Given the Sentrade home page is displayed
    home_page.load()

    # When the user searches for TICKER
    home_page.search(TICKER)
    assert result_page.result_count_for_sentiment() == 1
###################
def test_tsla_ticker_search_graph_title(browser):
  home_page = SentradeHomePage(browser)
  result_page = SentradeResultPage(browser)
  TICKER = "TSLA"

  # Given the Sentrade home page is displayed
  home_page.load()

  # When the user searches for TICKER
  home_page.search(TICKER)
  
  # Assert that the graph title is TICKER
  assert result_page.result_count_for_graph(TICKER) == 1

def test_tsla_ticker_search_graph_subtitle(browser):
  home_page = SentradeHomePage(browser)
  result_page = SentradeResultPage(browser)
  TICKER = "TSLA"

  # Given the Sentrade home page is displayed
  home_page.load()

  # When the user searches for TICKER
  home_page.search(TICKER)
  
  # Assert the graph subtitle pertain to TICKER
  companies = {
            "AMZN" : "Amazon.com Inc.",
            "AAPL"  : "Apple Inc.", 
            "FB"    : "Facebook Inc.",
            "GOOG"  : "Alphabet Inc.",
            "MSFT"  : "Microsoft Corporation",
            "NFLX"  : "Netflix Inc.",
            "TSLA"  : "Tesla Inc.",
            "UBER"  : "Uber Technologies Inc."
        }

  assert result_page.result_count_for_graph(companies[TICKER]) == 1

def test_tsla_ticker_search_news_count(browser):
  home_page = SentradeHomePage(browser)
  result_page = SentradeResultPage(browser)
  TICKER = "TSLA"

  # Given the Sentrade home page is displayed
  home_page.load()

  # When the user searches for TICKER
  home_page.search(TICKER)
  
  # Assert there are 10 headlines
  assert result_page.result_count_for_news() == 10


def test_tsla_ticker_search_news_pertinence(browser):
  home_page = SentradeHomePage(browser)
  result_page = SentradeResultPage(browser)
  TICKER = "TSLA"

  # Given the Sentrade home page is displayed
  home_page.load()

  # When the user searches for TICKER
  home_page.search(TICKER)
  
  # Assert there are pertinent headlines
  companies = {
            "AMZN" : "Amazon",
            "AAPL"  : "Apple", 
            "FB"    : "Facebook",
            "GOOG"  : "Alphabet",
            "MSFT"  : "Microsoft",
            "NFLX"  : "Netflix",
            "TSLA"  : "Tesla",
            "UBER"  : "Uber"
        }

  assert result_page.result_contents_for_news(companies[TICKER])

def test_tsla_ticker_search_news_color(browser):
  home_page = SentradeHomePage(browser)
  result_page = SentradeResultPage(browser)
  TICKER = "TSLA"

  # Given the Sentrade home page is displayed
  home_page.load()

  # When the user searches for TICKER
  home_page.search(TICKER)
  assert result_page.colored_contents_for_news()

def test_tsla_ticker_search_tweets_count(browser):
  home_page = SentradeHomePage(browser)
  result_page = SentradeResultPage(browser)
  TICKER = "TSLA"

  # Given the Sentrade home page is displayed
  home_page.load()

  # When the user searches for TICKER
  home_page.search(TICKER)
  
  # Assert there are 10 tweets
  assert result_page.result_count_for_tweets() == 10


def test_tsla_ticker_search_tweets_pertinence(browser):
  home_page = SentradeHomePage(browser)
  result_page = SentradeResultPage(browser)
  TICKER = "TSLA"

  # Given the Sentrade home page is displayed
  home_page.load()

  # When the user searches for TICKER
  home_page.search(TICKER)
  
  # Assert there are pertinent tweets
  companies = {
            "AMZN" : "Amazon",
            "AAPL"  : "Apple", 
            "FB"    : "Facebook",
            "GOOG"  : "Alphabet",
            "MSFT"  : "Microsoft",
            "NFLX"  : "Netflix",
            "TSLA"  : "Tesla",
            "UBER"  : "Uber"
        }

  assert result_page.result_contents_for_tweets(companies[TICKER])

def test_tsla_ticker_search_tweets_color(browser):
    home_page = SentradeHomePage(browser)
    result_page = SentradeResultPage(browser)
    TICKER = "TLSA"

    # Given the Sentrade home page is displayed
    home_page.load()

    # When the user searches for TICKER
    home_page.search(TICKER)
    assert result_page.colored_contents_for_tweets()

def test_tsla_ticker_search_finance_data(browser):
    home_page = SentradeHomePage(browser)
    result_page = SentradeResultPage(browser)
    TICKER = "TSLA"

    # Given the Sentrade home page is displayed
    home_page.load()

    # When the user searches for TICKER
    home_page.search(TICKER)
    assert result_page.result_count_for_finance() == 1

def test_tsla_ticker_search_sentiment_data(browser):
    home_page = SentradeHomePage(browser)
    result_page = SentradeResultPage(browser)
    TICKER = "TSLA"

    # Given the Sentrade home page is displayed
    home_page.load()

    # When the user searches for TICKER
    home_page.search(TICKER)
    assert result_page.result_count_for_sentiment() == 1
###################
def test_uber_ticker_search_graph_title(browser):
  home_page = SentradeHomePage(browser)
  result_page = SentradeResultPage(browser)
  TICKER = "UBER"

  # Given the Sentrade home page is displayed
  home_page.load()

  # When the user searches for TICKER
  home_page.search(TICKER)
  
  # Assert that the graph title is TICKER
  assert result_page.result_count_for_graph(TICKER) == 1

def test_uber_ticker_search_graph_subtitle(browser):
  home_page = SentradeHomePage(browser)
  result_page = SentradeResultPage(browser)
  TICKER = "UBER"

  # Given the Sentrade home page is displayed
  home_page.load()

  # When the user searches for TICKER
  home_page.search(TICKER)
  
  # Assert the graph subtitle pertain to TICKER
  companies = {
            "AMZN" : "Amazon.com Inc.",
            "AAPL"  : "Apple Inc.", 
            "FB"    : "Facebook Inc.",
            "GOOG"  : "Alphabet Inc.",
            "MSFT"  : "Microsoft Corporation",
            "NFLX"  : "Netflix Inc.",
            "TSLA"  : "Tesla Inc.",
            "UBER"  : "Uber Technologies Inc."
        }

  assert result_page.result_count_for_graph(companies[TICKER]) == 1

def test_uber_ticker_search_news_count(browser):
  home_page = SentradeHomePage(browser)
  result_page = SentradeResultPage(browser)
  TICKER = "UBER"

  # Given the Sentrade home page is displayed
  home_page.load()

  # When the user searches for TICKER
  home_page.search(TICKER)
  
  # Assert there are 10 headlines
  assert result_page.result_count_for_news() == 10


def test_uber_ticker_search_news_pertinence(browser):
  home_page = SentradeHomePage(browser)
  result_page = SentradeResultPage(browser)
  TICKER = "UBER"

  # Given the Sentrade home page is displayed
  home_page.load()

  # When the user searches for TICKER
  home_page.search(TICKER)
  
  # Assert there are pertinent headlines
  companies = {
            "AMZN" : "Amazon",
            "AAPL"  : "Apple", 
            "FB"    : "Facebook",
            "GOOG"  : "Alphabet",
            "MSFT"  : "Microsoft",
            "NFLX"  : "Netflix",
            "TSLA"  : "Tesla",
            "UBER"  : "Uber"
        }

  assert result_page.result_contents_for_news(companies[TICKER])

def test_uber_ticker_search_news_color(browser):
  home_page = SentradeHomePage(browser)
  result_page = SentradeResultPage(browser)
  TICKER = "UBER"

  # Given the Sentrade home page is displayed
  home_page.load()

  # When the user searches for TICKER
  home_page.search(TICKER)
  assert result_page.colored_contents_for_news()

def test_uber_ticker_search_tweets_count(browser):
  home_page = SentradeHomePage(browser)
  result_page = SentradeResultPage(browser)
  TICKER = "UBER"

  # Given the Sentrade home page is displayed
  home_page.load()

  # When the user searches for TICKER
  home_page.search(TICKER)
  
  # Assert there are 10 tweets
  assert result_page.result_count_for_tweets() == 10


def test_uber_ticker_search_tweets_pertinence(browser):
  home_page = SentradeHomePage(browser)
  result_page = SentradeResultPage(browser)
  TICKER = "UBER"

  # Given the Sentrade home page is displayed
  home_page.load()

  # When the user searches for TICKER
  home_page.search(TICKER)
  
  # Assert there are pertinent tweets
  companies = {
            "AMZN" : "Amazon",
            "AAPL"  : "Apple", 
            "FB"    : "Facebook",
            "GOOG"  : "Alphabet",
            "MSFT"  : "Microsoft",
            "NFLX"  : "Netflix",
            "TSLA"  : "Tesla",
            "UBER"  : "Uber"
        }

  assert result_page.result_contents_for_tweets(companies[TICKER])

def test_uber_ticker_search_tweets_color(browser):
    home_page = SentradeHomePage(browser)
    result_page = SentradeResultPage(browser)
    TICKER = "UBER"

    # Given the Sentrade home page is displayed
    home_page.load()

    # When the user searches for TICKER
    home_page.search(TICKER)
    assert result_page.colored_contents_for_tweets()

def test_uber_ticker_search_finance_data(browser):
    home_page = SentradeHomePage(browser)
    result_page = SentradeResultPage(browser)
    TICKER = "UBER"

    # Given the Sentrade home page is displayed
    home_page.load()

    # When the user searches for TICKER
    home_page.search(TICKER)
    assert result_page.result_count_for_finance() == 1

def test_uber_ticker_search_sentiment_data(browser):
    home_page = SentradeHomePage(browser)
    result_page = SentradeResultPage(browser)
    TICKER = "UBER"

    # Given the Sentrade home page is displayed
    home_page.load()

    # When the user searches for TICKER
    home_page.search(TICKER)
    assert result_page.result_count_for_sentiment() == 1
###################