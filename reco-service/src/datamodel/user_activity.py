"""  Item class
Author: Sudipto Nandi

Copyrights: MentorLink 2021-2022

Description: This class implements
the Schema class for User Activity class.
"""
from marshmallow import Schema, fields, post_load, ValidationError

"""
Schema Definition of User Activity.
"""


class ActivityInfoSchema(Schema):
    shared = fields.Bool()
    liked = fields.Bool()
    saved = fields.Bool()
    ratings = fields.Integer()
    tot_dur = fields.Integer()
    visit = fields.Bool()
    expand = fields.Bool()

    @post_load
    def create_activity_info(self, data, **kwargs):
        return ActivityInfo(**data)


class ItemSchema(Schema):
    res_id = fields.Integer()
    activity_info = fields.Nested(ActivityInfoSchema)

    @post_load
    def create_item(self, data, **kwargs):
        return Item(**data)


class UserActivitySchema(Schema):
    user_id = fields.Integer()
    items_info = fields.List(fields.Nested(ItemSchema))

    @post_load
    def create_user_activity(self, data, **kwargs):
        return UserActivity(**data)


class UsersInfoSchema(Schema):
    users_info = fields.List(fields.Nested(UserActivitySchema))

    @post_load
    def create_user_activities(self, data, **kwargs):
        return UsersInfo(**data)


class ActivityInfo:
    """
    Class to implement the Activity Info.
    Corresponding to Schema ActivityInfoSchema
    """

    def __init__(self, shared: bool, liked: bool, saved: bool,
                 ratings: int, tot_dur: int, visit: bool,
                 expand: bool):
        self.shared = shared
        self.liked = liked
        self.saved = saved
        self.ratings = ratings
        self.tot_dur = tot_dur
        self.visit = visit
        self.expand = expand

    def __str__(self):
        return f'Shared:{self.shared} Liked:{self.liked} Saved:{self.saved} Ratings:{self.ratings} ' \
               f'Total Duration:{self.tot_dur} Visit:{self.visit} Expand:{self.expand}'


class Item:
    """
    Class to implement the Item.
    Corresponding to Schema ItemSchema
    """

    def __init__(self, res_id: int, activity_info: ActivityInfo):
        self.res_id = res_id
        self.activity_info = activity_info

    def __str__(self):
        return f'ResId: {self.res_id} Activity Info: {self.activity_info.__str__()}'

    def __len__(self):
        return 1


class UserActivity:
    """
    Class to implement UserActivity.
    Corresponding to Schema UserActivitySchema
    """

    def __init__(self, user_id: int, items_info: list[Item]):
        self.user_id = user_id
        self.items_info = items_info

    def __str__(self):
        strs = f'UserId: {self.user_id}\n'
        for a in self.items_info:
            strs += f'\t{a.__str__()}\n'
        return strs

    def __len__(self):
        return len(self.items_info)


class UsersInfo:
    """
    Class to implement UserActivities
    Corresponding to Schema UserActivitiesAchema
    """

    def __init__(self, users_info: list[UserActivity]):
        self.users_info = users_info

    def __str__(self):
        strs = ""
        for a in self.users_info:
            strs += a.__str__() + "\n"
        return strs

    def __len__(self):
        return len(self.users_info)
