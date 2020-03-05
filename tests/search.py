"""
This module contains DuckDuckGoSearchPage,
the page object for the DuckDuckGo search page.
Warning: the SEARCH_INPUT locator had to be updated because the page changed!
"""

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains



class SentradeHomePage:

  # URL

  URL = 'http://127.0.0.1:8050/'

  # Locators

  SEARCH_INPUT = (By.ID, 'stock-ticker-input')

  # Initializer

  def __init__(self, browser):
    self.browser = browser

  # Interaction Methods

  def load(self):
    self.browser.get(self.URL)

  def search(self, phrase):
    #search_input = self.browser.find_element(*self.SEARCH_INPUT)
    #search_input.send_keys(Keys.TAB + phrase + Keys.RETURN)
    actions = ActionChains(self.browser)
    actions.send_keys(Keys.TAB + phrase + Keys.RETURN)
    actions.perform()