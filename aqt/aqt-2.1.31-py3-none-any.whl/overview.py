# -*- coding: utf-8 -*-
# Copyright: Ankitects Pty Ltd and contributors
# License: GNU AGPL, version 3 or later; http://www.gnu.org/licenses/agpl.html

from __future__ import annotations

from dataclasses import dataclass

import aqt
from anki.lang import _
from aqt import gui_hooks
from aqt.sound import av_player
from aqt.toolbar import BottomBar
from aqt.utils import askUserDialog, openLink, shortcut, tooltip


class OverviewBottomBar:
    def __init__(self, overview: Overview):
        self.overview = overview


@dataclass
class OverviewContent:
    """Stores sections of HTML content that the overview will be
    populated with.

    Attributes:
        deck {str} -- Plain text deck name
        shareLink {str} -- HTML of the share link section
        desc {str} -- HTML of the deck description section
        table {str} -- HTML of the deck stats table section
    """

    deck: str
    shareLink: str
    desc: str
    table: str


class Overview:
    "Deck overview."

    def __init__(self, mw: aqt.AnkiQt) -> None:
        self.mw = mw
        self.web = mw.web
        self.bottom = BottomBar(mw, mw.bottomWeb)

    def show(self):
        av_player.stop_and_clear_queue()
        self.web.set_bridge_command(self._linkHandler, self)
        self.mw.setStateShortcuts(self._shortcutKeys())
        self.refresh()

    def refresh(self):
        self.mw.col.reset()
        self._renderPage()
        self._renderBottom()
        self.mw.web.setFocus()
        gui_hooks.overview_did_refresh(self)

    # Handlers
    ############################################################

    def _linkHandler(self, url):
        if url == "study":
            self.mw.col.startTimebox()
            self.mw.moveToState("review")
            if self.mw.state == "overview":
                tooltip(_("No cards are due yet."))
        elif url == "anki":
            print("anki menu")
        elif url == "opts":
            self.mw.onDeckConf()
        elif url == "cram":
            deck = self.mw.col.decks.current()
            self.mw.onCram("'deck:%s'" % deck["name"])
        elif url == "refresh":
            self.mw.col.sched.rebuildDyn()
            self.mw.reset()
        elif url == "empty":
            self.mw.col.sched.emptyDyn(self.mw.col.decks.selected())
            self.mw.reset()
        elif url == "decks":
            self.mw.moveToState("deckBrowser")
        elif url == "review":
            openLink(aqt.appShared + "info/%s?v=%s" % (self.sid, self.sidVer))
        elif url == "studymore":
            self.onStudyMore()
        elif url == "unbury":
            self.onUnbury()
        elif url.lower().startswith("http"):
            openLink(url)
        return False

    def _shortcutKeys(self):
        return [
            ("o", self.mw.onDeckConf),
            ("r", self.onRebuildKey),
            ("e", self.onEmptyKey),
            ("c", self.onCustomStudyKey),
            ("u", self.onUnbury),
        ]

    def _filteredDeck(self):
        return self.mw.col.decks.current()["dyn"]

    def onRebuildKey(self):
        if self._filteredDeck():
            self.mw.col.sched.rebuildDyn()
            self.mw.reset()

    def onEmptyKey(self):
        if self._filteredDeck():
            self.mw.col.sched.emptyDyn(self.mw.col.decks.selected())
            self.mw.reset()

    def onCustomStudyKey(self):
        if not self._filteredDeck():
            self.onStudyMore()

    def onUnbury(self):
        if self.mw.col.schedVer() == 1:
            self.mw.col.sched.unburyCardsForDeck()
            self.mw.reset()
            return

        sibs = self.mw.col.sched.haveBuriedSiblings()
        man = self.mw.col.sched.haveManuallyBuried()

        if sibs and man:
            opts = [
                _("Manually Buried Cards"),
                _("Buried Siblings"),
                _("All Buried Cards"),
                _("Cancel"),
            ]

            diag = askUserDialog(_("What would you like to unbury?"), opts)
            diag.setDefault(0)
            ret = diag.run()
            if ret == opts[0]:
                self.mw.col.sched.unburyCardsForDeck(type="manual")
            elif ret == opts[1]:
                self.mw.col.sched.unburyCardsForDeck(type="siblings")
            elif ret == opts[2]:
                self.mw.col.sched.unburyCardsForDeck(type="all")
        else:
            self.mw.col.sched.unburyCardsForDeck(type="all")

        self.mw.reset()

    # HTML
    ############################################################

    def _renderPage(self):
        but = self.mw.button
        deck = self.mw.col.decks.current()
        self.sid = deck.get("sharedFrom")
        if self.sid:
            self.sidVer = deck.get("ver", None)
            shareLink = '<a class=smallLink href="review">Reviews and Updates</a>'
        else:
            shareLink = ""
        content = OverviewContent(
            deck=deck["name"],
            shareLink=shareLink,
            desc=self._desc(deck),
            table=self._table(),
        )
        gui_hooks.overview_will_render_content(self, content)
        self.web.stdHtml(
            self._body % content.__dict__,
            css=["overview.css"],
            js=["jquery.js", "overview.js"],
            context=self,
        )

    def _desc(self, deck):
        if deck["dyn"]:
            desc = _(
                """\
This is a special deck for studying outside of the normal schedule."""
            )
            desc += " " + _(
                """\
Cards will be automatically returned to their original decks after you review \
them."""
            )
            desc += " " + _(
                """\
Deleting this deck from the deck list will return all remaining cards \
to their original deck."""
            )
        else:
            desc = deck.get("desc", "")
        if not desc:
            return "<p>"
        if deck["dyn"]:
            dyn = "dyn"
        else:
            dyn = ""
        return '<div class="descfont descmid description %s">%s</div>' % (dyn, desc)

    def _table(self):
        counts = list(self.mw.col.sched.counts())
        finished = not sum(counts)
        but = self.mw.button
        if finished:
            return '<div style="white-space: pre-wrap;">%s</div>' % (
                self.mw.col.sched.finishedMsg()
            )
        else:
            return """
<table width=400 cellpadding=5>
<tr><td align=center valign=top>
<table cellspacing=5>
<tr><td>%s:</td><td><b><span class=new-count>%s</span></b></td></tr>
<tr><td>%s:</td><td><b><span class=learn-count>%s</span></b></td></tr>
<tr><td>%s:</td><td><b><span class=review-count>%s</span></b></td></tr>
</table>
</td><td align=center>
%s</td></tr></table>""" % (
                _("New"),
                counts[0],
                _("Learning"),
                counts[1],
                _("To Review"),
                counts[2],
                but("study", _("Study Now"), id="study", extra=" autofocus"),
            )

    _body = """
<center>
<h3>%(deck)s</h3>
%(shareLink)s
%(desc)s
%(table)s
</center>
"""

    # Bottom area
    ######################################################################

    def _renderBottom(self):
        links = [
            ["O", "opts", _("Options")],
        ]
        if self.mw.col.decks.current()["dyn"]:
            links.append(["R", "refresh", _("Rebuild")])
            links.append(["E", "empty", _("Empty")])
        else:
            links.append(["C", "studymore", _("Custom Study")])
            # links.append(["F", "cram", _("Filter/Cram")])
        if self.mw.col.sched.haveBuried():
            links.append(["U", "unbury", _("Unbury")])
        buf = ""
        for b in links:
            if b[0]:
                b[0] = _("Shortcut key: %s") % shortcut(b[0])
            buf += """
<button title="%s" onclick='pycmd("%s")'>%s</button>""" % tuple(
                b
            )
        self.bottom.draw(
            buf=buf, link_handler=self._linkHandler, web_context=OverviewBottomBar(self)
        )

    # Studying more
    ######################################################################

    def onStudyMore(self):
        import aqt.customstudy

        aqt.customstudy.CustomStudy(self.mw)
