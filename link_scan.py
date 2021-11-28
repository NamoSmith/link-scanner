"""A link scanner program for finding all links on a web page and the invalid links."""

import sys
import urllib.error
import urllib.request
from typing import List

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service


WEBDRIVER_PATH = "C:/selenium/chromedriver.exe"


def get_links(url: str) -> List:
    """Find all links on page at the given url.
    Returns:
        a list of all unique hyperlinks on the page,
        without page fragments or query parameters.
    """

    url_list = []
    browser.get(url)
    elements = browser.find_elements(By.TAG_NAME, "a")

    for link in elements:
        url: str = link.get_attribute('href')
        if url is not None:
            if '#' in url:
                url = url.split('#')[0]
            elif '?' in url:
                url = url.split('?')[0]
            if url not in url_list:
                url_list.append(url)

    return url_list


def is_valid_url(url: str):
    """Return True if the URL is valid, and false if not valid."""

    try:
        urllib.request.urlopen(url)
    except urllib.error.HTTPError as er:
        if er.getcode() == 403:
            return True
        return False
    else:
        return True


def invalid_urls(url_list: List[str]) -> List[str]:
    """Validate the urls in url_list and return a new list containing
    the invalid or unreachable urls.
    """

    invalid_urls_list = []

    for url in url_list:
        if not is_valid_url(url):
            invalid_urls_list.append(url)
    return invalid_urls_list


if __name__ == '__main__':
    try:
        test_url = sys.argv[1]
    except IndexError:
        print('Usage:  python3 link_scan.py url')
        print('\nTest all hyperlinks on the given url.')
    else:
        my_service = Service(WEBDRIVER_PATH)
        my_options = webdriver.ChromeOptions()
        my_options.headless = True

        browser = webdriver.Chrome(service=my_service, options=my_options)

        # Show all urls.
        urls = get_links(test_url)
        for each_url in urls:
            print(each_url)

        # Show invalid urls.
        bad_urls = invalid_urls(urls)
        print('\nBad Links:')
        for bad_url in bad_urls:
            print(bad_url)
