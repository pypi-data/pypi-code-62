from scrapy.exceptions import DropItem
import requests
import os
import json

class FlowPipeline(object):

    def process_item(self, item, spider):
        unique_id = item.get('unique_id')
        if not unique_id:
            raise DropItem('unique_id is None')

        data = item.deepcopy().to_dict()

        crawled_at = data.get('crawled_at')
        if crawled_at:
            data['crawled_at'] = data['crawled_at'].isoformat()

        # convert datetime to str before serialize
        flow_urls = item.get('flow_urls', None)
        if not flow_urls:
            flow_urls = spider.settings.get('FLOW_URLS')
        if flow_urls:
            data_helper_url = spider.settings.get('DATA_HELPER_URL')
            if not data_helper_url:
                data_helper_url = os.environ.get('DATA_HELPER_URL')
            if not data_helper_url:
                spider.logger.error(f'data helper url not found, config url to settings')
                return item
            else:
                config_type = type(flow_urls)
                flows = []
                if config_type == str:
                    # 本地开发直接发送 flow
                    if flow_urls.startswith('http://127.0.0.1') or flow_urls.startswith('http://localhost') :
                        response = requests.post(flow_urls, json=data, timeout=10)
                        if int(response.status_code) == 200:
                            spider.logger.info(f'req addr: {flow_urls}  {unique_id} request success')
                        else:
                            spider.logger.info(f'req addr: {flow_urls} {unique_id} request fail, {response.status_code} {data}')
                        return item
                    flows.append(flow_urls)
                elif config_type == list:
                    flows = flow_urls
                else:
                    spider.logger.error(f'flow urls config type error, make sure the type must be an array or string')
                    return item
                response = requests.post(data_helper_url, json={
                    'flow_urls': flows,
                    'payload': json.dumps(data),
                }, timeout=5)
                if response.status_code == 200:
                    spider.logger.info(f'send data to helper success: {item.get("unique_id")} {data_helper_url} {flows}')
                else:
                    spider.logger.warn(f'send data to helper fail: {item.get("unique_id")} {data_helper_url} {flows} {response.status_code}')
                return item
        return item

