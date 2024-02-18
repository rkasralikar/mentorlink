"""  Item class
Author: Sudipto Nandi

Copyrights: MentorLink 2021-2022

Description: This class implements
the Schema class for item info query response class.
"""
from marshmallow import Schema, fields, post_load, ValidationError

"""
Schema Definition of Item Info Response.
"""


class ItemsInfoSchema(Schema):
    name = fields.String()
    url = fields.URL()
    description = fields.String()
    provider = fields.String()
    online = fields.Bool()
    paid = fields.Bool()

    @post_load
    def create_items_info(self, data, **kwargs):
        return ItemsInfo(**data)


class ItemsInfoResponseSchema(Schema):
    item_id = fields.Integer()
    item_id_info = fields.Nested(ItemsInfoSchema)

    @post_load
    def create_items_info_response(self, data, **kwargs):
        return ItemsInfoResponse(**data)


class ItemsInfo:
    def __init__(self, name: str, url: str, description: str, provider: str, online: bool, paid: bool):
        self.name = name
        self.url = url
        self.description = description
        self.provider = provider
        self.online = online
        self.paid = paid

    def __str__(self):
        strs = f'name: {self.name} url: {self.url} provider: {self.provider}\n'
        return strs

    def __len__(self):
        return 1


class ItemsInfoResponse:
    def __init__(self, item_id: int, item_id_info: ItemsInfo):
        self.item_id = item_id
        self.item_id_info = item_id_info

    def __str__(self):
        strs = f'Item Id: {self.item_id} Info: {self.item_id_info}\n'
        return strs

    def __len__(self):
        return 1 + len(self.item_id_info)
