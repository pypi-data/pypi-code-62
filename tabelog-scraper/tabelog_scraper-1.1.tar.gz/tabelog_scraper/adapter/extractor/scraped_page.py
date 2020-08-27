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

        # レーティング
        result["rate"] = self.convert_to_rate(soup.select(
            '.rdheader-rating__score-val-dtl')[0].text)

        # 住所
        result["address"] = soup.select(
            '.rstinfo-table__address')[0].text.strip()

        # マップ画像
        result["address_image_url"] = soup.select(
            '.js-map-lazyload')[0].attrs['data-original']

        # URL
        result["url"] = self.url

        return result

    def convert_to_rate(self, rate_value: str) -> float:
        try:
            return float(rate_value)
        except ValueError:
            return 0.0
