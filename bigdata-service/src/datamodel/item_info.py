"""  Item class
Author: Sudipto Nandi

Copyrights: MentorLink 2021-2022

Description: This class implements
the Schema class for item info query response class.
"""
from marshmallow import Schema, fields, post_load, ValidationError
from typing import List

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
    upvotecount = fields.Integer()
    downvotecount = fields.Integer()
    sharecount = fields.Integer()
    tags = fields.List(fields.String())

    @post_load
    def create_items_info(self, data, **kwargs):
        return ItemsInfo(**data)


class ItemsInfoResponseSchema(Schema):
    item_id = fields.Integer()
    item_id_info = fields.Nested(ItemsInfoSchema)

    @post_load
    def create_items_info_response(self, data, **kwargs):
        return ItemsInfoResponse(**data)


class ItemsInfoBulkResponseSchema(Schema):
    item_list_info = fields.List(fields.Nested(ItemsInfoResponseSchema))

    @post_load
    def create_items_bulk_info_response(self, data, **kwargs):
        return ItemsInfoBulkResponse(**data)


class ItemsInfo:
    def __init__(self, name: str, url: str, description: str, provider: str, online: bool, paid: bool, upvotecount: int,
                 downvotecount: int, sharecount: int, tags: List[str]):
        self.name = name
        self.url = url
        self.description = description
        self.provider = provider
        self.online = online
        self.paid = paid
        self.upvotecount = upvotecount
        self.downvotecount = downvotecount
        self.sharecount = sharecount
        self.tags = tags

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


class ItemsInfoBulkResponse:
    def __init__(self, item_list_info: List[ItemsInfoResponse]):
        self.item_list_info = item_list_info

    def __str__(self):
        strs = "Info "
        for itr in self.item_list_info:
            strs += f'{itr}\n'
        return strs

    def __len__(self):
        return len(self.item_list_info)


class ItemInfoRequest:
    def __init__(self, item_id: int):
        self.item_id = item_id

    def __str__(self):
        strs = f'ItemId: {self.item_id}\n'
        return strs

    def __len__(self):
        return 1


class ItemInfoBulkRequest:
    def __init__(self, item_id_list: List[ItemInfoRequest]):
        self.item_id_list = item_id_list

    def __str__(self):
        strs = f'ItemIdList: {self.item_id_list}\n'
        return strs

    def __len__(self):
        return len(self.item_id_list)


class ItemInfoRequestSchema(Schema):
    item_id = fields.Integer()

    @post_load
    def create_item_info_request_request(self, data, **kwargs):
        return ItemInfoRequest(**data)


class ItemInfoBulkRequestSchema(Schema):
    item_id_list = fields.List(fields.Nested(ItemInfoRequestSchema))

    @post_load
    def create_item_info_bulk_request_request(self, data, **kwargs):
        return ItemInfoBulkRequest(**data)
