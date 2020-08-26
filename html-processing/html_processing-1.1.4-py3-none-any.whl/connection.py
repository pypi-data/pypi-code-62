from time import sleep

import dpp_common_utils.selenium
import requests
import re
from lxml import etree
from lxml.html import HtmlElement
from requests.exceptions import InvalidURL
from selenium.common.exceptions import WebDriverException

from html_processing.parser import get_html_parser


def lxml_connect(url, custom_element=None):
    """
    Connects to URL, retrieves the HTML via selenium and returns a lxml HTML Tree
    Args:
        url: The URL to the target data source
        custom_element: a subclass of lxml.html.HTMLElement

    Returns: an instance of the custom_element class
    """

    parser = get_html_parser() if custom_element is None else get_html_parser(custom_element)
    driver = dpp_common_utils.selenium.get_driver(True)
    __check_url(url)
    try:
        driver.get(url)
    except WebDriverException:
        raise requests.exceptions.ConnectionError

    sleep(3)  # sleep - the script has to be loaded and this needs time
    res = driver.page_source
    driver.quit()

    html_tree: HtmlElement = etree.fromstring(res, parser=parser)
    return html_tree


def lxml_fast_connect(url, custom_element=None):
    """
    Connects to URL, retrieves the HTML via requests and returns a lxml HTML Tree
    Args:
        url: The URL to the target data source
        custom_element: a subclass of lxml.html.HTMLElement

    Returns: an instance of the custom_element class
    """
    parser = get_html_parser() if custom_element is None else get_html_parser(custom_element)
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:53.0) Gecko/20100101 Firefox/53.0'
    headers = {'User-Agent': user_agent}
    res = requests.get(url, headers=headers)
    __check_url(url)
    html_tree: HtmlElement = etree.fromstring(res.content, parser=parser)
    return html_tree


def __check_url(url):
    """
    Checks if the URL has a valid format.
    Uses https://github.com/django/django/blob/stable/1.3.x/django/core/validators.py#L45
    See (https://stackoverflow.com/questions/7160737/python-how-to-validate-a-url-in-python-malformed-or-not)

    :param url: The URL to check
    :type url: str
    :throws: requests.exceptions
    """

    regex = re.compile(
        r'^(?:http|ftp)s?://'  # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'  # domain...
        r'localhost|'  # localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
        r'(?::\d+)?'  # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)

    if re.match(regex, url) is None:
        raise InvalidURL
