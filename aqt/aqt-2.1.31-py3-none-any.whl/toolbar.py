# Copyright: Ankitects Pty Ltd and contributors
# -*- coding: utf-8 -*-
# License: GNU AGPL, version 3 or later; http://www.gnu.org/licenses/agpl.html

from __future__ import annotations

from typing import Any, Dict, Optional

import aqt
from anki.lang import _
from anki.rsbackend import SyncStatus
from aqt import gui_hooks
from aqt.qt import *
from aqt.sync import get_sync_status
from aqt.webview import AnkiWebView


# wrapper class for set_bridge_command()
class TopToolbar:
    def __init__(self, toolbar: Toolbar) -> None:
        self.toolbar = toolbar


# wrapper class for set_bridge_command()
class BottomToolbar:
    def __init__(self, toolbar: Toolbar) -> None:
        self.toolbar = toolbar


class Toolbar:
    def __init__(self, mw: aqt.AnkiQt, web: AnkiWebView) -> None:
        self.mw = mw
        self.web = web
        self.link_handlers: Dict[str, Callable] = {
            "study": self._studyLinkHandler,
        }
        self.web.setFixedHeight(30)
        self.web.requiresCol = False

    def draw(
        self,
        buf: str = "",
        web_context: Optional[Any] = None,
        link_handler: Optional[Callable[[str], Any]] = None,
    ) -> None:
        web_context = web_context or TopToolbar(self)
        link_handler = link_handler or self._linkHandler
        self.web.set_bridge_command(link_handler, web_context)
        self.web.stdHtml(
            self._body % self._centerLinks(),
            css=["toolbar.css"],
            js=["webview.js", "jquery.js", "toolbar.js"],
            context=web_context,
        )
        self.web.adjustHeightToFit()

    def redraw(self) -> None:
        self.set_sync_active(self.mw.media_syncer.is_syncing())
        self.update_sync_status()
        gui_hooks.top_toolbar_did_redraw(self)

    # Available links
    ######################################################################

    def create_link(
        self,
        cmd: str,
        label: str,
        func: Callable,
        tip: Optional[str] = None,
        id: Optional[str] = None,
    ) -> str:
        """Generates HTML link element and registers link handler
        
        Arguments:
            cmd {str} -- Command name used for the JS → Python bridge
            label {str} -- Display label of the link
            func {Callable} -- Callable to be called on clicking the link
        
        Keyword Arguments:
            tip {Optional[str]} -- Optional tooltip text to show on hovering
                                   over the link (default: {None})
            id: {Optional[str]} -- Optional id attribute to supply the link with
                                   (default: {None})
        
        Returns:
            str -- HTML link element
        """

        self.link_handlers[cmd] = func

        title_attr = f'title="{tip}"' if tip else ""
        id_attr = f'id="{id}"' if id else ""

        return (
            f"""<a class=hitem tabindex="-1" aria-label="{label}" """
            f"""{title_attr} {id_attr} href=# onclick="return pycmd('{cmd}')">"""
            f"""{label}</a>"""
        )

    def _centerLinks(self) -> str:
        links = [
            self.create_link(
                "decks",
                _("Decks"),
                self._deckLinkHandler,
                tip=_("Shortcut key: %s") % "D",
                id="decks",
            ),
            self.create_link(
                "add",
                _("Add"),
                self._addLinkHandler,
                tip=_("Shortcut key: %s") % "A",
                id="add",
            ),
            self.create_link(
                "browse",
                _("Browse"),
                self._browseLinkHandler,
                tip=_("Shortcut key: %s") % "B",
                id="browse",
            ),
            self.create_link(
                "stats",
                _("Stats"),
                self._statsLinkHandler,
                tip=_("Shortcut key: %s") % "T",
                id="stats",
            ),
        ]

        links.append(self._create_sync_link())

        gui_hooks.top_toolbar_did_init_links(links, self)

        return "\n".join(links)

    # Sync
    ######################################################################

    def _create_sync_link(self) -> str:
        name = _("Sync")
        title = _("Shortcut key: %s") % "Y"
        label = "sync"
        self.link_handlers[label] = self._syncLinkHandler

        return f"""
<a class=hitem tabindex="-1" aria-label="{name}" title="{title}" id="{label}" href=# onclick="return pycmd('{label}')">{name}
<img id=sync-spinner src='/_anki/imgs/refresh.svg'>        
</a>"""

    def set_sync_active(self, active: bool) -> None:
        if active:
            meth = "addClass"
        else:
            meth = "removeClass"
        self.web.eval(f"$('#sync-spinner').{meth}('spin')")

    def set_sync_status(self, status: SyncStatus) -> None:
        self.web.eval(f"updateSyncColor({status.required})")

    def update_sync_status(self) -> None:
        get_sync_status(self.mw, self.mw.toolbar.set_sync_status)

    # Link handling
    ######################################################################

    def _linkHandler(self, link: str) -> bool:
        if link in self.link_handlers:
            self.link_handlers[link]()
        return False

    def _deckLinkHandler(self) -> None:
        self.mw.moveToState("deckBrowser")

    def _studyLinkHandler(self) -> None:
        # if overview already shown, switch to review
        if self.mw.state == "overview":
            self.mw.col.startTimebox()
            self.mw.moveToState("review")
        else:
            self.mw.onOverview()

    def _addLinkHandler(self) -> None:
        self.mw.onAddCard()

    def _browseLinkHandler(self) -> None:
        self.mw.onBrowse()

    def _statsLinkHandler(self) -> None:
        self.mw.onStats()

    def _syncLinkHandler(self) -> None:
        self.mw.on_sync_button_clicked()

    # HTML & CSS
    ######################################################################

    _body = """
<center id=outer>
<table id=header width=100%%>
<tr>
<td class=tdcenter align=center>%s</td>
</tr></table>
</center>
"""


# Bottom bar
######################################################################


class BottomBar(Toolbar):

    _centerBody = """
<center id=outer><table width=100%% id=header><tr><td align=center>
%s</td></tr></table></center>
"""

    def draw(
        self,
        buf: str = "",
        web_context: Optional[Any] = None,
        link_handler: Optional[Callable[[str], Any]] = None,
    ) -> None:
        # note: some screens may override this
        web_context = web_context or BottomToolbar(self)
        link_handler = link_handler or self._linkHandler
        self.web.set_bridge_command(link_handler, web_context)
        self.web.stdHtml(
            self._centerBody % buf,
            css=["toolbar.css", "toolbar-bottom.css"],
            context=web_context,
        )
        self.web.adjustHeightToFit()
