"""  Item class
Author: Sudipto Nandi

Copyrights: MentorLink 2021-2022

Description: This class implements
the Schema class for recommendation response class.
"""
from marshmallow import Schema, fields, post_load, ValidationError
from typing import List

"""
Schema Definition of Recommendation Response.
"""


class RecommendationRequestSchema(Schema):
    user_id = fields.Integer()
    interest_list = fields.List(fields.String())

    @post_load
    def create_recommendation_request(self, data, **kwargs):
        return RecommendationRequest(**data)


class RecommendationResponseSchema(Schema):
    user_id = fields.Integer()
    item_id_info = fields.List(fields.Integer())

    @post_load
    def create_recommendation_response(self, data, **kwargs):
        return RecommendationResponse(**data)


class RecommendationResponse:
    def __init__(self, user_id: int, item_id_info: List[int]):
        self.user_id = user_id
        self.item_id_info = item_id_info

    def __str__(self):
        strs = f'UserId: {self.user_id}\n'
        for a in self.item_id_info:
            strs += f'ItemId:\t{a}\n'
        return strs

    def __len__(self):
        return 1 + len(self.item_id_info)


class RecommendationRequest:
    def __init__(self, user_id: int, interest_list: List[str]):
        self.user_id = user_id
        self.interest_list = interest_list

    def __str__(self):
        strs = f'UserId: {self.user_id}\n'
        return strs

    def __len__(self):
        return 1
