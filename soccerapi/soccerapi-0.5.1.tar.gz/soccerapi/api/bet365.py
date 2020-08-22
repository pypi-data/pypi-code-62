from datetime import datetime
from typing import Dict, List, Tuple

import requests

from .base import ApiBase, NoOddsError


class ApiBet365(ApiBase):
    """ The ApiBase implementation of bet365.com """

    def __init__(self):
        self.name = 'bet365'
        self.competitions = self._load_competitions()
        self.parsers = [
            self._full_time_result,
            self._both_teams_to_score,
            self._double_chance,
        ]

    @staticmethod
    def _xor(msg: str, key: int) -> str:
        """ Applying xor algo to a message in order to make it readable """

        value = ''
        for char in msg:
            value += chr(ord(char) ^ key)
        return value

    def _guess_xor_key(self, encoded_msg: str) -> int:
        """ Try different key (int) until the msg is human readable """

        for key in range(130):
            msg = self._xor(encoded_msg, key)
            try:
                n, d = msg.split('/')
                if n.isdigit() and d.isdigit():
                    return key
            except ValueError:
                pass
        raise ValueError('Key not found !')

    @staticmethod
    def _get_values(data: str, value: str) -> List:
        """ Get value from data str XX=... return ...) """

        values = []
        for row in data.split('|'):
            if row.startswith('PA'):
                for data in row.split(';'):
                    if data.startswith(value):
                        values.append(data[3:])
        return values

    def _parse_datetimes(self, data: str) -> List:
        """ Parse datetimes in human readable ftm """

        datetimes = []
        values = self._get_values(data, 'BC')
        for dt in values:
            datetimes.append(datetime.strptime(dt, '%Y%m%d%H%M%S'))
        return datetimes

    def _parse_teams(self, data: str) -> List:
        """ Parse teams names from data str """

        home_teams, away_teams = [], []
        values = self._get_values(data, 'FD')
        for teams in values:
            if ' v ' in teams:
                home_team, away_team = teams.split(' v ')
                home_teams.append(home_team)
                away_teams.append(away_team)
        return home_teams, away_teams

    def _parse_odds(self, data: str) -> List:
        """ Get odds from data str, xoring and convert to decimal """

        odds = []
        values = self._get_values(data, 'OD')
        if len(values) == 0:
            raise NoOddsError
        key = self._guess_xor_key(values[0])
        for obfuscated_odd in values:
            # Event exists but no odds are available
            if obfuscated_odd == '':
                odd = None
            else:
                n, d = self._xor(obfuscated_odd, key).split('/')
                # TODO Watch out, the conversion between frac and dec
                # is not perfect due to rounding
                odd = round((int(n) / int(d) + 1) * 1000)
            odds.append(odd)
        return odds

    def _parse_events(self, data: str) -> List:
        """ Parse datetime, home_team, away_team and return list of events """

        events = []
        datetimes = self._parse_datetimes(data)
        home_teams, away_teams = self._parse_teams(data)

        for dt, home_team, away_team in zip(datetimes, home_teams, away_teams):
            events.append(
                {'time': dt, 'home_team': home_team, 'away_team': away_team}
            )

        return events

    def _full_time_result(self, data: str) -> List:
        """ Parse the raw data for full_time_result [13]"""

        odds = []
        events = self._parse_events(data)
        full_time_result = self._parse_odds(data)
        _1s = full_time_result[0::3]
        _Xs = full_time_result[1::3]
        _2s = full_time_result[2::3]

        for event, _1, _X, _2 in zip(events, _1s, _Xs, _2s):
            odds.append(
                {**event, 'full_time_result': {'1': _1, 'X': _X, '2': _2}}
            )
        return odds

    def _both_teams_to_score(self, data: str) -> List:
        """ Parse the raw data for both_teams_to_score [170]"""

        odds = []
        events = self._parse_events(data)
        full_time_result = self._parse_odds(data)
        yess = full_time_result[0::2]
        nos = full_time_result[1::2]

        for event, yes, no in zip(events, yess, nos):
            odds.append(
                {**event, 'both_teams_to_score': {'yes': yes, 'no': no}}
            )

        return odds

    def _double_chance(self, data: str) -> List:
        """ Parse the raw data for double_chance [195]"""

        odds = []
        events = self._parse_events(data)
        full_time_result = self._parse_odds(data)
        _1Xs = full_time_result[0::3]
        _2Xs = full_time_result[1::3]
        _12s = full_time_result[2::3]

        for event, _1X, _2X, _12 in zip(events, _1Xs, _2Xs, _12s):
            odds.append(
                {**event, 'double_chance': {'1X': _1X, '12': _12, '2X': _2X}}
            )

        return odds

    def _request(
        self, s: requests.Session, competition: str, category: int
    ) -> str:
        """ Make the single request using the active session """

        url = 'https://www.bet365.it/SportsBook.API/web'
        params = (
            ('lid', '1'),
            ('zid', '0'),
            ('pd', f'#AC#B1#C1#D{category}#{competition}#F2#'),
            ('cid', '97'),
            ('ctid', '97'),
        )
        return s.get(url, params=params).text

    def _requests(self, competition: str, **kwargs) -> Tuple[Dict]:
        """ Build URL starting from league (an unique id) and requests data for
            - full_time_result
            - both_teams_to_score
            - double_chance
        """

        config_url = 'https://www.bet365.it/defaultapi/sports-configuration'
        cookies = {'aps03': 'ct=97&lng=6'}
        headers = {
            'Connection': 'keep-alive',
            'Origin': 'https://www.bet365.it',
            'DNT': '1',
            'Accept': '*/*',
            'Sec-Fetch-Site': 'same-origin',
            'Sec-Fetch-Mode': 'cors',
            'Referer': 'https://www.bet365.it/',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'en-US,en;q=0.9,it;q=0.8,la;q=0.7',
            'User-Agent': (
                'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_2) '
                'AppleWebKit/537.36 (KHTML, like Gecko) '
                'Chrome/79.0.3945.117 Safari/537.36'
            ),
        }
        s = requests.Session()
        s.headers.update(headers)
        s.get(config_url, cookies=cookies)

        return (
            # full_time_result
            self._request(s, competition, 13),
            # both_teams_to_score
            self._request(s, competition, 170),
            # double_chance
            self._request(s, competition, 195),
            # under_over
            # self._request(s, competition, 56),
        )
