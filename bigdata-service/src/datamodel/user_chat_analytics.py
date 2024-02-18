"""  User Chat Analytics class
Author: Sudipto Nandi

Copyrights: MentorLink 2021-2022

Description: This class implements
the Schema class for user profile data analytics.
"""
from marshmallow import Schema, fields, post_load, ValidationError
from typing import List

"""
Schema Definition of User Profile Data Analytics.
"""


class UserChatAnalyticsInfo:
    """
    Class to implement the UserChatAnalyticsInfo
    Corresponding to UserChatAnalyticsInfoSchema
    """

    def __init__(self, peer_list: list[int],
                 group_list: list[int]):
        self.peer_list = peer_list
        self.group_list = group_list

    def __str__(self):
        strs = f'peer_list: {self.peer_list} group_list: {self.group_list} \n'
        return strs

    def __len__(self):
        return len(self.group_list) + len(self.peer_list)


class UserChatAnalytics:
    """
    Class to implement UserChatAnalytics.
    Corresponding to Schema UserChatAnalyticsSchema
    """

    def __init__(self, user_id: int, chat_info: UserChatAnalyticsInfo):
        self.user_id = user_id
        self.chat_info = chat_info

    def __str__(self):
        strs = f'UserId: {self.user_id}\n'
        strs += f'\tUser Chat Analytics Data {self.chat_info.__str__()}'
        return strs

    def __len__(self):
        return 1 + len(self.chat_info)


class UserChatAnalyticsInfoSchema(Schema):
    peer_list = fields.List(fields.Integer())
    group_list = fields.List(fields.Integer())

    @post_load
    def create_user_chat_analytics_info(self, data, **kwargs):
        return UserChatAnalyticsInfo(**data)


class UserChatAnalyticsSchema(Schema):
    user_id = fields.Integer()
    chat_info = fields.Nested(UserChatAnalyticsInfoSchema)

    @post_load
    def create_user_chat_analytics(self, data, **kwargs):
        return UserChatAnalytics(**data)
