import requests
import bs4
import re


def get_details_format(s: str, lang: str = 'zh-cn'):
    """
    Get API Request
    Parameters
    ----------
    s: Extensions Name
    lang: Lang

    Returns
    -------
    URL
    """
    return "http://www.solvusoft.com/%s/file-extensions/file-extension-%s/" % (lang, s)


def get_extension_details(extension: str, lang: str = 'en'):
    """
    Get Extension Details
    Parameters
    ----------
    extension: Extension Name
    lang: Lang

    Returns
    -------
    None: Can't Find
    Or (a, b, c)
    a:Description b: English Description c:Applications List(Double Level, [Company,APP])

    Examples
    ---------

    >>> print(get_extension_details('html', 'en'))


    """
    url = get_details_format(extension, lang)
    plain_data = requests.get(url=url)
    if plain_data.status_code != 200 and plain_data.status_code != 304:
        return None
    else:
        plain_data = plain_data.text

    bs = bs4.BeautifulSoup(plain_data, "html.parser")
    desc = bs.find_all('div', class_='photo-background-left')[0]
    desc_bs = bs4.BeautifulSoup(str(desc), 'html.parser')
    desc_ans_list = desc_bs.div.find_all('p')
    desc_ans = ''
    for i in desc_ans_list:
        desc_ans += (str(i)[3:-4]).replace('<strong>', '').replace('</strong>', '')
    desc_ans = desc_ans.replace('  ', '').replace('\n\n', '')[1:]
    del desc, desc_bs, desc_ans_list
    file_type = bs.select('div.accordian div.padding table tr td[valign=top]')[3]

    file_type = str(file_type).replace('<strong>', '').replace('</strong>', '').replace('<td valign="top">',
                                                                                        '').replace('</td>', '')

    a = bs.select('div.accordian div.grey-box p')[1:-3]

    a2 = []
    for i in a:
        w = i.select('a')
        w2 = []
        for j in w:
            w2.append(re.sub(r'<a href="[A-Za-z/-]+">', "", str(j)).replace('</a>', ''))
        if not w2:
            continue
        a2.append(w2)

    run_programs = a2
    del a, a2
    return desc_ans, file_type, run_programs


if __name__ == '__main__':
    print(repr(get_extension_details('html', 'qwety')))