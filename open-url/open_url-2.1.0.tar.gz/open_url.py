import requests
from bs4 import BeautifulSoup


def openURL(url):
    headers = {
        "user-agent": "Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/64.0.3282.167 Chrome/64.0.3282.167 Safari/537.36"}
    res = requests.get(url, headers=headers)

    return res


def toTXT(res):
    res.encoding = "utf-8"
    soup = BeautifulSoup(res.text, "html.parser")

    with open("index.txt", "w") as f:
        f.write(soup.prettify())
