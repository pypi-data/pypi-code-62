import requests
from bs4 import BeautifulSoup

def soupify(url,method='get',post_data=None,json_data=None):
    """Create soup from a url request.

    :param url: URL
    :type url: str
    :param method: Method of Request
    :type method: str, optional
    :param post_data: Post data (if any)
    :type post_data: dict, optional
    :param json_data: Request header as json
    :returns: Soup of HTML file using URL and request data
    """
    try:
        if method=='get':
            try:
                html = requests.get(url,params=json_data).content
                return BeautifulSoup(html,features="lxml")
            except:
                pass
        elif method=='post':
            try:
                html = requests.post(url,data=post_data,json=json_data).content
                return BeautifulSoup(html,features="lxml")
            except:
                pass
        else:
            print("Only GET & POST requests are allowed")
    except Exception as e:
        print("Soupify error: "+str(e))
        return None