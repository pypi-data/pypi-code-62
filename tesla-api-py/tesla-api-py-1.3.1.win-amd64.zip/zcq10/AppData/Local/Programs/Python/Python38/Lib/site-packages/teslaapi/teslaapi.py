import calendar
import json
import datetime
import logging
import requests


class Connect:
    def __init__(self, email, passwd, access_token=None):
        self.headers = {'User-Agent': 'app'}
        self.headers["Content-Type"] = "application/json"

        self.access_token = None
        self.expiration = 0
        self.baseurl = "https://owner-api.teslamotors.com"

        if access_token:
            self.__sethead(access_token)
        else:
            self.oauth = {
                "grant_type": "password",
                "client_id": "81527cff06843c8634fdc09e8ac0abefb46ac849f38fe1e431c2ef2106796384",
                "client_secret": "c7257eb71a564034f9419ee651c7d0e5f7aa6bfbd18bafb5c5c033b093bb2fa3",
                "email": email,
                "password": passwd
            }
            resp = self.post("/oauth/token", json.dumps(self.oauth))

            if resp.__contains__("access_token"):
                access_token = resp["access_token"]
                self.__sethead(access_token, resp["expires_in"])

        self.vehicles = [Vehicle(v, self)
                         for v in self.get('/api/1/vehicles')['response']]

    def post(self, command, data=None):
        now = calendar.timegm(datetime.datetime.now().timetuple())
        if now > self.expiration and command != '/oauth/token':
            auth = requests.post(
                f"{self.baseurl}/oauth/token", data=self.oauth).json()
            self.__sethead(auth['access_token'],
                           auth['created_at'] + auth['expires_in'] - 86400)
        url = self.baseurl+command
        resp = requests.post(url, headers=self.headers, data=data)
        j = resp.json()
        logging.debug(j)
        return j

    def get(self, command, params=None):
        url = self.baseurl+command
        resp = requests.get(url, headers=self.headers, params=params)
        j = resp.json()
        logging.debug(j)
        return j

    def __sethead(self, access_token, expiration=0):
        self.access_token = access_token
        self.expiration = expiration
        self.headers["Authorization"] = f"Bearer {access_token}"


class Vehicle(dict):
    def __init__(self, data, connect):
        super(Vehicle, self).__init__(data)
        self.connect = connect

    def vehicle_data(self):
        resp = self.get_("vehicle_data")
        return resp["response"]

    def data_request(self, state):
        """获取车辆数据

        Args:
            state ([type]): climate_state,charge_state,drive_state,gui_settings,
            vehicle_state,vehicle_config
        Returns:
            [type]: [description]
        """
        resp = self.get_("data_request/{}".format(state))
        return resp["response"]

    def nearby_charging_sites(self):
        """附近的充电桩

        Returns:
            [type]: [description]
        """
        resp = self.get_("nearby_charging_sites")
        return resp["response"]

    def wake_up(self):
        resp = self.post("wakeup")
        return resp["response"]

    def flash_lights(self):
        resp = self.post("command/flash_lights")
        return resp["response"]

    def honk_horn(self):
        resp = self.post("command/honk_horn")
        return resp["response"]

    def remote_start_drive(self):
        resp = self.post("command/remote_start_drive")
        return resp["response"]

    def speed_limit_set_limit(self, limit_mph):
        """设置最大限速
        """
        resp = self.post("command/speed_limit_set_limit",
                         {"limit_mph": limit_mph})
        return resp["response"]

    def speed_limit_activate(self, pin):
        """速度限制激活
        """
        resp = self.post("command/speed_limit_set_limit",
                         {"pin": pin})
        return resp["response"]

    def speed_limit_deactivate(self, pin):
        """速度限制解除
        """
        resp = self.post("command/speed_limit_deactivate", {"pin": pin})
        return resp["response"]

    def speed_limit_clear_pin(self, pin):
        """限速PIN删除
        """
        resp = self.post("command/speed_limit_clear_pin", {"pin": pin})
        return resp["response"]

    def set_valet_mode(self, on, password):
        """设置代客模式，70MPH and 80kW
        """
        resp = self.post("command/speed_limit_clear_pin",
                         {"on": on, "password": password})
        return resp["response"]

    def reset_valet_pin(self, pin):
        """关闭代客模式
        """
        resp = self.post("command/speed_limit_clear_pin", {"pin": pin})
        return resp["response"]

    def set_sentry_mode(self, on):
        """开启关闭情景模式
        """
        resp = self.post("command/set_sentry_mode", {"on": on})
        return resp["response"]

    def post(self, command, data=None):
        return self.connect.post("/api/1/vehicles/{}/{}".format(self["id"], command), data)

    def get_(self, command):
        return self.connect.get("/api/1/vehicles/{}/{}".format(self["id"], command))
