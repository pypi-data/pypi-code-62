import responses
import requests
import urllib.parse
import json
import unittest
from vkmix import VkMix

class TestVkMixGetTasks(unittest.TestCase):
    success_data = json.loads(r"""
{"response":{"count":3,"items":[{"id":30587450,"done_count":6,"ordered_count":5,"amount":5,"title":"NameA LastNameA","status":"success","source":"api","network":"vk","section":"friends","url":"https:\/\/vk.com\/id1"},{"id":30307135,"done_count":5,"ordered_count":5,"amount":5,"title":"NameA LastNameA","status":"success","source":"api","network":"vk","section":"friends","url":"https:\/\/vk.com\/id1"},{"id":30307090,"done_count":5,"ordered_count":5,"amount":5,"title":"NameB LastNameB","status":"success","source":"api","network":"vk","section":"friends","url":"https:\/\/vk.com\/id2"}]}}
""".strip())
    
    def response_callback(self, resp):
        resp.callback_processed = True
        args = {}
        try:
            args = urllib.parse.parse_qs(urllib.parse.urlparse(resp.url)[4])
        except AttributeError: pass
        except KeyError: pass
        self.assertIn("api_token", args)
        self.assertEqual(args["api_token"][0], "mykey")
        return resp

    def test_getTasks(self):
        with responses.RequestsMock(response_callback=self.response_callback) as m:
            m.add(responses.GET, "https://vkmix.com/api/2/getTasks", json=self.success_data)
            vkm = VkMix(api_token="mykey")
            data = vkm.getTasks()
            # self.assertEqual(m.assert_call_count("https://vkmix.com/api/2/getTasks", 1), True) # no support query string?
            self.assertIn("count", data)
            self.assertIn("items", data)

if __name__ == "__main__":
    unittest.main()
    