# -*- coding: utf-8 -*-

from qqbot.model.member import User


class GuildMember:
    def __init__(self, data=None):
        self.user: [User] = None
        self.nick = ""
        self.roles = []
        self.joined_at = ""
        if data is not None:
            self.__dict__ = data


class GuildMembersPager:
    def __init__(self):
        self.after = ""
        self.limit = ""
