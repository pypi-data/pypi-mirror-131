# -*- coding: utf-8 -*-

from qqbot.model.channel import Channel


class Role:
    def __init__(self, data=None):
        self.id = ""
        self.name = ""
        self.color = 0
        self.hoist = 0
        self.number = 0
        self.number_limit = 0
        if data is not None:
            self.__dict__ = data


class GuildRoles:
    def __init__(self, data=None):
        self.guild_id = ""
        self.roles = [Role()]
        self.role_num_limit = ""
        if data is not None:
            self.__dict__ = data


class RoleUpdateRequest:
    def __init__(self, data=None):
        self.guild_id = ""
        self.filter: [RoleUpdateFilter] = None
        self.info: [RoleUpdateInfo] = None
        if data is not None:
            self.__dict__ = data


class RoleUpdateFilter:
    def __init__(self, name, color, hoist):
        self.name = name
        self.color = color
        self.hoist = hoist


class RoleUpdateInfo:
    def __init__(self, name, color, hoist):
        """
        身份组更新的信息

        :param name:名称
        :param color:ARGB的HEX十六进制颜色值转换后的十进制数值
        :param hoist:在成员列表中单独展示: 0-否, 1-是
        """
        self.name = name
        self.color = color
        self.hoist = hoist


class RoleUpdateResult:
    def __init__(self, data=None):
        self.guild_id = ""
        self.role_id = ""
        self.role = Role()
        if data is not None:
            self.__dict__ = data


class RoleMemberRequest:
    def __init__(self, data=None):
        self.channel: [Channel] = None
