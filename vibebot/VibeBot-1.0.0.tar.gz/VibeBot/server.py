#!/usr/bin/env python3

"""Server

The Flask API for the bot

Author(s)
---------
Daniel Gisolfi <Daniel.Gisolfi1@marist.edu>
"""

import os
import logging

import markdown
from flask import Flask, request

from VibeBot.bot import Bot

# Create instance of flask
server = Flask(__name__)
server.config["JSON_SORT_KEYS"] = False
logging.basicConfig(level=logging.DEBUG)


name = os.getenv("BOT_NAME", None)
bot_id = os.getenv("BOT_ID", None)
group_id = os.getenv("GROUP_ID", None)
api_token = os.getenv("API_TOKEN", None)

# setup bot
bot = Bot(name, bot_id, group_id, api_token)


@server.route("/", methods=["GET"])
def index():
    try:
        markdown_file = open("README.md", "r")
        content = markdown_file.read()
        # Convert to HTML
        return markdown.markdown(content), 200
    except:
        return "Project Documentation Not found", 404


@server.route("/vibe", methods=["POST"])
def vibe():
    data = request.get_json()
    if data is not None:
        if bot.checkForMention(data["text"]):
            if bot.member != None:
                if data["user_id"] == bot.member["user_id"]:
                    print("{bot.member['name']} passed the vibe check")
                    bot.stopVibeCheck()
            else:
                bot.sendMessage("Leave me be, I'm trying to monitor these vibes.")

        return "OK", 200
    else:
        return "No Message Provided", 404
