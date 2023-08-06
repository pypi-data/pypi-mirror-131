# -*- coding: utf-8 -*-

from qqbot.model.member import User, Member


class Message:
    def __init__(self, data=None):
        self.id = ""
        self.channel_id = ""
        self.guild_id = ""
        self.content = ""
        self.timestamp = ""
        self.edited_timestamp = ""
        self.author = User()
        self.attachments = [MessageAttachment()]
        self.embeds = [MessageEmbed()]
        self.mentions = [User()]
        self.member = Member()
        self.ark = MessageArk()
        if data:
            self.__dict__ = data


class MessageAttachment:
    def __init__(self, data=None):
        self.url = ""
        if data:
            self.__dict__ = data


class MessageEmbed:
    def __init__(self, data=None):
        # 标题
        self.title = ""
        # 消息弹窗内容
        self.prompt = ""
        # 缩略图
        self.thumbnail = MessageEmbedThumbnail()
        # 消息创建时间
        self.fields = [MessageEmbedField()]
        if data:
            self.__dict__ = data


class MessageEmbedThumbnail:
    def __init__(self, data=None):
        # 图片地址
        self.url = ""
        if data is not None:
            self.__dict__ = data


class MessageEmbedField:
    def __init__(self, data=None):
        self.key = ""
        self.value = ""
        if data:
            self.__dict__ = data


class MessageArk:
    def __init__(self, data=None):
        self.template_id = 0
        self.kv = [MessageArkKv()]
        if data:
            self.__dict__ = data


class MessageArkKv:
    def __init__(self, data=None):
        self.key = ""
        self.value = ""
        self.obj = [MessageArkObj()]
        if data:
            self.__dict__ = data


class MessageArkObj:
    def __init__(self, data=None):
        self.obj_kv = [MessageArkObjKv()]
        if data:
            self.__dict__ = data


class MessageArkObjKv:
    def __init__(self, data=None):
        self.key = ""
        self.value = ""
        if data:
            self.__dict__ = data


class MessageSendRequest:
    def __init__(
        self,
        content,
        msg_id=None,
        embed: MessageEmbed = None,
        ark: MessageArk = None,
        image="",
    ):
        """

        :param content:消息内容，文本内容，支持内嵌格式
        :param msg_id:要回复的消息id(Message.id), 在 AT_CREATE_MESSAGE 事件中获取。带了 msg_id 视为被动回复消息，否则视为主动推送消息
        :param embed:embed 消息，一种特殊的 ark
        :param ark:ark 消息
        :param image:图片url地址
        """

        self.content = content
        self.embed = embed
        self.ark = ark
        self.image = image
        self.msg_id = msg_id


class DirectMessageGuild:
    def __init__(self, data=None):
        self.guild_id = ""
        self.channel_id = ""
        self.creat_time = ""
        if data is not None:
            self.__dict__ = data


class CreateDirectMessageRequest:
    def __init__(self, source_guild_id, user_id):
        """
        :param source_guild_id: 创建的私信频道ID
        :param user_id: 私信接收人用户ID
        """
        self.recipient_id = user_id
        self.source_guild_id = source_guild_id
