__author__ = 'rcj1492'
__created__ = '2016.02'

'''
Selenium
https://seleniumhq.github.io/selenium/docs/api/py/index.html
pip3 install selenium
'''


from selenium import webdriver

browser = webdriver.Firefox()
browser.get('http://seleniumhq.org/')
print(browser.title)


