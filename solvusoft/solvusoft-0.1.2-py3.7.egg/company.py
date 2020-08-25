import requests
import bs4


def get_details_format(s: str, lang: str = 'zh-cn'):
    """
        Get API Request

        Parameters
        ----------
        s: Company Name
        lang: Lang

        Returns
        -------
        URL
        """
    return "http://www.solvusoft.com/%s/file-extensions/software/%s/" % (lang, s)


def get_company_details(s: str, lang: str = 'en'):
    """
        Get Company Details
        Parameters
        ----------
        extension: Company Name
        lang: Lang

        Returns
        -------
        None: Can't Find
        Or (a, b)
        a:Description b:Applications

        Examples
        --------
        >>> print(get_company_details('kingsoft'))
        >>> ('Kingsoft is a Chinese software company founded in 1989 by Pak Kwan Kau. Aside from developing the WPS, Kingsoft is also an Internet service provider, created a mobile internet subsidiary (Cheetah) and security software products.', ['Kingsoft Office', 'Kingsoft Presentation', 'Kingsoft Writer', 'WPS Office'])

        """
    url = get_details_format(s, lang)

    # url = "https://www.solvusoft.com/zh-cn/file-extensions/software/kingsoft/kingsoft-office/"
    plain_data = requests.get(url=url)
    if plain_data.status_code != 200 and plain_data.status_code != 304:
        return None
    else:
        plain_data = plain_data.text
    bs = bs4.BeautifulSoup(plain_data, "html.parser")
    desc = bs.select('body>div.container>div.main>div.main-padding>div.left-col>p')[0]
    desc = str(desc).replace('<p>', '').replace('</p>', '')
    applications2 = bs.select('table.table')[0].select('td')
    applications = []
    for i in applications2:
        w = i.select('a')
        if len(w) != 0:
            w = bs4.BeautifulSoup(str(i), 'html.parser').a.text
        if not w:
            continue
        applications.append(w)
    return desc, applications



