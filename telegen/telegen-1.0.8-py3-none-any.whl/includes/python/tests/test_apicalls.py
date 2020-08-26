from asyncio import gather as asyncio_gather, get_event_loop
from inspect import currentframe
from json import loads as json_loads
from os import environ
from os.path import abspath, basename, dirname
from unittest import IsolatedAsyncioTestCase
from urllib.parse import urlencode

from telegen_definitions import (
    ForceReply,
    InlineKeyboardMarkup,
    InputFile,
    InputMediaPhoto,
    ReplyKeyboardRemove,
    ReplyKeyboardMarkup,
    editMessageMedia,
    sendDocument,
    sendMediaGroup,
    sendMessage,
    sendPhoto,
)

from ._http import HttpConnectionPool


token = environ.get("TELEGRAM_TOKEN")
chat_id = environ.get("TELEGRAM_CHAT_ID")


def InputFile_from_path(path):
    with open(path, "rb") as f:
        content = f.read()
    return InputFile(basename(path), body=content)


current_dir = dirname(abspath(__file__))
document = InputFile_from_path(f"{current_dir}/document.pdf")
photo = InputFile_from_path(f"{current_dir}/photo.jpg")
photo2 = InputFile_from_path(f"{current_dir}/photo2.jpg")
photo_url = InputFile("https://placekitten.com/200/300")


class ApiCallsCase(IsolatedAsyncioTestCase):
    async def test_calls(self):
        pool = HttpConnectionPool("api.telegram.org", loop=get_event_loop(), size=5)

        async def telegram_req(req):
            # "GET", "sendMessage", None, params, None
            method, endpoint, headers, params, body = req

            url = f"bot{token}/{endpoint}"
            if params:
                generator = [(k, v) for k, v in params.items() if v]
                url = url + "?" + urlencode(generator)

            try:
                res = await pool.request(url, method=method, headers=headers, body=body)
            except Exception as e:
                print(e)
                print(method, endpoint, headers, params, body)
                raise e

            res = json_loads(res.decode())
            try:
                assert res["ok"] == True
            except Exception as e:
                print(method, endpoint, headers, params, body)
                print(res)
                raise e

            return res

        async def test_sendMessage():
            req = sendMessage(chat_id, "Test!")
            res = await telegram_req(req)

        async def test_sendDocument():
            req = sendDocument(chat_id, document, thumb=photo)
            res = await telegram_req(req)

        async def test_sendPhotoUrl():
            req = sendPhoto(chat_id, photo_url)
            res = await telegram_req(req)

        async def test_editMessageMedia():
            req = sendPhoto(chat_id, photo_url)
            res = await telegram_req(req)

            new_photo: InputMediaPhoto = {"media": photo2, "type": "photo"}
            req = editMessageMedia(new_photo, chat_id=chat_id, message_id=res["result"]["message_id"])
            res = await telegram_req(req)

        async def test_editMessageMediaUrl():
            req = sendPhoto(chat_id, photo)
            res = await telegram_req(req)

            new_photo: InputMediaPhoto = {"media": photo_url, "type": "photo"}
            req = editMessageMedia(new_photo, chat_id=chat_id, message_id=res["result"]["message_id"])
            res = await telegram_req(req)

        async def test_sendMediaGroup():
            photos: List[InputMediaPhoto] = [
                {"media": photo, "type": "photo"},
                {"media": photo2, "type": "photo"},
                {"media": photo_url, "type": "photo"},
            ]

            req = sendMediaGroup(chat_id, photos)
            res = await telegram_req(req)

        async def test_InlineKeyboardMarkup():
            keyboard = InlineKeyboardMarkup().callback_data("test", "test")
            req = sendMessage(chat_id, "Test", reply_markup=keyboard)
            res = await telegram_req(req)

        async def test_ReplyKeyboard():
            keyboard = ReplyKeyboardMarkup().add_button("Test").add_row().add_button("Test2").add_button("Test3")
            req = sendMessage(chat_id, "Test", reply_markup=keyboard)
            res = await telegram_req(req)

            req = sendMessage(chat_id, "Test", reply_markup=ReplyKeyboardRemove())
            res = await telegram_req(req)

        async def test_ForceReply():
            req = sendMessage(chat_id, "Test", reply_markup=ForceReply().selective())
            res = await telegram_req(req)

        frame = currentframe()
        test_fns = [val() for name, val in frame.f_locals.items() if name.startswith("test_")]

        await asyncio_gather(*test_fns)

        pool.stop()
