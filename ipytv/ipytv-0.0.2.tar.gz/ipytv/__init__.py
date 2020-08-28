from ipytv.db import add_channel, print_channels, total_channels, get_channels
from os.path import join, dirname
from json_database.utils import match_one, fuzzy_match


class IPTV:
    def __init__(self, lang="en", db_path=None):
        self.db_path = db_path or join(dirname(__file__), "res",
                                       "channels.jsondb")
        self.lang = lang

    def add_channel(self, channel):
        self.update_channel(channel)

    def update_channel(self, channel):
        add_channel(channel, self.db_path, self.lang)

    def print_channels(self):
        print_channels(self.db_path)

    @property
    def channels(self):
        return list(set(get_channels(self.db_path)))

    @property
    def channel_names(self):
        return list(set([ch.name for ch in self.channels]))

    @property
    def total_channels(self):
        return total_channels(self.db_path)

    def search(self, query, max_res=5,
               tag_whitelist=None, lang_whitelist=None):
        scores = []
        query = query.lower()
        words = query.split(" ")
        tag_whitelist = tag_whitelist or []
        tag_whitelist = [t.lower().strip() for t in tag_whitelist]
        lang_whitelist = lang_whitelist or []
        lang_whitelist = [t.lower().split("-")[0] for t in lang_whitelist]

        def common(l1, l2):
            return list(set(l1).intersection(l2))

        for ch in self.channels:
            # check allowed langs
            if lang_whitelist:
                i = common(lang_whitelist, [ch.lang.split("-")[0]])
                if not len(i):
                    continue

            # check allowed tags
            if tag_whitelist:
                i = common(tag_whitelist, ch.channel_data["tags"])
                if not len(i):
                    continue

            # fuzzy match name for base score
            score = fuzzy_match(query, ch.name)

            # partial match name
            if ch.name in query:
                score += 0.4
            if query in ch.name:
                score += 0.3

            # fuzzy match aliases
            name, _score = match_one(query, ch.channel_data["aliases"])

            score += _score

            # language of TV
            if ch.lang == self.lang:
                score += 0.5  # base lang bonus  (full code)
            elif ch.lang == self.lang.split("-")[0]:
                score += 0.4  # base lang bonus (short code)
            elif ch.lang.split("-")[0] == self.lang.split("-")[0]:
                score += 0.3  # base lang bonus (short code mismatch)
            else:
                score -= 0.5

            # count word overlap with channel tags
            word_intersection = common(words, ch.channel_data["tags"])
            pct = len(word_intersection) / len(words)
            score += pct

            # fuzzy match tags
            _, _score = match_one(query, ch.channel_data["tags"])
            score += _score * 0.5
            for t in ch.channel_data["tags"]:
                if t in query:
                    score += 0.15

            # match country
            if "country" in ch.channel_data:
                if ch.channel_data["country"] in query:
                    score += 0.2

            # fuzzy match region
            if "region" in ch.channel_data:
                _, _score = match_one(query, ch.channel_data["region"])
                score += _score * 0.5

            # re-scale score values
            score = score / 4

            # name match bonus
            # we really want to increase score in this case
            name = name.replace("_", " ")
            word_intersection = common(words, name.split())
            pct = len(word_intersection) / len(words)
            if pct > 0:
                score += 0.4 * pct

            scores.append((ch, min(1, score)))

        scores = sorted(scores, key=lambda k: k[1], reverse=True)
        return scores[:max_res]


