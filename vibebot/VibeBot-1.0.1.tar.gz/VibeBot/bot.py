#!/usr/bin/env python3

"""The Vibe Check Bot

Author(s)
---------
Daniel Gisolfi <Daniel.Gisolfi1@marist.edu>
"""

import os
import re
import json
import threading
from random import randint, randrange
from datetime import datetime, timedelta

import requests

from VibeBot.utils.io import jsonToDict


class Bot:
    def __init__(self, name, bot_id, group_id, api_token):
        self.name = name
        self.bot_id = bot_id
        self.group_id = group_id
        self.api_token = api_token
        self.api_base_url = "https://api.groupme.com/v3"
        self.api_session = requests.session()
        self.member_responded = False
        self.member = None
        self.images = jsonToDict("./VibeBot/urls.json")
        self.startThread()

    def startThread(self):
        """ Starts a new thread to countdown to a vibe check """
        delay = self.vibeTime()
        vibe_check_time = datetime.now() + timedelta(seconds=delay)
        print(f"VibeBot => Current Time: {datetime.now()}", flush=True)
        print(f"VibeBot => Next Vibe check in: {delay} seconds.", flush=True)
        print(f"VibeBot => Vibe check will occur at: {vibe_check_time} seconds.",flush=True)
        threading.Timer(delay, self.startVibeCheck).start()

    def sendMessage(self, msg, picture_url=None) -> requests.Response:
        """Send a message from the bot to its assigned group.
        Args:
            msg (str): message to be sent to group
        Returns:
            requests.Response
        """
        # set parameters for post request
        params = {"bot_id": self.bot_id, "text": msg}
        if picture_url:
            params.update({"picture_url": picture_url})
        # send the request to the api and get the results in the response var
        response = self.api_session.post(
            f"{self.api_base_url}/bots/post", params=params
        )
        return response

    def getMessages(self) -> requests.Response:
        """Get all messages for the bot's group chat.
        Args:
            none
        Returns:
            requests.Response
        """
        # authenticate the request with the api token
        params = {"token": self.api_token}
        # get the messages for the bot's group
        response = self.api_session.post(
            f"{self.api_base_url}/groups/{self.group_id}/messages", params=params
        )
        return response

    def checkForMention(self, msg:str) -> bool:
        """Checks the recent messages of the bots group for instances of its name
        Args:
            msg (str): message sent in group chat
        Returns:
            boolean: a value denoting if the bot was mentioned or not
        """
        return re.match(r".*@" + self.name.lower() + r".*", msg.lower())

    def removeMention(self, msg:str) -> str:
        """Checks the recent messages of the bots group for instances of its name
        Args:
            msg (str): message sent in group chat
        Returns:
            msg (str): a messaged with the '@<bot_name>' removed
        """
        return re.sub(f"@{self.name}", "", msg)

    def vibeTime(self) -> int:
        """Creates a random time in the future for a vibe check to occur
     
        Returns:
            int : the number of seconds till the next vibe check
        """
        s = datetime.now() + timedelta(hours=24)
        e = s + timedelta(hours=48)
        d = self.randomDate(s, e) - datetime.now()
        # 86400 is 24 hours in seconds. We start our time delta at a
        # min of 24 hours so we need to account for that here
        return d.seconds + d.days * 86400

    def randomDate(self, start, end) -> datetime:
        """This function will return a random datetime between two datetime objects.
        Args:
            start (datetime): the min datetime
            end (datetime): the max datetime
        Returns:
            datetime : a random date between the start and end
        """
        delta = end - start
        int_delta = (delta.days * 24 * 60 * 60) + delta.seconds
        random_second = randrange(int_delta)
        return start + timedelta(seconds=random_second)

    def getMembers(self) -> dict:
        """Gets the members of a group

        Returns:
            dict : the members of the group
        """
        members = None
        params = {"token": self.api_token}
        # get the messages for the bot's group
        response = self.api_session.get(
            f"{self.api_base_url}/groups/{self.group_id}", params=params
        )

        if response.status_code == 200:
            members = response.json()["response"]["members"]

        return members

    def pickMember(self, members: dict) -> dict:
        """Returns a random group member

        Args:
            members (dict): the full dict of members

        Returns:
            [dict]: a single sub dict of the members
        """
        return members[randint(0, len(members) - 1)]

    def startVibeCheck(self):
        """Starts a vibe check and a thread to handle it """
        members = self.getMembers()
        if members != None:
            self.member = self.pickMember(members)
            self.member_responded = False
            msg = (
                f"@{self.member['name']} Vibe Check! Please tell me your current vibe. (remember to at me) "
                + "If you fail to do so I'll have to remove you from the group for bringing down the vibe"
            )

            pic = randint(0, len(self.images) - 1)
            self.sendMessage(
                msg,
                picture_url=self.images[list(self.images.keys())[pic]]["picture_url"],
            )

            # remove the user in 10 mins if they have not responded
            delay = 600
            print("----------------", flush=True)
            print(
                f"VibeBot => Member: {self.member['name']} has until "
                + f"{ datetime.now() + timedelta(seconds=delay)} to answer the vibe check.", flush=True
            )
            print("----------------", flush=True)
            threading.Timer(delay, self.finishVibeCheck).start()

    def finishVibeCheck(self):
        """Is called when a vibe thread finishes, resolves the check and starts anew """
        if not self.member_responded:
            if "owner" in self.member["roles"]:
                msg = (
                    f"@{self.member['name']} You failed the Vibe Check...but I can't remove the group owner. "
                    + "However just because I can't remove you doesn't excuse your vibe. Fix it, please."
                )
                self.sendMessage(msg)
            else:
                self.sendMessage(
                    f"@{self.member['name']} looks like you failed the vibe check..."
                )
                self.remove(self.member)

        self.member = None
        self.member_responded = False
        self.startThread()

    def stopVibeCheck(self):
        """ Stops a check if the users answers...doesnt stop the thread"""
        msg = f"@{self.member['name']} Okay you seem to be vibin, we're good."
        self.sendMessage(msg)
        self.member_responded = True
        self.member = None

    def remove(self, member) -> requests.Response:
        """Removes a member from a group
        
        Args:
            member ([dict]): a member dict

        Returns:
            [requests.Response]: response
        """
        # I was very confused as how to get a membership id...heres the answer I posted on SO:
        # https://stackoverflow.com/questions/36228748/determining-users-membership-id-for-a-group-given-user-id-in-groupme-api/63551443#63551443

        # authenticate the request with the api token
        params = {"token": self.api_token}
        # get the messages for the bot's group
        response = self.api_session.post(
            f"{self.api_base_url}/groups/{self.group_id}/members/{member['id']}/remove",
            params=params,
        )
        return response
