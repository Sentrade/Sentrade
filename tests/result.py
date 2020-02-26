"""
This module contains DuckDuckGoResultPage,
the page object for the DuckDuckGo search result page.
Warning: the SEARCH_INPUT locator had to be updated because the page changed!
"""

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys


class SentradeResultPage:
  
  # Locators

  SEARCH_INPUT = (By.ID, 'react-select-2--value-item')

  @classmethod
  def GRAPH_RESULTS(cls, ticker):
    xpath = f"//div[@id='graph']//*[contains(text(), '{ticker}')]"
    return (By.XPATH, xpath)

  @classmethod
  def NEWS_RESULTS(cls, company):
    xpath = f"//div[@id='news']//*[contains(text(), '{company}')]"
    return (By.XPATH, xpath)

  @classmethod
  def TWEETS_RESULTS(cls, company):
    xpath = f"//div[@id='tweets']//*[contains(text(), '{company}')]"
    return (By.XPATH, xpath)

  # Initializer

  def __init__(self, browser):
    self.browser = browser

  # Interaction Methods

  def result_count_for_graph(self, ticker):
    results = self.browser.find_elements(*self.GRAPH_RESULTS(ticker))
    return len(results)

  def result_count_for_finance(self):
    results = self.browser.find_elements_by_id('finance')
    return len(results)

  def result_count_for_sentiment(self):
    results = self.browser.find_elements_by_id('sentiment')
    return len(results)

  def result_count_for_news(self):
    results = self.browser.find_elements_by_id('news-row')
    return len(results)
  
  def result_contents_for_news(self, company):
    results = self.browser.find_elements(*self.NEWS_RESULTS(company))
    if len(results) == 0:
      company = lower(company)
      results = self.browser.find_elements(*self.NEWS_RESULTS(company))
    return len(results)

  def colored_contents_for_news(self):
    results = self.browser.find_elements_by_xpath('//table[@id="news"]/tbody/tr/td')
    for element in results:
      color = element.value_of_css_property('color')
      if (color != 'rgb(224, 210, 4)') and (color != 'red') and (color != 'green'):
        return False
    return True

  def click_buttons(self):
    buttons = self.browser.find_element_by_xpath('//*[@id="graph"]/div[2]/div[2]/div/div/svg[2]/g[3]/g[2]/g[1]')
    buttons.send_keys(Keys.RETURN)
    return True

  def result_count_for_tweets(self):
    results = self.browser.find_elements_by_id('tweet-row')
    return len(results)

  def result_contents_for_tweets(self, company):
    results = self.browser.find_elements(*self.TWEETS_RESULTS(company))
    if len(results) == 0:
      company = lower(company)
      results = self.browser.find_elements(*self.TWEETS_RESULTS(company))
    return len(results)
  
  def colored_contents_for_tweets(self):
    results = self.browser.find_elements_by_xpath('//table[@id="tweets"]/tbody/tr/td')
    for element in results:
      color = element.value_of_css_property('color')
      if (color != 'rgb(224, 210, 4)') and (color != 'red') and (color != 'green'):
        return False
    return True

  def title(self):
    return self.browser.title