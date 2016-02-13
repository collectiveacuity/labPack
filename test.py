__author__ = 'rcj1492'
__created__ = '2016.02'

from selenium import webdriver

browser = webdriver.Firefox()
browser.get('http://seleniumhq.org/')
print(browser.title)