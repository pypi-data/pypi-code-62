import base64
import json
import re
from datetime import datetime, date
import time

from bs4 import BeautifulSoup, Tag

from .core import SkypeObj, SkypeEnum
from .util import SkypeUtils
from .conn import SkypeConnection


def makeTag(name, string=None, **kwargs):
    tag = Tag(name=name, attrs=kwargs)
    for key in kwargs:
        if kwargs[key] is None:
            kwargs[key] = ""
    if string:
        tag.string = string
    return tag


@SkypeUtils.initAttrs
@SkypeUtils.convertIds("user", "chat")
class SkypeMsg(SkypeObj):
    """
    A message either sent or received in a conversation.

    An edit is represented by a follow-up message with the same :attr:`clientId`, which replaces the earlier message.

    Attributes:
        id (str):
            Identifier of the message provided by the server, usually a timestamp.
        type (str):
            Raw message type, as specified by the Skype API.
        time (datetime.datetime):
            Original arrival time of the message.
        clientId (str):
            Identifier generated by the client, used as a reference for edits.
        user (:class:`.SkypeUser`):
            User that sent the message.
        chat (:class:`.SkypeChat`):
            Conversation where this message was received.
        content (str):
            Raw message content, as received from the API.
        html (str):
            Recreated content string based on the field values.
        deleted (bool):
            Whether the message content was deleted by the sender.
    """

    @staticmethod
    def bold(s):
        """
        Format text to be bold.

        Args:
            s (str): string to format

        Returns:
            str: formatted string
        """
        return """<b raw_pre="*" raw_post="*">{0}</b>""".format(s)

    @staticmethod
    def italic(s):
        """
        Format text to be italic.

        Args:
            s (str): string to format

        Returns:
            str: formatted string
        """
        return """<i raw_pre="_" raw_post="_">{0}</i>""".format(s)

    @staticmethod
    def strike(s):
        """
        Format text to be struck through.

        Args:
            s (str): string to format

        Returns:
            str: formatted string
        """
        return """<s raw_pre="~" raw_post="~">{0}</s>""".format(s)

    @staticmethod
    def mono(s):
        """
        Format text to be monospaced.

        Args:
            s (str): string to format

        Returns:
            str: formatted string
        """
        return """<pre raw_pre="{{code}}" raw_post="{{code}}">{0}</pre>""".format(s)

    @staticmethod
    def colour(s, colour):
        """
        Format text to be coloured.

        Args:
            s (str): string to format
            colour (str): colour to display text in

        Returns:
            str: formatted string
        """
        return """<font color="{0}">{1}</font>""".format(colour, s)

    @staticmethod
    def link(url, display=None):
        """
        Create a hyperlink.  If ``display`` is not specified, display the URL.

        .. note:: Anomalous API behaviour: official clients don't provide the ability to set display text.

        Args:
            url (str): full URL to link to
            display (str): custom label for the hyperlink

        Returns:
            str: tag to display a hyperlink
        """
        return """<a href="{0}">{1}</a>""".format(url, display or url)

    @staticmethod
    def emote(shortcut):
        """
        Display an emoticon.  This accepts any valid shortcut.

        Args:
            shortcut (str): emoticon shortcut

        Returns:
            str: tag to render the emoticon
        """
        for emote in SkypeUtils.static["items"]:
            if shortcut == emote["id"]:
                return """<ss type="{0}">{1}</ss>""".format(shortcut, emote["shortcuts"][0])
            elif shortcut in emote["shortcuts"]:
                return """<ss type="{0}">{1}</ss>""".format(emote["id"], shortcut)
        # No match, return the input as-is.
        return shortcut

    @staticmethod
    def mention(user):
        """
        Mention a user in a message.  This may trigger a notification for them even if the conversation is muted.

        Args:
            user (SkypeUser): user who is to be mentioned

        Returns:
            str: tag to display the mention
        """
        return """<at id="8:{0}">{1}</at>""".format(user.id, user.name)

    @staticmethod
    def quote(user, chat, timestamp, content):
        """
        Display a message excerpt as a quote from another user.

        Skype for Web doesn't support native quotes, and instead displays the legacy quote text.  Supported desktop
        clients show a blockquote with the author's name and timestamp underneath.

        .. note:: Anomalous API behaviour: it is possible to fake the message content of a quote.

        Args:
            user (SkypeUser): user who is to be quoted saying the message
            chat (SkypeChat): conversation the quote was originally seen in
            timestamp (datetime.datetime): original arrival time of the quoted message
            content (str): excerpt of the original message to be quoted

        Returns:
            str: tag to display the excerpt as a quote
        """
        # Single conversations lose their prefix here.
        chatId = chat.id if chat.id.split(":")[0] == "19" else SkypeUtils.noPrefix(chat.id)
        # Legacy timestamp includes the date if the quote is not from today.
        unixTime = int(time.mktime(timestamp.timetuple()))
        legacyTime = timestamp.strftime("{0}%H:%M:%S".format("" if timestamp.date() == date.today() else "%d/%m/%Y "))
        return """<quote author="{0}" authorname="{1}" conversation="{2}" timestamp="{3}"><legacyquote>""" \
               """[{4}] {1}: </legacyquote>{5}<legacyquote>\n\n&lt;&lt;&lt; </legacyquote></quote>""" \
               .format(user.id, user.name, chatId, unixTime, legacyTime, content)

    @staticmethod
    def uriObject(content, type, url, thumb=None, title=None, desc=None, **values):
        """
        Generate the markup needed for a URI component in a rich message.

        Args:
            content (str): object-specific content inside the object tag
            type (str): URI object type
            url (str): URL to content
            title (str): name of object
            desc (str): additional line of information
            thumb (str): URL to thumbnail of content
            values (dict): standard value tags of the form ``<key v="value"/>``

        Returns:
            str: ``<URIObject>`` tag
        """
        titleTag = """<Title>Title: {0}</Title>""".format(title) if title else """<Title/>"""
        descTag = """<Description>Description: {0}</Description>""".format(desc) if desc else """<Description/>"""
        thumbAttr = " url_thumbnail=\"{0}\"".format(thumb) if thumb else ""
        valTags = "".join("""<{0} v="{1}"/>""".format(k, v) for k, v in values.items())
        return """<URIObject type="{1}" uri="{2}"{3}>{4}{5}{6}{0}</URIObject>""" \
               .format(content, type, url, thumbAttr, titleTag, descTag, valTags)

    attrs = ("id", "type", "time", "clientId", "userId", "chatId", "content")

    @classmethod
    def rawToFields(cls, raw={}):
        try:
            msgTime = datetime.strptime(raw.get("originalarrivaltime", ""), "%Y-%m-%dT%H:%M:%S.%fZ")
        except ValueError:
            msgTime = datetime.now()
        return {"id": raw.get("id"),
                "type": raw.get("messagetype"),
                "time": msgTime,
                "clientId": raw.get("clientmessageid", raw.get("skypeeditedid")),
                "userId": SkypeUtils.userToId(raw.get("from", "")),
                "chatId": SkypeUtils.chatToId(raw.get("conversationLink", "")),
                "content": raw.get("content")}

    @classmethod
    def fromRaw(cls, skype=None, raw={}):
        msgCls = {"Text": SkypeTextMsg,
                  "RichText": SkypeTextMsg,
                  "RichText/Contacts": SkypeContactMsg,
                  "RichText/Location": SkypeLocationMsg,
                  "RichText/Media_GenericFile": SkypeFileMsg,
                  "RichText/UriObject": SkypeImageMsg,
                  "RichText/Media_Card": SkypeCardMsg,
                  "Event/Call": SkypeCallMsg,
                  "ThreadActivity/TopicUpdate": SkypeTopicPropertyMsg,
                  "ThreadActivity/JoiningEnabledUpdate": SkypeOpenPropertyMsg,
                  "ThreadActivity/HistoryDisclosedUpdate": SkypeHistoryPropertyMsg,
                  "ThreadActivity/AddMember": SkypeAddMemberMsg,
                  "ThreadActivity/RoleUpdate": SkypeChangeMemberMsg,
                  "ThreadActivity/DeleteMember": SkypeRemoveMemberMsg}.get(raw.get("messagetype"), cls)
        return msgCls(skype, raw, **msgCls.rawToFields(raw))

    @property
    def html(self):
        # If not overridden in a subclass, just return the existing content.
        return self.content

    @property
    def deleted(self):
        return self.content == ""

    def read(self):
        """
        Mark this message as read by sending an updated consumption horizon.
        """
        self.chat.setConsumption("{0};{1};{0}".format(self.clientId, int(time.time() * 1000)))

    def edit(self, content, me=False, rich=False):
        """
        Send an edit of this message.  Arguments are passed to :meth:`.SkypeChat.sendMsg`.

        .. note:: Anomalous API behaviour: messages can be undeleted by editing their content to be non-empty.

        Args:
            content (str): main message body
            me (bool): whether to send as an action, where the current account's name prefixes the message
            rich (bool): whether to send with rich text formatting

        Returns:
            .SkypeMsg: copy of the edited message object
        """
        return self.chat.sendMsg(content, me, rich, self.id)

    def delete(self):
        """
        Delete the message and remove it from the conversation.

        Equivalent to calling :meth:`edit` with an empty ``content`` string.

        Returns:
            .SkypeMsg: copy of the deleted message object
        """
        return self.edit("")


class SkypeTextMsg(SkypeMsg):
    """
    A message containing rich or plain text.

    Attributes:
        plain (str):
            Message content converted to plain text.

            Hyperlinks are replaced with their target, quotes are converted to the legacy format, and all other HTML
            tags are stripped from the text.
        markup (str):
            Message converted to plain text, retaining formatting markup.

            Hyperlinks become their target, message edit tags are stripped, and legacy quote text is used.

            In addition, the following replacements are made:

            ===============================  =========================
            Rich text                        Plain text
            ===============================  =========================
            ``<b>bold</b>``                  ``*bold*``
            ``<i>italic</i>``                ``_italic_``
            ``<s>strikethrough</s>``         ``~strikethrough~``
            ``<pre>monospace</pre>``         ``{code}monospace{code}``
            ``<at id="8:fred.2">Fred</at>``  ``@fred.2``
            ===============================  =========================
    """

    @property
    def plain(self):
        if self.content is None:
            return None
        text = re.sub(r"</?(e|b|i|ss?|pre|quote|legacyquote)\b.*?>", "", self.content)
        text = re.sub(r"""<a\b.*?href="(.*?)">.*?</a>""", r"\1", text)
        text = re.sub(r"""<at\b.*?id="8:(.*?)">.*?</at>""", r"@\1", text)
        text = (text.replace("&lt;", "<").replace("&gt;", ">").replace("&amp;", "&")
                    .replace("&quot;", "\"").replace("&apos;", "'"))
        return text

    @property
    def markup(self):
        if self.content is None:
            return None
        text = re.sub(r"</?(e|ss|quote|legacyquote)\b.*?>", "", self.content)
        text = re.sub(r"</?b\b.*?>", "*", text)
        text = re.sub(r"</?i\b.*?>", "_", text)
        text = re.sub(r"</?s\b.*?>", "~", text)
        text = re.sub(r"</?pre\b.*?>", "{code}", text)
        text = re.sub(r"""<a\b.*?href="(.*?)">.*?</a>""", r"\1", text)
        text = re.sub(r"""<at\b.*?id="8:(.*?)">.*?</at>""", r"@\1", text)
        text = (text.replace("&lt;", "<").replace("&gt;", ">").replace("&amp;", "&")
                    .replace("&quot;", "\"").replace("&apos;", "'"))
        return text


@SkypeUtils.initAttrs
@SkypeUtils.convertIds(users=("contact",))
class SkypeContactMsg(SkypeMsg):
    """
    A message containing one or more shared contacts.

    Attributes:
        contacts (:class:`.SkypeUser` list):
            User objects embedded in the message.
        contactNames (str list):
            Names of the users, as seen by the sender of the message.
    """

    attrs = SkypeMsg.attrs + ("contactIds", "contactNames")

    @classmethod
    def rawToFields(cls, raw={}):
        fields = super(SkypeContactMsg, cls).rawToFields(raw)
        fields.update({"contactIds": [], "contactNames": []})
        contactTags = BeautifulSoup(raw.get("content"), "html.parser").find_all("c")
        for tag in contactTags:
            fields["contactIds"].append(tag.get("s"))
            fields["contactNames"].append(tag.get("f"))
        return fields

    @property
    def html(self):
        tag = makeTag("contacts")
        for con in self.contacts:
            tag.append(makeTag("c", t="s", s=con.id, f=con.name))
        return tag


@SkypeUtils.initAttrs
class SkypeLocationMsg(SkypeMsg):
    """
    A message containing the sender's location.

    Attributes:
        latitude (float):
            North-South coordinate of the user's location.
        longitude (float):
            East-West coordinate of the user's location.
        altitude (int):
            Vertical position from sea level.
        speed (int):
            Current velocity during the reading.
        course (int):
            Current direction during the recording.
        address (str):
            Geocoded address provided by the sender.
        mapUrl (str):
            Link to map displaying the location.
    """

    attrs = SkypeMsg.attrs + ("latitude", "longitude", "altitude", "speed", "course", "address", "mapUrl")

    @classmethod
    def rawToFields(cls, raw={}):
        fields = super(SkypeLocationMsg, cls).rawToFields(raw)
        locTag = BeautifulSoup(raw.get("content"), "html.parser").find("location")
        for attr in ("latitude", "longitude", "altitude", "speed", "course"):
            fields[attr] = int(locTag.get(attr)) if locTag.get(attr) else None
        # Exponent notation produces a float, meaning lat/long will always be floats too.
        for attr in ("latitude", "longitude"):
            if fields[attr]:
                fields[attr] /= 1e6
        fields.update({"address": locTag.get("address"),
                       "mapUrl": locTag.find("a").get("href")})
        return fields

    @property
    def html(self):
        timestamp = self.time or datetime.now()
        params = {}
        for attr in ("latitude", "longitude", "altitude", "speed", "course"):
            if getattr(self, attr):
                params[attr] = getattr(self, attr)
        for attr in ("latitude", "longitude"):
            if attr in params:
                params[attr] = int(params[attr] * 1e6)
        if self.address:
            params["address"] = self.address
        params.update({"pointOfInterest": "",
                       "timeStamp": str(int(time.mktime(timestamp.timetuple())))})
        tag = makeTag("location", **params)
        tag.append(makeTag("a", self.address, href=self.mapUrl))
        return tag


@SkypeUtils.initAttrs
class SkypeCardMsg(SkypeMsg):
    """
    A message containing an interactive card.

    Attributes:
        title (str):
            Heading text at the top of the card.
        body (str):
            Main text content in the card.
        buttons (:class:`Button` list):
            Available actions for this card.
    """

    @SkypeUtils.initAttrs
    class Button(SkypeObj):
        """
        A clickable button within a card.

        Attributes:
            type (str):
                Type of action to be performed on click.
            title (str):
                Text displayed on the button.
            value (str):
                Parameter to the action.
        """

        attrs = ("type", "title", "value")

        @property
        def data(self):
            return dict((k, getattr(self, k)) for k in self.attrs)

    attrs = SkypeMsg.attrs + ("title", "body", "buttons")

    @classmethod
    def rawToFields(cls, raw={}):
        fields = super(SkypeCardMsg, cls).rawToFields(raw)
        swiftTag = BeautifulSoup(raw.get("content"), "html.parser").find("swift")
        data = json.loads(base64.b64decode(swiftTag.get("b64")))
        card = data.get("attachments", [{}])[0].get("content", {})
        fields.update({"title": card.get("title"),
                       "body": card.get("text"),
                       "buttons": [cls.Button(**button) for button in card.get("buttons")]})
        return fields

    @property
    def html(self):
        data = {"attachments": [{"content": {"title": self.title,
                                             "text": self.body,
                                             "buttons": [button.data for button in self.buttons]},
                                 "contentType": "application/vnd.microsoft.card.hero"}],
                "type": "message/card",
                "timestamp": datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%fZ")}
        if self.chatId:
            data["recipient"] = {"id": self.chatId}
            userType, userId = self.chatId.split(":", 1)
            if userType == "19":
                # Cards haven't been seen in group conversations yet, so assuming a sensible behaviour.
                data["recipient"]["name"] = self.chat.topic
            elif self.skype:
                data["recipient"]["name"] = str(self.skype.contacts[userId].name)
        b64 = base64.b64encode(json.dumps(data, separators=(",", ":")).encode("utf-8")).decode("utf-8")
        tag = makeTag("URIObject", "Card - access it on ", type="SWIFT.1",
                      url_thumbnail="https://urlp.asm.skype.com/v1/url/content?url=https://"
                                    "neu1-urlp.secure.skypeassets.com/static/card-128x128.png")
        tag.append(makeTag("a", "https://go.skype.com/cards.unsupported",
                           href="https://go.skype.com/cards.unsupported"))
        tag.append(". ")
        tag.append(makeTag("Swift", b64=b64))
        tag.append(makeTag("Description"))
        return tag


@SkypeUtils.initAttrs
class SkypeFileMsg(SkypeMsg):
    """
    A message containing a file shared in a conversation.

    Attributes:
        file (:class:`File`):
            File object embedded in the message.
        fileContent (bytes):
            Raw content of the file.
    """

    @SkypeUtils.initAttrs
    class File(SkypeObj):
        """
        Details about a file contained within a message.

        Attributes:
            name (str):
                Original filename from the client.
            size (int):
                Number of bytes in the file.
            urlFull (str):
                URL to retrieve the original file.
            urlThumb (str):
                URL to retrieve a thumbnail or display image for the file.
            urlView (str):
                URL for the user to access the file outside of the API.
        """

        attrs = ("name", "size", "urlFull", "urlThumb", "urlView")

        @property
        def urlAsm(self):
            # Workaround for Skype providing full URLs with the wrong domain.
            # api.asm.skype.com/.../0-xxx-yy-zzz... -> xxx-api.asm.skype.com
            if not self.urlFull:
                return None
            match = re.match("{}/0-([a-z0-9]+)-".format(SkypeConnection.API_ASM), self.urlFull)
            if not match:
                return self.urlFull
            prefix = SkypeConnection.API_ASM_LOCAL.format(match.group(1))
            return self.urlFull.replace(SkypeConnection.API_ASM, prefix, 1)

    attrs = SkypeMsg.attrs + ("file",)

    @classmethod
    def rawToFields(cls, raw={}):
        fields = super(SkypeFileMsg, cls).rawToFields(raw)
        # BeautifulSoup converts tag names to lower case, and find() is case-sensitive.
        file = BeautifulSoup(raw.get("content"), "html.parser").find("uriobject")
        if file:
            fileFields = {"name": (file.find("originalname") or {}).get("v"),
                          "size": (file.find("filesize") or {}).get("v"),
                          "urlFull": file.get("uri"),
                          "urlThumb": file.get("url_thumbnail"),
                          "urlView": (file.find("a") or {}).get("href")}
            fields["file"] = SkypeFileMsg.File(**fileFields)
        return fields

    @property
    @SkypeUtils.cacheResult
    def fileContent(self):
        if not self.file:
            return None
        return self.skype.conn("GET", "{0}/views/original".format(self.file.urlAsm),
                               auth=SkypeConnection.Auth.Authorize).content

    @property
    def html(self):
        if not self.file:
            return ""
        tag = makeTag("URIObject", type="File.1", uri=self.file.urlFull, url_thumbnail=self.file.urlThumb)
        tag.append(makeTag("Title", "Title: {0}".format(self.file.name) if self.file.name else ""))
        tag.append(makeTag("Description", "Description: {0}".format(self.file.name) if self.file.name else ""))
        tag.append(makeTag("FileSize", v=self.file.size))
        tag.append(makeTag("OriginalName", v=self.file.name))
        tag.append(makeTag("a", self.file.urlView, href=self.file.urlView))
        return tag


@SkypeUtils.initAttrs
class SkypeImageMsg(SkypeFileMsg):
    """
    A message containing a picture shared in a conversation.
    """

    @property
    @SkypeUtils.cacheResult
    def fileContent(self):
        if not self.file:
            return None
        return self.skype.conn("GET", "{0}/views/imgpsh_fullsize".format(self.file.urlAsm),
                               auth=SkypeConnection.Auth.Authorize).content

    @property
    def html(self):
        if not self.file:
            return ""
        tag = makeTag("URIObject", type="Picture.1", uri=self.file.urlFull, url_thumbnail=self.file.urlThumb)
        tag.append(makeTag("Title"))
        tag.append(makeTag("Description"))
        tag.append(makeTag("OriginalName", v=self.file.name))
        tag.append(makeTag("a", self.file.urlView, href=self.file.urlView))
        tag.append(makeTag("meta", type="photo", originalName=self.file.name))
        return tag


@SkypeUtils.initAttrs
@SkypeUtils.convertIds("users")
class SkypeCallMsg(SkypeMsg):
    """
    A message representing a change in state to a voice or video call inside the conversation.

    Attributes:
        state (:class:`.State`):
            New state of the call.
        users (:class:`.SkypeUser` list):
            User objects embedded in the message.
        userNames (str list):
            Names of the users, as seen by the initiator of the call.
    """

    State = SkypeEnum("SkypeCallMsg.State", ("Started", "Ended", "Missed"))
    """
    :class:`.SkypeEnum`: Possible call states (either started and incoming, or ended).

    Attributes:
        State.Started:
            New call has just begun.
        State.Ended:
            Call failed to connect, or all call participants have hung up.
        State.Missed:
            Missed the call as it ended.
    """

    attrs = SkypeMsg.attrs + ("state", "userIds", "userNames")

    @classmethod
    def rawToFields(cls, raw={}):
        fields = super(SkypeCallMsg, cls).rawToFields(raw)
        listTag = BeautifulSoup(raw.get("content"), "html.parser").find("partlist")
        fields.update({"state": {"started": cls.State.Started,
                                 "ended": cls.State.Ended,
                                 "missed": cls.State.Missed}.get(listTag.get("type")),
                       "userIds": [], "userNames": []})
        for partTag in listTag.find_all("part"):
            fields["userIds"].append(SkypeUtils.noPrefix(partTag.get("identity")))
            fields["userNames"].append(partTag.find("name").text)
        return fields

    @property
    def html(self):
        partType = {self.State.Started: "started",
                    self.State.Ended: "ended",
                    self.State.Missed: "missed"}[self.state]
        tag = makeTag("partlist", type=partType, alt="")
        for user in self.users:
            conTag = makeTag("part", identity=user.id)
            conTag.append(makeTag("name", str(user.name)))
            tag.append(conTag)
        return tag


@SkypeUtils.initAttrs
class SkypePropertyMsg(SkypeMsg):
    """
    A base message type for changes to conversation properties.
    """

    def tagTemplate(self, root):
        # Subclasses of this class have the same message structure.
        timestamp = self.time or datetime.now()
        tag = makeTag(root)
        tag.append(makeTag("eventtime", str(int(time.mktime(timestamp.timetuple())))))
        tag.append(makeTag("initiator", "8:{0}".format(self.userId) if self.userId else ""))
        return tag


@SkypeUtils.initAttrs
class SkypeTopicPropertyMsg(SkypePropertyMsg):
    """
    A message representing a change in a group conversation's topic.

    Attributes:
        topic (str):
            Description of the conversation, shown to all participants.
    """

    attrs = SkypeMsg.attrs + ("topic",)

    @classmethod
    def rawToFields(cls, raw={}):
        fields = super(SkypeTopicPropertyMsg, cls).rawToFields(raw)
        propInfo = BeautifulSoup(raw.get("content"), "html.parser").find("topicupdate")
        if propInfo:
            fields.update({"userId": SkypeUtils.noPrefix(propInfo.find("initiator").text),
                           "topic": propInfo.find("value").text})
        return fields

    @property
    def html(self):
        tag = self.tagTemplate("topicupdate")
        tag.append(makeTag("value", self.topic))
        return tag


@SkypeUtils.initAttrs
class SkypeOpenPropertyMsg(SkypePropertyMsg):
    """
    A message representing a change to joining the conversation by link.

    Attributes:
        open (bool):
            Whether new participants can join via a public join link.
    """

    attrs = SkypeMsg.attrs + ("open",)

    @classmethod
    def rawToFields(cls, raw={}):
        fields = super(SkypeOpenPropertyMsg, cls).rawToFields(raw)
        propInfo = BeautifulSoup(raw.get("content"), "html.parser").find("joiningenabledupdate")
        if propInfo:
            fields.update({"userId": SkypeUtils.noPrefix(propInfo.find("initiator").text),
                           "open": propInfo.find("value").text == "true"})
        return fields

    @property
    def html(self):
        tag = self.tagTemplate("joiningenabledupdate")
        tag.append(makeTag("value", "true" if self.open else "false"))
        return tag


@SkypeUtils.initAttrs
class SkypeHistoryPropertyMsg(SkypePropertyMsg):
    """
    A message representing a change to history disclosure.

    Attributes:
        history (bool):
            Whether message history is provided to new participants.
    """

    attrs = SkypeMsg.attrs + ("history",)

    @classmethod
    def rawToFields(cls, raw={}):
        fields = super(SkypeHistoryPropertyMsg, cls).rawToFields(raw)
        propInfo = BeautifulSoup(raw.get("content"), "html.parser").find("historydisclosedupdate")
        if propInfo:
            fields.update({"userId": SkypeUtils.noPrefix(propInfo.find("initiator").text),
                           "history": propInfo.find("value").text == "true"})
        return fields

    @property
    def html(self):
        tag = self.tagTemplate("historydisclosedupdate")
        tag.append(makeTag("value", "true" if self.history else "false"))
        return tag


@SkypeUtils.initAttrs
@SkypeUtils.convertIds(user=("member",))
class SkypeMemberMsg(SkypePropertyMsg):
    """
    A message representing a change in a group conversation's participants.

    Note that Skype represents these messages as being sent *by the conversation*, rather than the initiator.  Instead,
    :attr:`user <SkypeMsg.user>` is set to the initiator, and :attr:`member` to the target.

    Attributes:
        member (:class:`.SkypeUser`):
            User being added to or removed from the conversation.
    """

    attrs = SkypeMsg.attrs + ("memberId",)


@SkypeUtils.initAttrs
class SkypeAddMemberMsg(SkypeMemberMsg):
    """
    A message representing a user added to a group conversation.
    """

    @classmethod
    def rawToFields(cls, raw={}):
        fields = super(SkypeAddMemberMsg, cls).rawToFields(raw)
        memInfo = BeautifulSoup(raw.get("content"), "html.parser").find("addmember")
        if memInfo:
            fields.update({"userId": SkypeUtils.noPrefix(memInfo.find("initiator").text),
                           "memberId": SkypeUtils.noPrefix(memInfo.find("target").text)})
        return fields

    @property
    def html(self):
        tag = self.tagTemplate("addmember")
        tag.append(makeTag("target", "8:{0}".format(self.memberId) if self.memberId else ""))
        return tag


@SkypeUtils.initAttrs
class SkypeChangeMemberMsg(SkypeMemberMsg):
    """
    A message representing a user's role being changed within a group conversation.

    Attributes:
        admin (bool):
            Whether the change now makes the user an admin.
    """

    attrs = SkypeMemberMsg.attrs + ("admin",)

    @classmethod
    def rawToFields(cls, raw={}):
        fields = super(SkypeChangeMemberMsg, cls).rawToFields(raw)
        memInfo = BeautifulSoup(raw.get("content"), "html.parser").find("roleupdate")
        if memInfo:
            fields.update({"userId": SkypeUtils.noPrefix(memInfo.find("initiator").text),
                           "memberId": SkypeUtils.noPrefix(memInfo.find("target").find("id").text),
                           "admin": memInfo.find("target").find("role").text == "admin"})
        return fields

    @property
    def html(self):
        tag = self.tagTemplate("addmember")
        valTag = makeTag("target")
        valTag.append(makeTag("id", "8:{0}".format(self.memberId) if self.memberId else ""))
        valTag.append(makeTag("role", "admin" if self.admin else "user"))
        tag.append(valTag)
        return tag


@SkypeUtils.initAttrs
class SkypeRemoveMemberMsg(SkypeMemberMsg):
    """
    A message representing a user removed from a group conversation.
    """

    @classmethod
    def rawToFields(cls, raw={}):
        fields = super(SkypeRemoveMemberMsg, cls).rawToFields(raw)
        memInfo = BeautifulSoup(raw.get("content"), "html.parser").find("deletemember")
        if memInfo:
            fields.update({"userId": SkypeUtils.noPrefix(memInfo.find("initiator").text),
                           "memberId": SkypeUtils.noPrefix(memInfo.find("target").text)})
        return fields

    @property
    def html(self):
        tag = self.tagTemplate("addmember")
        tag.append(makeTag("target", "8:{0}".format(self.memberId) if self.memberId else ""))
        return tag
