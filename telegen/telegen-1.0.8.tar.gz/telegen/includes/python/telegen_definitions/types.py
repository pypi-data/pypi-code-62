from enum import Enum
from mimetypes import guess_type as guess_mime
from typing import List, Optional, Tuple


# method, endpoint, headers, params, body
EndpointCall = Tuple[str, str, Optional[dict], Optional[dict], Optional[bytes]]


class ParseMode(Enum):
    Markdown = 1
    HTML = 2
    MarkdownV2 = 3


class InputFile:
    def __init__(self, file_id: str, *, body: Optional[bytes] = None, content_type: Optional[str] = None):
        # file id, file name or url
        self.file_id = file_id

        self.body = body
        if body:
            self.content_type = (content_type or guess_mime(file_id)[0]).encode()  # type: ignore

    def update(self, file_id: str):
        self.file_id = file_id
        self.body = None

    def __call__(
        self,
        field_name: str,
        files: List[Tuple[bytes, bytes, bytes, bytes]],
        params: dict,
        *,
        attach: Optional[str] = None,
    ):
        body = self.body
        if body:
            if attach:
                files.append((attach.encode(), self.file_id.encode(), self.content_type, body))
                params[field_name] = f"attach://{attach}"
            else:
                files.append((field_name.encode(), self.file_id.encode(), self.content_type, body))
        else:
            params[field_name] = self.file_id


class InlineKeyboardMarkup:
    __slots__ = ["serialized", "__current_row"]

    def __init__(self):
        row = []
        self.serialized = {"inline_keyboard": [row]}
        self.__current_row = row

    def add_row(self):
        row = []
        self.serialized["inline_keyboard"].append(row)
        self.__current_row = row
        return self

    def url(self, text: str, url: str):
        self.__current_row.append({"text": text, "url": url})
        return self

    def login_url(
        self,
        text: str,
        url: str,
        *,
        forward_text: str = None,
        bot_username: str = None,
        request_write_access: bool = False,
    ):
        login_url: dict = {"url": url}

        if forward_text:
            login_url["forward_text"] = forward_text

        if bot_username:
            login_url["bot_username"] = bot_username

        if request_write_access:
            login_url["request_write_access"] = True

        self.__current_row.append({"text": text, "login_url": login_url})
        return self

    def callback_data(self, text: str, callback_data: bytes):
        assert 0 < len(callback_data) < 64
        self.__current_row.append({"text": text, "callback_data": callback_data})
        return self

    def switch_inline_query(self, text: str, switch_inline_query: str):
        self.__current_row.append({"text": text, "switch_inline_query": switch_inline_query})
        return self

    def switch_inline_query_current_chat(self, text: str, switch_inline_query_current_chat: str):
        self.__current_row.append({"text": text, "switch_inline_query_current_chat": switch_inline_query_current_chat})
        return self

    def callback_game(self, text: str):
        assert len(self.serialized["inline_keyboard"]) == 1 and len(self.__current_row) == 0
        self.__current_row.append({"text": text, "callback_game": {}})
        return self

    def pay(self, text: str):
        assert len(self.serialized["inline_keyboard"]) == 1 and len(self.__current_row) == 0
        self.__current_row.append({"text": text, "pay": True})
        return self


class ReplyKeyboardMarkup:
    __slots__ = ["serialized", "__current_row"]

    def __init__(self):
        row = []
        self.serialized = {"keyboard": [row]}
        self.__current_row = row

    def add_row(self):
        row = []
        self.serialized["keyboard"].append(row)
        self.__current_row = row
        return self

    def add_button(self, text, *, request_contact=False, request_location=False):
        button = {"text": text}

        if request_contact:
            button["request_contact"] = True

        if request_location:
            button["request_location"] = True

        self.__current_row.append(button)
        return self

    def resize_keyboard(self, resize_keyboard: bool = True):
        self.serialized["resize_keyboard"] = resize_keyboard
        return self

    def one_time_keyboard(self, one_time_keyboard: bool = True):
        self.serialized["one_time_keyboard"] = one_time_keyboard
        return self

    def selective(self, selective: bool = True):
        self.serialized["selective"] = selective
        return self


class ReplyKeyboardRemove:
    __slots__ = ["serialized"]

    def __init__(self):
        self.serialized = {"remove_keyboard": True}

    def selective(self, selective: bool = True):
        self.serialized["selective"] = selective
        return self


class ForceReply:
    __slots__ = ["serialized"]

    def __init__(self):
        self.serialized = {"force_reply": True}

    def selective(self, selective: bool = True):
        self.serialized["selective"] = selective
        return self
