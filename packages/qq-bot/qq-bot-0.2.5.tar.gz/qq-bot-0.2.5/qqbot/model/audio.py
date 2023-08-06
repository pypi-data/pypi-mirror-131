# -*- coding: utf-8 -*-

from enum import Enum


class STATUS(Enum):
    START = 0
    PAUSE = 1
    RESUME = 2
    STOP = 3


class AudioControl:
    def __init__(self, audio_url, text, status: STATUS):
        self.audio_url = audio_url
        self.text = text
        self.status = status


class AudioAction:
    def __init__(self, data=None):
        self.guild_id = ""
        self.channel_id = ""
        self.audio_url = ""
        self.text = ""
        if data is not None:
            self.__dict__ = data
