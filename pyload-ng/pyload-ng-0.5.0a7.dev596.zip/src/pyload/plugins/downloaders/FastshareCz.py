# -*- coding: utf-8 -*-

import re
import urllib.parse
from datetime import timedelta

from ..base.simple_downloader import SimpleDownloader


class FastshareCz(SimpleDownloader):
    __name__ = "FastshareCz"
    __type__ = "downloader"
    __version__ = "0.44"
    __status__ = "testing"

    __pattern__ = r"https?://(?:www\.)?fastshare\.cz/\d+/.+"
    __config__ = [
        ("enabled", "bool", "Activated", True),
        ("use_premium", "bool", "Use premium account if available", True),
        ("fallback", "bool", "Fallback to free download if premium fails", True),
        ("chk_filesize", "bool", "Check file size", True),
        ("max_wait", "int", "Reconnect if waiting time is greater than minutes", 10),
    ]

    __description__ = """FastShare.cz downloader plugin"""
    __license__ = "GPLv3"
    __authors__ = [
        ("Walter Purcaro", "vuolter@gmail.com"),
        ("GammaC0de", "nitzo2001[AT]yahoo[DOT]com"),
        ("ondrej", "git@ondrej.it"),
    ]

    URL_REPLACEMENTS = [("#.*", "")]

    COOKIES = [("fastshare.cz", "lang", "en")]

    NAME_PATTERN = r'<h2 title="(.+?)" class="section_title'
    SIZE_PATTERN = r'<i class="fa fa-bars"></i> (?P<S>\d+)&nbsp;(?P<U>[\w^_]+)'
    TEMP_OFFLINE_PATTERN = r"[^\w](503\s|[Mm]aint(e|ai)nance|[Tt]emp([.-]|orarily))"
    OFFLINE_PATTERN = r">(The file has been deleted|Requested page not found|This file is no longer available)"

    LINK_FREE_PATTERN = r'href="(.+?)" id=free-trigger>'
    LINK_PREMIUM_PATTERN = r"(https?://\w+\.fastshare\.cz/download\.php\?id=\d+&)"

    SLOT_ERROR = "> 100% of FREE slots are full"
    CREDIT_ERROR = " credit for "

    def check_errors(self):
        if self.SLOT_ERROR in self.data:
            errmsg = self.info["error"] = self._("No free slots")
            self.retry(12, 60, errmsg)

        if self.CREDIT_ERROR in self.data:
            errmsg = self.info["error"] = self._("Not enough traffic left")
            self.log_warning(errmsg)
            self.restart(premium=False)

        self.info.pop("error", None)

    def handle_free(self, pyfile):
        m = re.search(self.LINK_FREE_PATTERN, self.data)
        if m is None:
            self.error(self._("LINK_FREE_PATTERN not found"))

        self.link = urllib.parse.urljoin("https://fastshare.cz", m.group(1))
        baseurl = "https://fastshare.cz"

    def check_download(self):
        check = self.scan_download(
            {
                "paralell-dl": re.compile(
                    r"<title>FastShare.cz</title>|<script>alert\('Pres FREE muzete stahovat jen jeden soubor najednou.'\)"
                ),
                "wrong captcha": re.compile(r"Download for FREE"),
                "credit": re.compile(self.CREDIT_ERROR),
            }
        )

        if check == "paralell-dl":
            self.retry(6, timedelta(minutes=10).seconds, self._("Paralell download"))

        elif check == "wrong captcha":
            self.retry_captcha()

        elif check == "credit":
            self.restart(premium=False)

        return SimpleDownloader.check_download(self)
