
from abc import ABCMeta, abstractmethod
from typing import Dict, Tuple, Text, Any, List
import inject


class Extractor(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def get_store_urls(self) -> List[str]:
        pass

    @abstractmethod
    def get_store(self, store_url: str) -> Dict[Text, Any]:
        pass


class TabelogRecommender:
    def __init__(self) -> None:
        self.extractor = inject.instance(Extractor)

    def execute(self, ignore_urls) -> Tuple[Dict[Text, Any]]:
        # 分析対象となる店舗URLをすべて取得
        store_urls = self.extractor.get_store_urls()

        # 店舗URLをひとつずつ回しながら詳細情報を取得
        store_list: List[Dict[Text, Any]] = []
        for url in store_urls:
            if url in ignore_urls:
                continue
            store = self.extractor.get_store(url)
            store_list.append(store)

        return tuple(store_list)
