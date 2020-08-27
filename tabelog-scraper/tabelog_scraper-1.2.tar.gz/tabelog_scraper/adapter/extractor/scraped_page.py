from bs4 import BeautifulSoup
from typing import Dict, Text, Any, List


class ScrapedPage:
    def __init__(self, html: str):
        self.html: str = html

    def create_soup(self):
        # UTF-8にエンコードしないといけない
        return BeautifulSoup(self.html, 'html.parser')


class ScrapedListPage(ScrapedPage):
    def __init__(self, html: str):
        super().__init__(html)

    def get_detail_urls(self) -> List[str]:
        soup = self.create_soup()

        urls = []
        for a in soup.select('div.list-rst'):
            url = a.get('data-detail-url')
            urls.append(url)

        return urls

    def get_next_target_url(self):
        try:
            soup = self.create_soup()
            return soup.find(
                'a', class_='c-pagination__arrow--next').attrs['href']
        except AttributeError:
            return ''


class ScrapedDetailPage(ScrapedPage):
    def __init__(self, html: str, url: str):
        super().__init__(html)
        self.url: str = url

    def get_store(self) -> Dict[Text, Any]:
        soup = self.create_soup()

        result: Dict[Text, Any] = {}
        # 店名
        result["name"] = soup.select('.display-name > span')[0].text.strip()

        # 地理情報
        result["navigation"] = self.get_navigation()

        # レーティング
        result["rate"] = _convert_to_rate(
            soup.select('.rdheader-rating__score-val-dtl')[0].text)

        # 住所
        result["address"] = soup.select(
            '.rstinfo-table__address')[0].text.strip()

        # マップ画像
        result["address_image_url"] = soup.select(
            '.js-map-lazyload')[0].attrs['data-original']

        # URL
        result["url"] = self.url

        return result

    def get_navigation(self) -> str:
        soup = self.create_soup()
        breadcrumbs = soup.select('#location-breadcrumbs-wrap span')
        # 「ホーム > 食べログ」と、最後の店名は要らない
        # もしこの３つしかパンくずリストになかったら、空の文字列を返す
        if len(breadcrumbs) <= 3:
            return ''
        # 上記の不要な箇所を除外してから、テキストを抽出してカンマでつなぐ
        breadcrumbs = breadcrumbs[2: len(breadcrumbs)]
        breadcrumbs = breadcrumbs[0:-1]
        return ",".join(list(map(lambda b: b.text, breadcrumbs)))


def _convert_to_rate(rate_value: str) -> float:
    try:
        return float(rate_value)
    except ValueError:
        return 0.0


if __name__ == '__main__':
    import requests
    response = requests.get(
        'https://tabelog.com/tokyo/A1315/A131501/13194580/')
    detail_page = ScrapedDetailPage(response.text, response.url)
    print(detail_page.get_navigation())
