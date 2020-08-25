import requests
import bs4
import re


def get_details_format(company: str, app_name: str, lang: str):
    """
    Get API
    Parameters
    ----------
    company: Company Name
    app_name: APP Name
    lang: Lang

    Returns
    -------
    URL
    """
    return "http://www.solvusoft.com/%s/file-extensions/software/%s/%s/" % (lang, company, app_name)


def get_application_details(company: str, appname: str, lang: str = 'zh-cn'):
    """
    Get Application Details
    Parameters
    ----------
    company: company
    appname: app name
    lang: Lang

    Returns
    -------
    None: Can't Find
    (a,b,c)
    a:All Desc b: short desc c: extensions
    """
    url = get_details_format(company, appname, lang)
    plain_data = requests.get(url=url)
    if plain_data.status_code != 200 and plain_data.status_code != 304:
        return None
    else:
        plain_data = plain_data.text
    bs = bs4.BeautifulSoup(plain_data, "html.parser")
    exes = bs.select('table tbody tr')
    exes2 = []
    for i in exes:
        exes3 = []
        j = i.select('a')
        for k in j:

            bs2 = bs4.BeautifulSoup(str(k), 'html.parser').select('a')[0]
            bs2 = re.sub(r'<a href="[A-Za-z/-]+">', "", str(bs2)).replace('</a>', '')
            exes3.append(bs2)
        exes2.append(exes3)
    exes = exes2
    del exes2, exes3
    desc = bs.select('div.grey-box')[0].select('table')[0].select('td')[1:]
    descs = []
    temp = []
    for i in range(len(desc)):
        desc[i] = str(desc[i]).replace("<td>", "").replace("</td>","").replace('<strong>', '').replace('</strong>', '').replace('</a>', '')
        desc[i] = re.sub('<a href="[A-Za-z/-]+">', '', desc[i])
        if desc[i].startswith('<td'):
            continue
        descs.append(desc[i])
    short_desc = str(bs.select(".left-col p")[0]).replace('<p>', '').replace('</p>', '')
    return descs, short_desc, exes



