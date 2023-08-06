# -*- coding: utf-8 -*-


class User:
    def __init__(self, data=None):
        self.id = ""
        self.username = ""
        self.avatar = ""
        self.bot = False
        self.union_openid = ""
        self.union_user_account = ""
        if data is not None:
            self.__dict__ = data


class Member:
    def __init__(self, data=None):
        self.user = User()
        self.nick = ""
        self.roles = [""]
        self.joined_at = ""
        if data is not None:
            self.__dict__ = data


class MemberWithGuildID:
    def __init__(self, data=None):
        self.guild_id = ""
        self.user = User()
        self.nick = ""
        self.roles = [""]
        self.joined_at = ""
        if data is not None:
            self.__dict__ = data
