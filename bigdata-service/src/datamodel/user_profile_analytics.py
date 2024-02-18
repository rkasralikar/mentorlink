"""  User Profile Analytics class
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


class UserProfileDataAnalyticsInfo:
    """
    Class to implement the profile data
    Corresponding to UserProfileDataSchema
    """

    def __init__(self, num_saved_feed: int, last_login_time: str, num_feed_visited: int,
                 total_time_spent: int, search_keywords: list[str],
                 app_version: str):
        self.num_saved_feed = num_saved_feed
        self.last_login_time = last_login_time
        self.num_feed_visited = num_feed_visited
        self.total_time_spent = total_time_spent
        self.search_keywords = search_keywords
        self.app_version = app_version

    def __str__(self):
        strs = f'num_saved_feed: {self.num_saved_feed} last_login_time: {self.last_login_time} \n'
        strs += f' num_feed_visited: {self.num_feed_visited} total_time_spent: {self.total_time_spent}\n'
        strs += f' search_keywords: {self.search_keywords} app_version: {self.app_version}\n'
        return strs

    def __len__(self):
        return 5 + len(self.search_keywords)


class UserProfileDataAnalytics:
    """
    Class to implement UserProfileData.
    Corresponding to Schema UserProfileDataSchema
    """

    def __init__(self, user_id: int, profile_info: UserProfileDataAnalyticsInfo):
        self.user_id = user_id
        self.profile_info = profile_info

    def __str__(self):
        strs = f'UserId: {self.user_id}\n'
        strs += f'\tProfile Analytics Data {self.profile_info.__str__()}'
        return strs

    def __len__(self):
        return 1 + len(self.profile_info)


class UserProfileDataAnalyticsInfoSchema(Schema):
    num_saved_feed = fields.Integer()
    last_login_time = fields.String()
    num_feed_visited = fields.Integer()
    total_time_spent = fields.Integer()
    search_keywords = fields.List(fields.String())
    app_version = fields.String()

    @post_load
    def create_user_profile_analytics_info(self, data, **kwargs):
        return UserProfileDataAnalyticsInfo(**data)


class UserProfileDataAnalyticsSchema(Schema):
    user_id = fields.Integer()
    profile_info = fields.Nested(UserProfileDataAnalyticsInfoSchema)

    @post_load
    def create_user_profile_data(self, data, **kwargs):
        return UserProfileDataAnalytics(**data)
