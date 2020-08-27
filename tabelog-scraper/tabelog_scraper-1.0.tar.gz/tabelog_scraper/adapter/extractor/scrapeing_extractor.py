import requests
import time
from typing import List, Dict, Any, Text
from tabelog_scraper.adapter.extractor.scraped_page import ScrapedDetailPage, ScrapedListPage


class ScrapingExtractor(object):
    def __init__(self, target_url, limit_page_count) -> None:
        self.target_url = target_url
        self.limit_page_count = limit_page_count
        self.page_count = 1

    def get_store_urls(self) -> List[str]:
        store_urls: List[str] = []
        while self._can_search():
            self.page_count = self.page_count + 1

            _wait_a_second()
            response: requests.Response = requests.get(self.target_url)
            scraped_list_page = ScrapedListPage(response.text)
            self.target_url = scraped_list_page.get_next_target_url()
            store_urls.extend(scraped_list_page.get_detail_urls())

        return store_urls

    def get_store(self, store_url) -> Dict[Text, Any]:
        response: requests.Response = requests.get(store_url)
        scraped_detail_page = ScrapedDetailPage(response.text, response.url)
        return scraped_detail_page.get_store()

    def _can_search(self) -> bool:
        if len(self.target_url) == 0:
            return False
        if self.page_count > self.limit_page_count:
            return False
        return True


def _wait_a_second() -> None:
    time.sleep(1)
