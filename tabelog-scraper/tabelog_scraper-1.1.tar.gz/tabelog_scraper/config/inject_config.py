import inject
from tabelog_scraper.adapter.tabelog_recommender import Extractor
from tabelog_scraper.adapter.extractor.scrapeing_extractor import ScrapingExtractor

__target_url = ''
__limit_page_count = 0


def init_injection(target_url: str, limit_page_count: int):
    global __target_url, __limit_page_count
    __target_url = target_url
    __limit_page_count = limit_page_count
    inject.configure(inject_config)


def inject_config(binder):
    scraping_extractor = ScrapingExtractor(__target_url, __limit_page_count)
    # インスタンスを直で指定する場合は bind を使う
    binder.bind(Extractor, scraping_extractor)
    # 継承先のクラスを指定する場合は bind_to_constructor を使う
