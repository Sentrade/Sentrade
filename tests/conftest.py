#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "Davide Locatelli"
__status__ = "Production"

import pytest 
import selenium.webdriver

@pytest.fixture
def browser():
    b = selenium.webdriver.Chrome('/Users/davidelocatelli/Downloads/chromedriver')
    b.implicitly_wait(10)
    yield b
    b.quit()