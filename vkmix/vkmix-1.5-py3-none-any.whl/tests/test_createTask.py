import responses
import requests
import urllib.parse
import json
import unittest
from vkmix import VkMix

class TestVkMixCreateTask(unittest.TestCase):
    success_data = json.loads(r"""
{"response":{"success": 1, "points": 50, "id": 30592809}}
""".strip())
    
    def response_callback(self, resp):
        resp.callback_processed = True
        return resp
        args = {}
        try:
            args = urllib.parse.parse_qs(urllib.parse.urlparse(resp.url)[4])
        except AttributeError: pass
        except KeyError: pass
        try: args.update(resp.data)
        except TypeError: pass
        
        self.assertIn("api_token", args)
        self.assertEqual(args["api_token"][0], "mykey")
        self.assertEqual(args["network"][0], "vk")
        self.assertEqual(args["section"][0], "likes")
        self.assertEqual(args["link"][0], "https://vk.com/wall-139740824_2687166")
        self.assertEqual(int(args["count"][0]), 10)
        self.assertEqual(int(args["hourly_limit"][0]), 5)
        self.assertEqual(int(args["amount"][0]), 5)
        return resp

    def test_createTask(self):
        with responses.RequestsMock(response_callback=self.response_callback) as m:
            m.add(responses.POST, "https://vkmix.com/api/2/createTask", json=self.success_data)
            vkm = VkMix(api_token="mykey")
            data = vkm.createTask(
                network = "vk",
                section = "likes",
                link = "https://vk.com/wall-139740824_2687166",
                count = 10,
                hourly_limit = 5,
                amount = 5
            )
            self.assertEqual(m.assert_call_count("https://vkmix.com/api/2/createTask", 1), True)
            self.assertIn("id", data)
            self.assertEqual(data["success"], 1)
            self.assertEqual(data["points"], 50)

if __name__ == "__main__":
    unittest.main()
    