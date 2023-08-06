# -*- coding: utf-8 -*-


class Channel:
    def __init__(self, data=None):
        self.id = ""
        self.guild_id = ""
        self.name = ""
        self.type = 0
        self.sub_type = 0
        self.position = 0
        self.parent_id = ""
        self.owner_id = ""
        if data is not None:
            self.__dict__ = data
