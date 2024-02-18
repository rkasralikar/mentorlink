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
    disliked = fields.Bool()
    saved = fields.Bool()
    rating = fields.Integer()
    tot_dur = fields.Integer()
    visit = fields.Bool()
    expand = fields.Bool()

    @post_load
    def create_activity_info(self, data, **kwargs):
        return ActivityInfo(**data)


class ItemSchema(Schema):
    item_id = fields.Integer()
    activity_info = fields.Nested(ActivityInfoSchema)

    @post_load
    def create_item(self, data, **kwargs):
        return Item(**data)


class UserActivitySchema(Schema):
    user_id = fields.Integer()
    activity = fields.List(fields.Nested(ItemSchema))

    @post_load
    def create_user_activity(self, data, **kwargs):
        return UserActivity(**data)


class UserActivityResponseSchema(Schema):
    user_id = fields.Integer()
    status = fields.String()

    @post_load
    def create_user_activity_response(self, data, **kwargs):
        return UserActivityResponse(**data)


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

    def __init__(self, shared: bool, liked: bool, disliked: bool, saved: bool,
                 rating: int, tot_dur: int, visit: bool):
        self.shared = shared
        self.liked = liked
        self.disliked = disliked
        self.saved = saved
        self.rating = rating
        self.tot_dur = tot_dur
        self.visit = visit

    def __str__(self):
        return f'Shared:{self.shared} Liked:{self.liked} Disliked: {self.disliked} Saved:{self.saved} Ratings:{self.rating} ' \
               f'Total Duration:{self.tot_dur} Visit:{self.visit}'


class Item:
    """
    Class to implement the Item.
    Corresponding to Schema ItemSchema
    """

    def __init__(self, item_id: int, activity_info: ActivityInfo):
        self.item_id = item_id
        self.activity_info = activity_info

    def __str__(self):
        return f'ResId: {self.item_id} Activity Info: {self.activity_info.__str__()}'

    def __len__(self):
        return 1


class UserActivity:
    """
    Class to implement UserActivity.
    Corresponding to Schema UserActivitySchema
    """

    def __init__(self, user_id: int, activity: list[Item]):
        self.user_id = user_id
        self.activity = activity

    def __str__(self):
        strs = f'UserId: {self.user_id}\n'
        for a in self.activity:
            strs += f'\t{a.__str__()}\n'
        return strs

    def __len__(self):
        return len(self.activity)


class UserActivityResponse:
    """
        Class to implement UserActivity.
        Corresponding to Schema UserActivitySchema
        """

    def __init__(self, user_id: int, status):
        self.user_id = user_id
        self.status = status

    def __str__(self):
        strs = f'UserId: {self.user_id} Status: {self.status}\n'
        return strs

    def __len__(self):
        return 1


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
