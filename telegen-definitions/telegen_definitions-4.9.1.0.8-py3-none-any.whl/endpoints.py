from json import dumps as json_dumps
from typing import List, Optional, Tuple, Union
from uuid import uuid4

from .generated import InputMedia, InputMediaPhoto, InputMediaVideo
from .multipart_encoder import MultipartEncoder
from .types import InlineKeyboardMarkup


def sendMediaGroup(
    chat_id: Union[int, str],
    media: List[Union[InputMediaPhoto, InputMediaVideo]],
    *,
    disable_notification: Optional[bool] = None,
    reply_to_message_id: Optional[int] = None
):
    files: List[Tuple[bytes, bytes, bytes, bytes]] = []

    params: dict = {"chat_id": chat_id}

    for _media in media:
        _media["media"]("media", files, _media, attach=uuid4().hex)  # type: ignore

    params["media"] = json_dumps(media, check_circular=False)

    if disable_notification is not None:
        params["disable_notification"] = disable_notification

    if reply_to_message_id is not None:
        params["reply_to_message_id"] = reply_to_message_id

    if files:
        headers: dict = {}
        encoder = MultipartEncoder(files=files)
        headers["content-type"], body = encoder.encode()
        headers["content-length"] = len(body)
        return "POST", "sendMediaGroup", headers, params, body
    else:
        return "GET", "sendMediaGroup", None, params, None


def editMessageMedia(
    media: InputMedia,
    *,
    chat_id: Optional[Union[int, str]] = None,
    message_id: Optional[int] = None,
    inline_message_id: Optional[str] = None,
    reply_markup: Optional[InlineKeyboardMarkup] = None
):
    files: List[Tuple[bytes, bytes, bytes, bytes]] = []

    params: dict = {}

    media["media"]("media", files, media, attach="media")  # type: ignore
    params["media"] = json_dumps(media, check_circular=False)

    if chat_id is not None:
        params["chat_id"] = chat_id

    if message_id is not None:
        params["message_id"] = message_id

    if inline_message_id is not None:
        params["inline_message_id"] = inline_message_id

    if reply_markup is not None:
        params["reply_markup"] = json_dumps(reply_markup.serialized)

    if files:
        headers: dict = {}
        encoder = MultipartEncoder(files=files)
        headers["content-type"], body = encoder.encode()
        headers["content-length"] = len(body)
        return "POST", "editMessageMedia", headers, params, body
    else:
        return "GET", "editMessageMedia", None, params, None
