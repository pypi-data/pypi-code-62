from json import dumps as json_dumps
from typing import List, Optional, Tuple, Union

try:
    from typing import TypedDict
except:
    try:
        from mypy_extensions import TypedDict
    except:
        TypedDict = dict

from .multipart_encoder import MultipartEncoder
from .types import *


class InputMedia(TypedDict, total=False):
    pass


class InlineQueryResult(TypedDict, total=False):
    pass


class InputMessageContent(TypedDict, total=False):
    pass


class PassportElementError(TypedDict, total=False):
    pass


class InputContactMessageContent(InputMessageContent, total=False):
    phone_number: str
    first_name: str
    vcard: Optional[str]
    last_name: Optional[str]


class InputVenueMessageContent(InputMessageContent, total=False):
    title: str
    address: str
    latitude: float
    longitude: float
    foursquare_id: Optional[str]
    foursquare_type: Optional[str]


class InputTextMessageContent(InputMessageContent, total=False):
    message_text: str
    disable_web_page_preview: Optional[bool]
    parse_mode: Optional[ParseMode]


class InputLocationMessageContent(InputMessageContent, total=False):
    latitude: float
    longitude: float
    live_period: Optional[int]


class LoginUrl(TypedDict, total=False):
    url: str
    forward_text: Optional[str]
    bot_username: Optional[str]
    request_write_access: Optional[bool]


class KeyboardButtonPollType(TypedDict, total=False):
    type: Optional[str]


class CallbackGame(TypedDict, total=False):
    pass


class InlineQueryResultCachedVoice(InlineQueryResult, total=False):
    id: str
    type: str
    title: str
    voice_file_id: str
    input_message_content: Optional[InputMessageContent]
    parse_mode: Optional[ParseMode]
    reply_markup: Optional[InlineKeyboardMarkup]
    caption: Optional[str]


class PassportElementErrorTranslationFiles(PassportElementError, total=False):
    message: str
    type: str
    file_hashes: List[str]
    source: str


class InlineQueryResultDocument(InlineQueryResult, total=False):
    id: str
    document_url: str
    type: str
    title: str
    mime_type: str
    thumb_height: Optional[int]
    description: Optional[str]
    parse_mode: Optional[ParseMode]
    input_message_content: Optional[InputMessageContent]
    thumb_width: Optional[int]
    thumb_url: Optional[str]
    reply_markup: Optional[InlineKeyboardMarkup]
    caption: Optional[str]


class PassportElementErrorDataField(PassportElementError, total=False):
    data_hash: str
    field_name: str
    type: str
    source: str
    message: str


class InlineQueryResultCachedSticker(InlineQueryResult, total=False):
    id: str
    sticker_file_id: str
    type: str
    input_message_content: Optional[InputMessageContent]
    reply_markup: Optional[InlineKeyboardMarkup]


class InputMediaAnimation(InputMedia, total=False):
    type: str
    media: InputFile
    width: Optional[int]
    duration: Optional[int]
    thumb: Optional[InputFile]
    parse_mode: Optional[ParseMode]
    height: Optional[int]
    caption: Optional[str]


class PassportElementErrorUnspecified(PassportElementError, total=False):
    message: str
    element_hash: str
    type: str
    source: str


class InlineQueryResultVoice(InlineQueryResult, total=False):
    id: str
    type: str
    title: str
    voice_url: str
    input_message_content: Optional[InputMessageContent]
    parse_mode: Optional[ParseMode]
    reply_markup: Optional[InlineKeyboardMarkup]
    voice_duration: Optional[int]
    caption: Optional[str]


class InlineQueryResultCachedVideo(InlineQueryResult, total=False):
    id: str
    type: str
    video_file_id: str
    title: str
    description: Optional[str]
    parse_mode: Optional[ParseMode]
    input_message_content: Optional[InputMessageContent]
    reply_markup: Optional[InlineKeyboardMarkup]
    caption: Optional[str]


class InlineQueryResultLocation(InlineQueryResult, total=False):
    id: str
    type: str
    title: str
    latitude: float
    longitude: float
    thumb_height: Optional[int]
    input_message_content: Optional[InputMessageContent]
    thumb_width: Optional[int]
    live_period: Optional[int]
    thumb_url: Optional[str]
    reply_markup: Optional[InlineKeyboardMarkup]


class InputMediaAudio(InputMedia, total=False):
    type: str
    media: InputFile
    duration: Optional[int]
    title: Optional[str]
    thumb: Optional[InputFile]
    parse_mode: Optional[ParseMode]
    caption: Optional[str]
    performer: Optional[str]


class InlineQueryResultVideo(InlineQueryResult, total=False):
    id: str
    video_url: str
    type: str
    title: str
    mime_type: str
    thumb_url: str
    description: Optional[str]
    parse_mode: Optional[ParseMode]
    video_duration: Optional[int]
    input_message_content: Optional[InputMessageContent]
    video_width: Optional[int]
    reply_markup: Optional[InlineKeyboardMarkup]
    caption: Optional[str]
    video_height: Optional[int]


class InlineQueryResultCachedGif(InlineQueryResult, total=False):
    gif_file_id: str
    id: str
    type: str
    title: Optional[str]
    input_message_content: Optional[InputMessageContent]
    parse_mode: Optional[ParseMode]
    reply_markup: Optional[InlineKeyboardMarkup]
    caption: Optional[str]


class InputMediaPhoto(InputMedia, total=False):
    media: InputFile
    type: str
    caption: Optional[str]
    parse_mode: Optional[ParseMode]


class InputMediaVideo(InputMedia, total=False):
    type: str
    media: InputFile
    width: Optional[int]
    duration: Optional[int]
    supports_streaming: Optional[bool]
    thumb: Optional[InputFile]
    parse_mode: Optional[ParseMode]
    height: Optional[int]
    caption: Optional[str]


class PassportElementErrorFrontSide(PassportElementError, total=False):
    message: str
    type: str
    file_hash: str
    source: str


class InlineQueryResultCachedDocument(InlineQueryResult, total=False):
    id: str
    document_file_id: str
    type: str
    title: str
    description: Optional[str]
    input_message_content: Optional[InputMessageContent]
    parse_mode: Optional[ParseMode]
    reply_markup: Optional[InlineKeyboardMarkup]
    caption: Optional[str]


class PassportElementErrorFiles(PassportElementError, total=False):
    message: str
    type: str
    file_hashes: List[str]
    source: str


class InlineQueryResultCachedMpeg4Gif(InlineQueryResult, total=False):
    id: str
    mpeg4_file_id: str
    type: str
    title: Optional[str]
    input_message_content: Optional[InputMessageContent]
    parse_mode: Optional[ParseMode]
    reply_markup: Optional[InlineKeyboardMarkup]
    caption: Optional[str]


class PassportElementErrorSelfie(PassportElementError, total=False):
    message: str
    type: str
    file_hash: str
    source: str


class PassportElementErrorReverseSide(PassportElementError, total=False):
    message: str
    type: str
    file_hash: str
    source: str


class InlineQueryResultMpeg4Gif(InlineQueryResult, total=False):
    id: str
    mpeg4_url: str
    type: str
    thumb_url: str
    mpeg4_width: Optional[int]
    mpeg4_duration: Optional[int]
    mpeg4_height: Optional[int]
    title: Optional[str]
    input_message_content: Optional[InputMessageContent]
    parse_mode: Optional[ParseMode]
    thumb_mime_type: Optional[str]
    reply_markup: Optional[InlineKeyboardMarkup]
    caption: Optional[str]


class InputMediaDocument(InputMedia, total=False):
    type: str
    media: InputFile
    thumb: Optional[InputFile]
    parse_mode: Optional[ParseMode]
    caption: Optional[str]


class InlineQueryResultAudio(InlineQueryResult, total=False):
    id: str
    type: str
    title: str
    audio_url: str
    audio_duration: Optional[int]
    input_message_content: Optional[InputMessageContent]
    parse_mode: Optional[ParseMode]
    reply_markup: Optional[InlineKeyboardMarkup]
    caption: Optional[str]
    performer: Optional[str]


class InlineQueryResultGame(InlineQueryResult, total=False):
    id: str
    type: str
    game_short_name: str
    reply_markup: Optional[InlineKeyboardMarkup]


class InlineQueryResultGif(InlineQueryResult, total=False):
    id: str
    type: str
    thumb_url: str
    gif_url: str
    caption: Optional[str]
    title: Optional[str]
    input_message_content: Optional[InputMessageContent]
    parse_mode: Optional[ParseMode]
    thumb_mime_type: Optional[str]
    gif_height: Optional[int]
    gif_width: Optional[int]
    gif_duration: Optional[int]
    reply_markup: Optional[InlineKeyboardMarkup]


class InlineQueryResultPhoto(InlineQueryResult, total=False):
    id: str
    type: str
    photo_url: str
    thumb_url: str
    title: Optional[str]
    photo_height: Optional[int]
    description: Optional[str]
    parse_mode: Optional[ParseMode]
    input_message_content: Optional[InputMessageContent]
    photo_width: Optional[int]
    reply_markup: Optional[InlineKeyboardMarkup]
    caption: Optional[str]


class InlineQueryResultVenue(InlineQueryResult, total=False):
    id: str
    type: str
    title: str
    address: str
    latitude: float
    longitude: float
    thumb_height: Optional[int]
    input_message_content: Optional[InputMessageContent]
    thumb_width: Optional[int]
    foursquare_id: Optional[str]
    foursquare_type: Optional[str]
    thumb_url: Optional[str]
    reply_markup: Optional[InlineKeyboardMarkup]


class PassportElementErrorTranslationFile(PassportElementError, total=False):
    message: str
    type: str
    file_hash: str
    source: str


class PassportElementErrorFile(PassportElementError, total=False):
    message: str
    type: str
    file_hash: str
    source: str


class InlineQueryResultArticle(InlineQueryResult, total=False):
    id: str
    type: str
    input_message_content: InputMessageContent
    title: str
    thumb_height: Optional[int]
    url: Optional[str]
    description: Optional[str]
    thumb_width: Optional[int]
    thumb_url: Optional[str]
    reply_markup: Optional[InlineKeyboardMarkup]
    hide_url: Optional[bool]


class InlineQueryResultCachedAudio(InlineQueryResult, total=False):
    id: str
    audio_file_id: str
    type: str
    input_message_content: Optional[InputMessageContent]
    parse_mode: Optional[ParseMode]
    reply_markup: Optional[InlineKeyboardMarkup]
    caption: Optional[str]


class InlineQueryResultContact(InlineQueryResult, total=False):
    id: str
    phone_number: str
    type: str
    first_name: str
    thumb_height: Optional[int]
    input_message_content: Optional[InputMessageContent]
    thumb_width: Optional[int]
    vcard: Optional[str]
    thumb_url: Optional[str]
    reply_markup: Optional[InlineKeyboardMarkup]
    last_name: Optional[str]


class InlineQueryResultCachedPhoto(InlineQueryResult, total=False):
    id: str
    type: str
    photo_file_id: str
    caption: Optional[str]
    description: Optional[str]
    title: Optional[str]
    input_message_content: Optional[InputMessageContent]
    parse_mode: Optional[ParseMode]
    reply_markup: Optional[InlineKeyboardMarkup]


class MaskPosition(TypedDict, total=False):
    point: str
    x_shift: float
    y_shift: float
    scale: float


class ChatPermissions(TypedDict, total=False):
    can_send_messages: Optional[bool]
    can_send_media_messages: Optional[bool]
    can_send_polls: Optional[bool]
    can_send_other_messages: Optional[bool]
    can_add_web_page_previews: Optional[bool]
    can_change_info: Optional[bool]
    can_invite_users: Optional[bool]
    can_pin_messages: Optional[bool]


class BotCommand(TypedDict, total=False):
    command: str
    description: str


class LabeledPrice(TypedDict, total=False):
    label: str
    amount: int


class ShippingOption(TypedDict, total=False):
    id: str
    title: str
    prices: List[LabeledPrice]


def getUpdates(*,
    offset: Optional[int] = None,
    limit: Optional[int] = None,
    timeout: Optional[int] = None,
    allowed_updates: Optional[List[str]] = None
) -> EndpointCall:
    params: dict = {}

    if offset is not None:
        params["offset"] = offset

    if limit is not None:
        params["limit"] = limit

    if timeout is not None:
        params["timeout"] = timeout

    if allowed_updates is not None:
        params["allowed_updates"] = allowed_updates

    return "GET", "getUpdates", None, params, None


def setWebhook(
    url: str,
    *,
    certificate: Optional[InputFile] = None,
    max_connections: Optional[int] = None,
    allowed_updates: Optional[List[str]] = None
) -> EndpointCall:
    files: List[Tuple[bytes, bytes, bytes, bytes]] = []

    params: dict = {
        "url": url,
    }

    if certificate is not None:
        certificate("certificate", files, params, attach=None)

    if max_connections is not None:
        params["max_connections"] = max_connections

    if allowed_updates is not None:
        params["allowed_updates"] = allowed_updates

    if files:
        headers: dict = {}
        encoder = MultipartEncoder(files=files)
        headers["content-type"], body = encoder.encode()
        headers["content-length"] = len(body)
        return "POST", "setWebhook", headers, params, body
    else:
        return "GET", "setWebhook", None, params, None


def deleteWebhook() -> EndpointCall:
    return "GET", "deleteWebhook", None, None, None


def getWebhookInfo() -> EndpointCall:
    return "GET", "getWebhookInfo", None, None, None


def getMe() -> EndpointCall:
    return "GET", "getMe", None, None, None


def sendMessage(
    chat_id: Union[int, str],
    text: str,
    *,
    parse_mode: Optional[ParseMode] = None,
    disable_web_page_preview: Optional[bool] = None,
    disable_notification: Optional[bool] = None,
    reply_to_message_id: Optional[int] = None,
    reply_markup: Optional[Union[InlineKeyboardMarkup, ReplyKeyboardMarkup, ReplyKeyboardRemove, ForceReply]] = None
) -> EndpointCall:
    params: dict = {
        "chat_id": chat_id,
        "text": text,
    }

    if parse_mode is not None:
        params["parse_mode"] = parse_mode.name

    if disable_web_page_preview is not None:
        params["disable_web_page_preview"] = disable_web_page_preview

    if disable_notification is not None:
        params["disable_notification"] = disable_notification

    if reply_to_message_id is not None:
        params["reply_to_message_id"] = reply_to_message_id

    if reply_markup is not None:
        params["reply_markup"] = json_dumps(reply_markup.serialized, check_circular=False)

    return "GET", "sendMessage", None, params, None


def forwardMessage(
    chat_id: Union[int, str],
    from_chat_id: Union[int, str],
    message_id: int,
    *,
    disable_notification: Optional[bool] = None
) -> EndpointCall:
    params: dict = {
        "chat_id": chat_id,
        "from_chat_id": from_chat_id,
        "message_id": message_id,
    }

    if disable_notification is not None:
        params["disable_notification"] = disable_notification

    return "GET", "forwardMessage", None, params, None


def sendPhoto(
    chat_id: Union[int, str],
    photo: InputFile,
    *,
    caption: Optional[str] = None,
    parse_mode: Optional[ParseMode] = None,
    disable_notification: Optional[bool] = None,
    reply_to_message_id: Optional[int] = None,
    reply_markup: Optional[Union[InlineKeyboardMarkup, ReplyKeyboardMarkup, ReplyKeyboardRemove, ForceReply]] = None
) -> EndpointCall:
    files: List[Tuple[bytes, bytes, bytes, bytes]] = []

    params: dict = {
        "chat_id": chat_id,
    }

    photo("photo", files, params, attach=None)

    if caption is not None:
        params["caption"] = caption

    if parse_mode is not None:
        params["parse_mode"] = parse_mode.name

    if disable_notification is not None:
        params["disable_notification"] = disable_notification

    if reply_to_message_id is not None:
        params["reply_to_message_id"] = reply_to_message_id

    if reply_markup is not None:
        params["reply_markup"] = json_dumps(reply_markup.serialized, check_circular=False)

    if files:
        headers: dict = {}
        encoder = MultipartEncoder(files=files)
        headers["content-type"], body = encoder.encode()
        headers["content-length"] = len(body)
        return "POST", "sendPhoto", headers, params, body
    else:
        return "GET", "sendPhoto", None, params, None


def sendAudio(
    chat_id: Union[int, str],
    audio: InputFile,
    *,
    caption: Optional[str] = None,
    parse_mode: Optional[ParseMode] = None,
    duration: Optional[int] = None,
    performer: Optional[str] = None,
    title: Optional[str] = None,
    thumb: Optional[InputFile] = None,
    disable_notification: Optional[bool] = None,
    reply_to_message_id: Optional[int] = None,
    reply_markup: Optional[Union[InlineKeyboardMarkup, ReplyKeyboardMarkup, ReplyKeyboardRemove, ForceReply]] = None
) -> EndpointCall:
    files: List[Tuple[bytes, bytes, bytes, bytes]] = []

    params: dict = {
        "chat_id": chat_id,
    }

    audio("audio", files, params, attach=None)

    if thumb is not None:
        thumb("thumb", files, params, attach="thumb")

    if caption is not None:
        params["caption"] = caption

    if parse_mode is not None:
        params["parse_mode"] = parse_mode.name

    if duration is not None:
        params["duration"] = duration

    if performer is not None:
        params["performer"] = performer

    if title is not None:
        params["title"] = title

    if disable_notification is not None:
        params["disable_notification"] = disable_notification

    if reply_to_message_id is not None:
        params["reply_to_message_id"] = reply_to_message_id

    if reply_markup is not None:
        params["reply_markup"] = json_dumps(reply_markup.serialized, check_circular=False)

    if files:
        headers: dict = {}
        encoder = MultipartEncoder(files=files)
        headers["content-type"], body = encoder.encode()
        headers["content-length"] = len(body)
        return "POST", "sendAudio", headers, params, body
    else:
        return "GET", "sendAudio", None, params, None


def sendDocument(
    chat_id: Union[int, str],
    document: InputFile,
    *,
    thumb: Optional[InputFile] = None,
    caption: Optional[str] = None,
    parse_mode: Optional[ParseMode] = None,
    disable_notification: Optional[bool] = None,
    reply_to_message_id: Optional[int] = None,
    reply_markup: Optional[Union[InlineKeyboardMarkup, ReplyKeyboardMarkup, ReplyKeyboardRemove, ForceReply]] = None
) -> EndpointCall:
    files: List[Tuple[bytes, bytes, bytes, bytes]] = []

    params: dict = {
        "chat_id": chat_id,
    }

    document("document", files, params, attach=None)

    if thumb is not None:
        thumb("thumb", files, params, attach="thumb")

    if caption is not None:
        params["caption"] = caption

    if parse_mode is not None:
        params["parse_mode"] = parse_mode.name

    if disable_notification is not None:
        params["disable_notification"] = disable_notification

    if reply_to_message_id is not None:
        params["reply_to_message_id"] = reply_to_message_id

    if reply_markup is not None:
        params["reply_markup"] = json_dumps(reply_markup.serialized, check_circular=False)

    if files:
        headers: dict = {}
        encoder = MultipartEncoder(files=files)
        headers["content-type"], body = encoder.encode()
        headers["content-length"] = len(body)
        return "POST", "sendDocument", headers, params, body
    else:
        return "GET", "sendDocument", None, params, None


def sendVideo(
    chat_id: Union[int, str],
    video: InputFile,
    *,
    duration: Optional[int] = None,
    width: Optional[int] = None,
    height: Optional[int] = None,
    thumb: Optional[InputFile] = None,
    caption: Optional[str] = None,
    parse_mode: Optional[ParseMode] = None,
    supports_streaming: Optional[bool] = None,
    disable_notification: Optional[bool] = None,
    reply_to_message_id: Optional[int] = None,
    reply_markup: Optional[Union[InlineKeyboardMarkup, ReplyKeyboardMarkup, ReplyKeyboardRemove, ForceReply]] = None
) -> EndpointCall:
    files: List[Tuple[bytes, bytes, bytes, bytes]] = []

    params: dict = {
        "chat_id": chat_id,
    }

    video("video", files, params, attach=None)

    if thumb is not None:
        thumb("thumb", files, params, attach="thumb")

    if duration is not None:
        params["duration"] = duration

    if width is not None:
        params["width"] = width

    if height is not None:
        params["height"] = height

    if caption is not None:
        params["caption"] = caption

    if parse_mode is not None:
        params["parse_mode"] = parse_mode.name

    if supports_streaming is not None:
        params["supports_streaming"] = supports_streaming

    if disable_notification is not None:
        params["disable_notification"] = disable_notification

    if reply_to_message_id is not None:
        params["reply_to_message_id"] = reply_to_message_id

    if reply_markup is not None:
        params["reply_markup"] = json_dumps(reply_markup.serialized, check_circular=False)

    if files:
        headers: dict = {}
        encoder = MultipartEncoder(files=files)
        headers["content-type"], body = encoder.encode()
        headers["content-length"] = len(body)
        return "POST", "sendVideo", headers, params, body
    else:
        return "GET", "sendVideo", None, params, None


def sendAnimation(
    chat_id: Union[int, str],
    animation: InputFile,
    *,
    duration: Optional[int] = None,
    width: Optional[int] = None,
    height: Optional[int] = None,
    thumb: Optional[InputFile] = None,
    caption: Optional[str] = None,
    parse_mode: Optional[ParseMode] = None,
    disable_notification: Optional[bool] = None,
    reply_to_message_id: Optional[int] = None,
    reply_markup: Optional[Union[InlineKeyboardMarkup, ReplyKeyboardMarkup, ReplyKeyboardRemove, ForceReply]] = None
) -> EndpointCall:
    files: List[Tuple[bytes, bytes, bytes, bytes]] = []

    params: dict = {
        "chat_id": chat_id,
    }

    animation("animation", files, params, attach=None)

    if thumb is not None:
        thumb("thumb", files, params, attach="thumb")

    if duration is not None:
        params["duration"] = duration

    if width is not None:
        params["width"] = width

    if height is not None:
        params["height"] = height

    if caption is not None:
        params["caption"] = caption

    if parse_mode is not None:
        params["parse_mode"] = parse_mode.name

    if disable_notification is not None:
        params["disable_notification"] = disable_notification

    if reply_to_message_id is not None:
        params["reply_to_message_id"] = reply_to_message_id

    if reply_markup is not None:
        params["reply_markup"] = json_dumps(reply_markup.serialized, check_circular=False)

    if files:
        headers: dict = {}
        encoder = MultipartEncoder(files=files)
        headers["content-type"], body = encoder.encode()
        headers["content-length"] = len(body)
        return "POST", "sendAnimation", headers, params, body
    else:
        return "GET", "sendAnimation", None, params, None


def sendVoice(
    chat_id: Union[int, str],
    voice: InputFile,
    *,
    caption: Optional[str] = None,
    parse_mode: Optional[ParseMode] = None,
    duration: Optional[int] = None,
    disable_notification: Optional[bool] = None,
    reply_to_message_id: Optional[int] = None,
    reply_markup: Optional[Union[InlineKeyboardMarkup, ReplyKeyboardMarkup, ReplyKeyboardRemove, ForceReply]] = None
) -> EndpointCall:
    files: List[Tuple[bytes, bytes, bytes, bytes]] = []

    params: dict = {
        "chat_id": chat_id,
    }

    voice("voice", files, params, attach=None)

    if caption is not None:
        params["caption"] = caption

    if parse_mode is not None:
        params["parse_mode"] = parse_mode.name

    if duration is not None:
        params["duration"] = duration

    if disable_notification is not None:
        params["disable_notification"] = disable_notification

    if reply_to_message_id is not None:
        params["reply_to_message_id"] = reply_to_message_id

    if reply_markup is not None:
        params["reply_markup"] = json_dumps(reply_markup.serialized, check_circular=False)

    if files:
        headers: dict = {}
        encoder = MultipartEncoder(files=files)
        headers["content-type"], body = encoder.encode()
        headers["content-length"] = len(body)
        return "POST", "sendVoice", headers, params, body
    else:
        return "GET", "sendVoice", None, params, None


def sendVideoNote(
    chat_id: Union[int, str],
    video_note: InputFile,
    *,
    duration: Optional[int] = None,
    length: Optional[int] = None,
    thumb: Optional[InputFile] = None,
    disable_notification: Optional[bool] = None,
    reply_to_message_id: Optional[int] = None,
    reply_markup: Optional[Union[InlineKeyboardMarkup, ReplyKeyboardMarkup, ReplyKeyboardRemove, ForceReply]] = None
) -> EndpointCall:
    files: List[Tuple[bytes, bytes, bytes, bytes]] = []

    params: dict = {
        "chat_id": chat_id,
    }

    video_note("video_note", files, params, attach=None)

    if thumb is not None:
        thumb("thumb", files, params, attach="thumb")

    if duration is not None:
        params["duration"] = duration

    if length is not None:
        params["length"] = length

    if disable_notification is not None:
        params["disable_notification"] = disable_notification

    if reply_to_message_id is not None:
        params["reply_to_message_id"] = reply_to_message_id

    if reply_markup is not None:
        params["reply_markup"] = json_dumps(reply_markup.serialized, check_circular=False)

    if files:
        headers: dict = {}
        encoder = MultipartEncoder(files=files)
        headers["content-type"], body = encoder.encode()
        headers["content-length"] = len(body)
        return "POST", "sendVideoNote", headers, params, body
    else:
        return "GET", "sendVideoNote", None, params, None


def sendLocation(
    chat_id: Union[int, str],
    latitude: float,
    longitude: float,
    *,
    live_period: Optional[int] = None,
    disable_notification: Optional[bool] = None,
    reply_to_message_id: Optional[int] = None,
    reply_markup: Optional[Union[InlineKeyboardMarkup, ReplyKeyboardMarkup, ReplyKeyboardRemove, ForceReply]] = None
) -> EndpointCall:
    params: dict = {
        "chat_id": chat_id,
        "latitude": latitude,
        "longitude": longitude,
    }

    if live_period is not None:
        params["live_period"] = live_period

    if disable_notification is not None:
        params["disable_notification"] = disable_notification

    if reply_to_message_id is not None:
        params["reply_to_message_id"] = reply_to_message_id

    if reply_markup is not None:
        params["reply_markup"] = json_dumps(reply_markup.serialized, check_circular=False)

    return "GET", "sendLocation", None, params, None


def editMessageLiveLocation(
    latitude: float,
    longitude: float,
    *,
    chat_id: Optional[Union[int, str]] = None,
    message_id: Optional[int] = None,
    inline_message_id: Optional[str] = None,
    reply_markup: Optional[InlineKeyboardMarkup] = None
) -> EndpointCall:
    params: dict = {
        "latitude": latitude,
        "longitude": longitude,
    }

    if chat_id is not None:
        params["chat_id"] = chat_id

    if message_id is not None:
        params["message_id"] = message_id

    if inline_message_id is not None:
        params["inline_message_id"] = inline_message_id

    if reply_markup is not None:
        params["reply_markup"] = json_dumps(reply_markup.serialized, check_circular=False)

    return "GET", "editMessageLiveLocation", None, params, None


def stopMessageLiveLocation(*,
    chat_id: Optional[Union[int, str]] = None,
    message_id: Optional[int] = None,
    inline_message_id: Optional[str] = None,
    reply_markup: Optional[InlineKeyboardMarkup] = None
) -> EndpointCall:
    params: dict = {}

    if chat_id is not None:
        params["chat_id"] = chat_id

    if message_id is not None:
        params["message_id"] = message_id

    if inline_message_id is not None:
        params["inline_message_id"] = inline_message_id

    if reply_markup is not None:
        params["reply_markup"] = json_dumps(reply_markup.serialized, check_circular=False)

    return "GET", "stopMessageLiveLocation", None, params, None


def sendVenue(
    chat_id: Union[int, str],
    latitude: float,
    longitude: float,
    title: str,
    address: str,
    *,
    foursquare_id: Optional[str] = None,
    foursquare_type: Optional[str] = None,
    disable_notification: Optional[bool] = None,
    reply_to_message_id: Optional[int] = None,
    reply_markup: Optional[Union[InlineKeyboardMarkup, ReplyKeyboardMarkup, ReplyKeyboardRemove, ForceReply]] = None
) -> EndpointCall:
    params: dict = {
        "chat_id": chat_id,
        "latitude": latitude,
        "longitude": longitude,
        "title": title,
        "address": address,
    }

    if foursquare_id is not None:
        params["foursquare_id"] = foursquare_id

    if foursquare_type is not None:
        params["foursquare_type"] = foursquare_type

    if disable_notification is not None:
        params["disable_notification"] = disable_notification

    if reply_to_message_id is not None:
        params["reply_to_message_id"] = reply_to_message_id

    if reply_markup is not None:
        params["reply_markup"] = json_dumps(reply_markup.serialized, check_circular=False)

    return "GET", "sendVenue", None, params, None


def sendContact(
    chat_id: Union[int, str],
    phone_number: str,
    first_name: str,
    *,
    last_name: Optional[str] = None,
    vcard: Optional[str] = None,
    disable_notification: Optional[bool] = None,
    reply_to_message_id: Optional[int] = None,
    reply_markup: Optional[Union[InlineKeyboardMarkup, ReplyKeyboardMarkup, ReplyKeyboardRemove, ForceReply]] = None
) -> EndpointCall:
    params: dict = {
        "chat_id": chat_id,
        "phone_number": phone_number,
        "first_name": first_name,
    }

    if last_name is not None:
        params["last_name"] = last_name

    if vcard is not None:
        params["vcard"] = vcard

    if disable_notification is not None:
        params["disable_notification"] = disable_notification

    if reply_to_message_id is not None:
        params["reply_to_message_id"] = reply_to_message_id

    if reply_markup is not None:
        params["reply_markup"] = json_dumps(reply_markup.serialized, check_circular=False)

    return "GET", "sendContact", None, params, None


def sendPoll(
    chat_id: Union[int, str],
    question: str,
    options: List[str],
    *,
    is_anonymous: Optional[bool] = None,
    type: Optional[str] = None,
    allows_multiple_answers: Optional[bool] = None,
    correct_option_id: Optional[int] = None,
    explanation: Optional[str] = None,
    explanation_parse_mode: Optional[str] = None,
    open_period: Optional[int] = None,
    close_date: Optional[int] = None,
    is_closed: Optional[bool] = None,
    disable_notification: Optional[bool] = None,
    reply_to_message_id: Optional[int] = None,
    reply_markup: Optional[Union[InlineKeyboardMarkup, ReplyKeyboardMarkup, ReplyKeyboardRemove, ForceReply]] = None
) -> EndpointCall:
    params: dict = {
        "chat_id": chat_id,
        "question": question,
        "options": options,
    }

    if is_anonymous is not None:
        params["is_anonymous"] = is_anonymous

    if type is not None:
        params["type"] = type

    if allows_multiple_answers is not None:
        params["allows_multiple_answers"] = allows_multiple_answers

    if correct_option_id is not None:
        params["correct_option_id"] = correct_option_id

    if explanation is not None:
        params["explanation"] = explanation

    if explanation_parse_mode is not None:
        params["explanation_parse_mode"] = explanation_parse_mode

    if open_period is not None:
        params["open_period"] = open_period

    if close_date is not None:
        params["close_date"] = close_date

    if is_closed is not None:
        params["is_closed"] = is_closed

    if disable_notification is not None:
        params["disable_notification"] = disable_notification

    if reply_to_message_id is not None:
        params["reply_to_message_id"] = reply_to_message_id

    if reply_markup is not None:
        params["reply_markup"] = json_dumps(reply_markup.serialized, check_circular=False)

    return "GET", "sendPoll", None, params, None


def sendDice(
    chat_id: Union[int, str],
    *,
    emoji: Optional[str] = None,
    disable_notification: Optional[bool] = None,
    reply_to_message_id: Optional[int] = None,
    reply_markup: Optional[Union[InlineKeyboardMarkup, ReplyKeyboardMarkup, ReplyKeyboardRemove, ForceReply]] = None
) -> EndpointCall:
    params: dict = {
        "chat_id": chat_id,
    }

    if emoji is not None:
        params["emoji"] = emoji

    if disable_notification is not None:
        params["disable_notification"] = disable_notification

    if reply_to_message_id is not None:
        params["reply_to_message_id"] = reply_to_message_id

    if reply_markup is not None:
        params["reply_markup"] = json_dumps(reply_markup.serialized, check_circular=False)

    return "GET", "sendDice", None, params, None


def sendChatAction(
    chat_id: Union[int, str],
    action: str
) -> EndpointCall:
    params: dict = {
        "chat_id": chat_id,
        "action": action,
    }

    return "GET", "sendChatAction", None, params, None


def getUserProfilePhotos(
    user_id: int,
    *,
    offset: Optional[int] = None,
    limit: Optional[int] = None
) -> EndpointCall:
    params: dict = {
        "user_id": user_id,
    }

    if offset is not None:
        params["offset"] = offset

    if limit is not None:
        params["limit"] = limit

    return "GET", "getUserProfilePhotos", None, params, None


def getFile(
    file_id: str
) -> EndpointCall:
    params: dict = {
        "file_id": file_id,
    }

    return "GET", "getFile", None, params, None


def kickChatMember(
    chat_id: Union[int, str],
    user_id: int,
    *,
    until_date: Optional[int] = None
) -> EndpointCall:
    params: dict = {
        "chat_id": chat_id,
        "user_id": user_id,
    }

    if until_date is not None:
        params["until_date"] = until_date

    return "GET", "kickChatMember", None, params, None


def unbanChatMember(
    chat_id: Union[int, str],
    user_id: int
) -> EndpointCall:
    params: dict = {
        "chat_id": chat_id,
        "user_id": user_id,
    }

    return "GET", "unbanChatMember", None, params, None


def restrictChatMember(
    chat_id: Union[int, str],
    user_id: int,
    permissions: ChatPermissions,
    *,
    until_date: Optional[int] = None
) -> EndpointCall:
    params: dict = {
        "chat_id": chat_id,
        "user_id": user_id,
        "permissions": json_dumps(permissions, check_circular=False),
    }

    if until_date is not None:
        params["until_date"] = until_date

    return "GET", "restrictChatMember", None, params, None


def promoteChatMember(
    chat_id: Union[int, str],
    user_id: int,
    *,
    can_change_info: Optional[bool] = None,
    can_post_messages: Optional[bool] = None,
    can_edit_messages: Optional[bool] = None,
    can_delete_messages: Optional[bool] = None,
    can_invite_users: Optional[bool] = None,
    can_restrict_members: Optional[bool] = None,
    can_pin_messages: Optional[bool] = None,
    can_promote_members: Optional[bool] = None
) -> EndpointCall:
    params: dict = {
        "chat_id": chat_id,
        "user_id": user_id,
    }

    if can_change_info is not None:
        params["can_change_info"] = can_change_info

    if can_post_messages is not None:
        params["can_post_messages"] = can_post_messages

    if can_edit_messages is not None:
        params["can_edit_messages"] = can_edit_messages

    if can_delete_messages is not None:
        params["can_delete_messages"] = can_delete_messages

    if can_invite_users is not None:
        params["can_invite_users"] = can_invite_users

    if can_restrict_members is not None:
        params["can_restrict_members"] = can_restrict_members

    if can_pin_messages is not None:
        params["can_pin_messages"] = can_pin_messages

    if can_promote_members is not None:
        params["can_promote_members"] = can_promote_members

    return "GET", "promoteChatMember", None, params, None


def setChatAdministratorCustomTitle(
    chat_id: Union[int, str],
    user_id: int,
    custom_title: str
) -> EndpointCall:
    params: dict = {
        "chat_id": chat_id,
        "user_id": user_id,
        "custom_title": custom_title,
    }

    return "GET", "setChatAdministratorCustomTitle", None, params, None


def setChatPermissions(
    chat_id: Union[int, str],
    permissions: ChatPermissions
) -> EndpointCall:
    params: dict = {
        "chat_id": chat_id,
        "permissions": json_dumps(permissions, check_circular=False),
    }

    return "GET", "setChatPermissions", None, params, None


def exportChatInviteLink(
    chat_id: Union[int, str]
) -> EndpointCall:
    params: dict = {
        "chat_id": chat_id,
    }

    return "GET", "exportChatInviteLink", None, params, None


def setChatPhoto(
    chat_id: Union[int, str],
    photo: InputFile
) -> EndpointCall:
    files: List[Tuple[bytes, bytes, bytes, bytes]] = []

    params: dict = {
        "chat_id": chat_id,
    }

    photo("photo", files, params, attach=None)

    if files:
        headers: dict = {}
        encoder = MultipartEncoder(files=files)
        headers["content-type"], body = encoder.encode()
        headers["content-length"] = len(body)
        return "POST", "setChatPhoto", headers, params, body
    else:
        return "GET", "setChatPhoto", None, params, None


def deleteChatPhoto(
    chat_id: Union[int, str]
) -> EndpointCall:
    params: dict = {
        "chat_id": chat_id,
    }

    return "GET", "deleteChatPhoto", None, params, None


def setChatTitle(
    chat_id: Union[int, str],
    title: str
) -> EndpointCall:
    params: dict = {
        "chat_id": chat_id,
        "title": title,
    }

    return "GET", "setChatTitle", None, params, None


def setChatDescription(
    chat_id: Union[int, str],
    *,
    description: Optional[str] = None
) -> EndpointCall:
    params: dict = {
        "chat_id": chat_id,
    }

    if description is not None:
        params["description"] = description

    return "GET", "setChatDescription", None, params, None


def pinChatMessage(
    chat_id: Union[int, str],
    message_id: int,
    *,
    disable_notification: Optional[bool] = None
) -> EndpointCall:
    params: dict = {
        "chat_id": chat_id,
        "message_id": message_id,
    }

    if disable_notification is not None:
        params["disable_notification"] = disable_notification

    return "GET", "pinChatMessage", None, params, None


def unpinChatMessage(
    chat_id: Union[int, str]
) -> EndpointCall:
    params: dict = {
        "chat_id": chat_id,
    }

    return "GET", "unpinChatMessage", None, params, None


def leaveChat(
    chat_id: Union[int, str]
) -> EndpointCall:
    params: dict = {
        "chat_id": chat_id,
    }

    return "GET", "leaveChat", None, params, None


def getChat(
    chat_id: Union[int, str]
) -> EndpointCall:
    params: dict = {
        "chat_id": chat_id,
    }

    return "GET", "getChat", None, params, None


def getChatAdministrators(
    chat_id: Union[int, str]
) -> EndpointCall:
    params: dict = {
        "chat_id": chat_id,
    }

    return "GET", "getChatAdministrators", None, params, None


def getChatMembersCount(
    chat_id: Union[int, str]
) -> EndpointCall:
    params: dict = {
        "chat_id": chat_id,
    }

    return "GET", "getChatMembersCount", None, params, None


def getChatMember(
    chat_id: Union[int, str],
    user_id: int
) -> EndpointCall:
    params: dict = {
        "chat_id": chat_id,
        "user_id": user_id,
    }

    return "GET", "getChatMember", None, params, None


def setChatStickerSet(
    chat_id: Union[int, str],
    sticker_set_name: str
) -> EndpointCall:
    params: dict = {
        "chat_id": chat_id,
        "sticker_set_name": sticker_set_name,
    }

    return "GET", "setChatStickerSet", None, params, None


def deleteChatStickerSet(
    chat_id: Union[int, str]
) -> EndpointCall:
    params: dict = {
        "chat_id": chat_id,
    }

    return "GET", "deleteChatStickerSet", None, params, None


def answerCallbackQuery(
    callback_query_id: str,
    *,
    text: Optional[str] = None,
    show_alert: Optional[bool] = None,
    url: Optional[str] = None,
    cache_time: Optional[int] = None
) -> EndpointCall:
    params: dict = {
        "callback_query_id": callback_query_id,
    }

    if text is not None:
        params["text"] = text

    if show_alert is not None:
        params["show_alert"] = show_alert

    if url is not None:
        params["url"] = url

    if cache_time is not None:
        params["cache_time"] = cache_time

    return "GET", "answerCallbackQuery", None, params, None


def setMyCommands(
    commands: List[BotCommand]
) -> EndpointCall:
    params: dict = {
        "commands": json_dumps(commands, check_circular=False),
    }

    return "GET", "setMyCommands", None, params, None


def getMyCommands() -> EndpointCall:
    return "GET", "getMyCommands", None, None, None


def editMessageText(
    text: str,
    *,
    chat_id: Optional[Union[int, str]] = None,
    message_id: Optional[int] = None,
    inline_message_id: Optional[str] = None,
    parse_mode: Optional[ParseMode] = None,
    disable_web_page_preview: Optional[bool] = None,
    reply_markup: Optional[InlineKeyboardMarkup] = None
) -> EndpointCall:
    params: dict = {
        "text": text,
    }

    if chat_id is not None:
        params["chat_id"] = chat_id

    if message_id is not None:
        params["message_id"] = message_id

    if inline_message_id is not None:
        params["inline_message_id"] = inline_message_id

    if parse_mode is not None:
        params["parse_mode"] = parse_mode.name

    if disable_web_page_preview is not None:
        params["disable_web_page_preview"] = disable_web_page_preview

    if reply_markup is not None:
        params["reply_markup"] = json_dumps(reply_markup.serialized, check_circular=False)

    return "GET", "editMessageText", None, params, None


def editMessageCaption(*,
    chat_id: Optional[Union[int, str]] = None,
    message_id: Optional[int] = None,
    inline_message_id: Optional[str] = None,
    caption: Optional[str] = None,
    parse_mode: Optional[ParseMode] = None,
    reply_markup: Optional[InlineKeyboardMarkup] = None
) -> EndpointCall:
    params: dict = {}

    if chat_id is not None:
        params["chat_id"] = chat_id

    if message_id is not None:
        params["message_id"] = message_id

    if inline_message_id is not None:
        params["inline_message_id"] = inline_message_id

    if caption is not None:
        params["caption"] = caption

    if parse_mode is not None:
        params["parse_mode"] = parse_mode.name

    if reply_markup is not None:
        params["reply_markup"] = json_dumps(reply_markup.serialized, check_circular=False)

    return "GET", "editMessageCaption", None, params, None


def editMessageReplyMarkup(*,
    chat_id: Optional[Union[int, str]] = None,
    message_id: Optional[int] = None,
    inline_message_id: Optional[str] = None,
    reply_markup: Optional[InlineKeyboardMarkup] = None
) -> EndpointCall:
    params: dict = {}

    if chat_id is not None:
        params["chat_id"] = chat_id

    if message_id is not None:
        params["message_id"] = message_id

    if inline_message_id is not None:
        params["inline_message_id"] = inline_message_id

    if reply_markup is not None:
        params["reply_markup"] = json_dumps(reply_markup.serialized, check_circular=False)

    return "GET", "editMessageReplyMarkup", None, params, None


def stopPoll(
    chat_id: Union[int, str],
    message_id: int,
    *,
    reply_markup: Optional[InlineKeyboardMarkup] = None
) -> EndpointCall:
    params: dict = {
        "chat_id": chat_id,
        "message_id": message_id,
    }

    if reply_markup is not None:
        params["reply_markup"] = json_dumps(reply_markup.serialized, check_circular=False)

    return "GET", "stopPoll", None, params, None


def deleteMessage(
    chat_id: Union[int, str],
    message_id: int
) -> EndpointCall:
    params: dict = {
        "chat_id": chat_id,
        "message_id": message_id,
    }

    return "GET", "deleteMessage", None, params, None


def sendSticker(
    chat_id: Union[int, str],
    sticker: InputFile,
    *,
    disable_notification: Optional[bool] = None,
    reply_to_message_id: Optional[int] = None,
    reply_markup: Optional[Union[InlineKeyboardMarkup, ReplyKeyboardMarkup, ReplyKeyboardRemove, ForceReply]] = None
) -> EndpointCall:
    files: List[Tuple[bytes, bytes, bytes, bytes]] = []

    params: dict = {
        "chat_id": chat_id,
    }

    sticker("sticker", files, params, attach=None)

    if disable_notification is not None:
        params["disable_notification"] = disable_notification

    if reply_to_message_id is not None:
        params["reply_to_message_id"] = reply_to_message_id

    if reply_markup is not None:
        params["reply_markup"] = json_dumps(reply_markup.serialized, check_circular=False)

    if files:
        headers: dict = {}
        encoder = MultipartEncoder(files=files)
        headers["content-type"], body = encoder.encode()
        headers["content-length"] = len(body)
        return "POST", "sendSticker", headers, params, body
    else:
        return "GET", "sendSticker", None, params, None


def getStickerSet(
    name: str
) -> EndpointCall:
    params: dict = {
        "name": name,
    }

    return "GET", "getStickerSet", None, params, None


def uploadStickerFile(
    user_id: int,
    png_sticker: InputFile
) -> EndpointCall:
    files: List[Tuple[bytes, bytes, bytes, bytes]] = []

    params: dict = {
        "user_id": user_id,
    }

    png_sticker("png_sticker", files, params, attach=None)

    if files:
        headers: dict = {}
        encoder = MultipartEncoder(files=files)
        headers["content-type"], body = encoder.encode()
        headers["content-length"] = len(body)
        return "POST", "uploadStickerFile", headers, params, body
    else:
        return "GET", "uploadStickerFile", None, params, None


def createNewStickerSet(
    user_id: int,
    name: str,
    title: str,
    emojis: str,
    *,
    png_sticker: Optional[InputFile] = None,
    tgs_sticker: Optional[InputFile] = None,
    contains_masks: Optional[bool] = None,
    mask_position: Optional[MaskPosition] = None
) -> EndpointCall:
    files: List[Tuple[bytes, bytes, bytes, bytes]] = []

    params: dict = {
        "user_id": user_id,
        "name": name,
        "title": title,
        "emojis": emojis,
    }

    if png_sticker is not None:
        png_sticker("png_sticker", files, params, attach=None)

    if tgs_sticker is not None:
        tgs_sticker("tgs_sticker", files, params, attach=None)

    if contains_masks is not None:
        params["contains_masks"] = contains_masks

    if mask_position is not None:
        params["mask_position"] = json_dumps(mask_position, check_circular=False)

    if files:
        headers: dict = {}
        encoder = MultipartEncoder(files=files)
        headers["content-type"], body = encoder.encode()
        headers["content-length"] = len(body)
        return "POST", "createNewStickerSet", headers, params, body
    else:
        return "GET", "createNewStickerSet", None, params, None


def addStickerToSet(
    user_id: int,
    name: str,
    emojis: str,
    *,
    png_sticker: Optional[InputFile] = None,
    tgs_sticker: Optional[InputFile] = None,
    mask_position: Optional[MaskPosition] = None
) -> EndpointCall:
    files: List[Tuple[bytes, bytes, bytes, bytes]] = []

    params: dict = {
        "user_id": user_id,
        "name": name,
        "emojis": emojis,
    }

    if png_sticker is not None:
        png_sticker("png_sticker", files, params, attach=None)

    if tgs_sticker is not None:
        tgs_sticker("tgs_sticker", files, params, attach=None)

    if mask_position is not None:
        params["mask_position"] = json_dumps(mask_position, check_circular=False)

    if files:
        headers: dict = {}
        encoder = MultipartEncoder(files=files)
        headers["content-type"], body = encoder.encode()
        headers["content-length"] = len(body)
        return "POST", "addStickerToSet", headers, params, body
    else:
        return "GET", "addStickerToSet", None, params, None


def setStickerPositionInSet(
    sticker: InputFile,
    position: int
) -> EndpointCall:
    files: List[Tuple[bytes, bytes, bytes, bytes]] = []

    params: dict = {
        "position": position,
    }

    sticker("sticker", files, params, attach=None)

    if files:
        headers: dict = {}
        encoder = MultipartEncoder(files=files)
        headers["content-type"], body = encoder.encode()
        headers["content-length"] = len(body)
        return "POST", "setStickerPositionInSet", headers, params, body
    else:
        return "GET", "setStickerPositionInSet", None, params, None


def deleteStickerFromSet(
    sticker: InputFile
) -> EndpointCall:
    files: List[Tuple[bytes, bytes, bytes, bytes]] = []

    params: dict = {

    }

    sticker("sticker", files, params, attach=None)

    if files:
        headers: dict = {}
        encoder = MultipartEncoder(files=files)
        headers["content-type"], body = encoder.encode()
        headers["content-length"] = len(body)
        return "POST", "deleteStickerFromSet", headers, params, body
    else:
        return "GET", "deleteStickerFromSet", None, params, None


def setStickerSetThumb(
    name: str,
    user_id: int,
    *,
    thumb: Optional[InputFile] = None
) -> EndpointCall:
    files: List[Tuple[bytes, bytes, bytes, bytes]] = []

    params: dict = {
        "name": name,
        "user_id": user_id,
    }

    if thumb is not None:
        thumb("thumb", files, params, attach="thumb")

    if files:
        headers: dict = {}
        encoder = MultipartEncoder(files=files)
        headers["content-type"], body = encoder.encode()
        headers["content-length"] = len(body)
        return "POST", "setStickerSetThumb", headers, params, body
    else:
        return "GET", "setStickerSetThumb", None, params, None


def answerInlineQuery(
    inline_query_id: str,
    results: List[InlineQueryResult],
    *,
    cache_time: Optional[int] = None,
    is_personal: Optional[bool] = None,
    next_offset: Optional[str] = None,
    switch_pm_text: Optional[str] = None,
    switch_pm_parameter: Optional[str] = None
) -> EndpointCall:
    params: dict = {
        "inline_query_id": inline_query_id,
        "results": json_dumps(results, check_circular=False),
    }

    if cache_time is not None:
        params["cache_time"] = cache_time

    if is_personal is not None:
        params["is_personal"] = is_personal

    if next_offset is not None:
        params["next_offset"] = next_offset

    if switch_pm_text is not None:
        params["switch_pm_text"] = switch_pm_text

    if switch_pm_parameter is not None:
        params["switch_pm_parameter"] = switch_pm_parameter

    return "GET", "answerInlineQuery", None, params, None


def sendInvoice(
    chat_id: int,
    title: str,
    description: str,
    payload: str,
    provider_token: str,
    start_parameter: str,
    currency: str,
    prices: List[LabeledPrice],
    *,
    provider_data: Optional[str] = None,
    photo_url: Optional[str] = None,
    photo_size: Optional[int] = None,
    photo_width: Optional[int] = None,
    photo_height: Optional[int] = None,
    need_name: Optional[bool] = None,
    need_phone_number: Optional[bool] = None,
    need_email: Optional[bool] = None,
    need_shipping_address: Optional[bool] = None,
    send_phone_number_to_provider: Optional[bool] = None,
    send_email_to_provider: Optional[bool] = None,
    is_flexible: Optional[bool] = None,
    disable_notification: Optional[bool] = None,
    reply_to_message_id: Optional[int] = None,
    reply_markup: Optional[InlineKeyboardMarkup] = None
) -> EndpointCall:
    params: dict = {
        "chat_id": chat_id,
        "title": title,
        "description": description,
        "payload": payload,
        "provider_token": provider_token,
        "start_parameter": start_parameter,
        "currency": currency,
        "prices": json_dumps(prices, check_circular=False),
    }

    if provider_data is not None:
        params["provider_data"] = provider_data

    if photo_url is not None:
        params["photo_url"] = photo_url

    if photo_size is not None:
        params["photo_size"] = photo_size

    if photo_width is not None:
        params["photo_width"] = photo_width

    if photo_height is not None:
        params["photo_height"] = photo_height

    if need_name is not None:
        params["need_name"] = need_name

    if need_phone_number is not None:
        params["need_phone_number"] = need_phone_number

    if need_email is not None:
        params["need_email"] = need_email

    if need_shipping_address is not None:
        params["need_shipping_address"] = need_shipping_address

    if send_phone_number_to_provider is not None:
        params["send_phone_number_to_provider"] = send_phone_number_to_provider

    if send_email_to_provider is not None:
        params["send_email_to_provider"] = send_email_to_provider

    if is_flexible is not None:
        params["is_flexible"] = is_flexible

    if disable_notification is not None:
        params["disable_notification"] = disable_notification

    if reply_to_message_id is not None:
        params["reply_to_message_id"] = reply_to_message_id

    if reply_markup is not None:
        params["reply_markup"] = json_dumps(reply_markup.serialized, check_circular=False)

    return "GET", "sendInvoice", None, params, None


def answerShippingQuery(
    shipping_query_id: str,
    ok: bool,
    *,
    shipping_options: Optional[List[ShippingOption]] = None,
    error_message: Optional[str] = None
) -> EndpointCall:
    params: dict = {
        "shipping_query_id": shipping_query_id,
        "ok": ok,
    }

    if shipping_options is not None:
        params["shipping_options"] = json_dumps(shipping_options, check_circular=False)

    if error_message is not None:
        params["error_message"] = error_message

    return "GET", "answerShippingQuery", None, params, None


def answerPreCheckoutQuery(
    pre_checkout_query_id: str,
    ok: bool,
    *,
    error_message: Optional[str] = None
) -> EndpointCall:
    params: dict = {
        "pre_checkout_query_id": pre_checkout_query_id,
        "ok": ok,
    }

    if error_message is not None:
        params["error_message"] = error_message

    return "GET", "answerPreCheckoutQuery", None, params, None


def setPassportDataErrors(
    user_id: int,
    errors: List[PassportElementError]
) -> EndpointCall:
    params: dict = {
        "user_id": user_id,
        "errors": json_dumps(errors, check_circular=False),
    }

    return "GET", "setPassportDataErrors", None, params, None


def sendGame(
    chat_id: int,
    game_short_name: str,
    *,
    disable_notification: Optional[bool] = None,
    reply_to_message_id: Optional[int] = None,
    reply_markup: Optional[InlineKeyboardMarkup] = None
) -> EndpointCall:
    params: dict = {
        "chat_id": chat_id,
        "game_short_name": game_short_name,
    }

    if disable_notification is not None:
        params["disable_notification"] = disable_notification

    if reply_to_message_id is not None:
        params["reply_to_message_id"] = reply_to_message_id

    if reply_markup is not None:
        params["reply_markup"] = json_dumps(reply_markup.serialized, check_circular=False)

    return "GET", "sendGame", None, params, None


def setGameScore(
    user_id: int,
    score: int,
    *,
    force: Optional[bool] = None,
    disable_edit_message: Optional[bool] = None,
    chat_id: Optional[int] = None,
    message_id: Optional[int] = None,
    inline_message_id: Optional[str] = None
) -> EndpointCall:
    params: dict = {
        "user_id": user_id,
        "score": score,
    }

    if force is not None:
        params["force"] = force

    if disable_edit_message is not None:
        params["disable_edit_message"] = disable_edit_message

    if chat_id is not None:
        params["chat_id"] = chat_id

    if message_id is not None:
        params["message_id"] = message_id

    if inline_message_id is not None:
        params["inline_message_id"] = inline_message_id

    return "GET", "setGameScore", None, params, None


def getGameHighScores(
    user_id: int,
    *,
    chat_id: Optional[int] = None,
    message_id: Optional[int] = None,
    inline_message_id: Optional[str] = None
) -> EndpointCall:
    params: dict = {
        "user_id": user_id,
    }

    if chat_id is not None:
        params["chat_id"] = chat_id

    if message_id is not None:
        params["message_id"] = message_id

    if inline_message_id is not None:
        params["inline_message_id"] = inline_message_id

    return "GET", "getGameHighScores", None, params, None


