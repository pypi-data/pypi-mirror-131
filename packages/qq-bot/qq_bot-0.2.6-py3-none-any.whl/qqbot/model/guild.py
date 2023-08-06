# -*- coding: utf-8 -*-


class Guild:
    def __init__(self, data=None):
        self.id = ""
        self.name = ""
        self.icon = ""
        self.owner_id = ""
        self.owner = False
        self.member_count = 0
        self.max_members = 0
        self.description = ""
        self.joined_at = ""
        if data:
            self.__dict__ = data
