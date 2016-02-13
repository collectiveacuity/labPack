__author__ = 'rcj1492'
__created__ = '2016.02'

'''
Selenium
https://seleniumhq.github.io/selenium/docs/api/py/index.html
pip3 install selenium

Splinter
https://pypi.python.org/pypi/splinter
pip3 install splinter

PhantomJS
http://phantomjs.org/download.html
Download, unpack, and start having fun in just 5 minutes.

Morph.io
https://morph.io/documentation
Schedules & runs scraping from GitHub repo
'''

from selenium import webdriver
from splinter import Browser
from urllib.request import urlopen, Request
from urllib.parse import urlencode

class labSelenium(object):

    def __init__(self):
        pass

    def unitTests(self):
        browser = webdriver.Firefox()
        browser.get('http://seleniumhq.org/')
        print(browser.title)
        browser.get('https://collectiveacuity.com/')
        print(browser.title)
        browser.quit()

class labSplinter(object):

    def __init__(self):
        pass

    def unitTests(self):

        with Browser("phantomjs") as browser:
            # Optional, but make sure large enough that responsive pages don't
            # hide elements on you...
            browser.driver.set_window_size(1280, 1024)

            # Open the page you want...
            browser.visit("https://morph.io")

            # submit the search form...
            browser.fill("q", "parliament")
            button = browser.find_by_css("button[type='submit']")
            button.click()

            # Scrape the data you like...
            links = browser.find_by_css(".search-results .list-group-item")
            for link in links:
                print(link['href'])

class labMorph(object):

    def __init__(self, api_credentials):
        self.cred = api_credentials

    def unitTests(self):
        # We're always asking for json because it's the easiest to deal with
        morph_api_url = "https://api.morph.io/planningalerts-scrapers/blue-mountains/data.json"

        # Keep this key secret!
        morph_api_key = self.cred['apiKey']

        query_args = {
          'key': morph_api_key,
          'query': "select * from 'swvariables' limit 10"
        }

        url_string = "%s?%s" % (morph_api_url, urlencode(query_args))
        print(url_string)
        get_request = Request(url=url_string)
        r = urlopen(get_request)

        print(r.read().decode())

