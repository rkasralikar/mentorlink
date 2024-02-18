"""  User Profile class
Author: Sudipto Nandi

Copyrights: MentorLink 2021-2022

Description: This class implements
the Schema class for user profile data.
"""
from marshmallow import Schema, fields, post_load, ValidationError
from typing import List

"""
Schema Definition of User Profile Data.
"""


class UserProfileDataInfoExperience:
    def __init__(self, company_name: str, role_desc: str, start_date: str, end_date: str):
        self.end_date = end_date
        self.start_date = start_date
        self.company_name = company_name
        self.role_desc = role_desc

    def __str__(self):
        strs = f'Company Name: {self.company_name} Role Desc: {self.role_desc} Start Date: {self.start_date}' \
               f' End Date: {self.end_date}\n'
        return strs

    def __len__(self):
        return 1


class UserProfileDataInfo:
    """
    Class to implement the profile data
    Corresponding to UserProfileDataSchema
    """

    def __init__(self, name: str, phone: str, email: str, linkedin_profile: str,
                 sign_in_method: str, about: str, total_exp: int, interest: list[str],
                 experience: list[UserProfileDataInfoExperience], skills: list[str],
                 saved_items: list[int]):
        self.name = name
        self.phone = phone
        self.about = about
        self.email = email
        self.linkedin_profile = linkedin_profile
        self.sign_in_method = sign_in_method
        self.total_exp = total_exp
        self.interest = interest
        self.experience = experience
        self.skills = skills
        self.saved_items = saved_items

    def __str__(self):
        strs = f'Name: {self.name} Phone: {self.phone} About: {self.about} Total Exp: {self.total_exp}'
        strs += f' Interests: {self.interest} Skills: {self.skills}\n'
        for exp in self.experience:
            strs += f'\t Experience: {exp}'
        return strs

    def __len__(self):
        return 4 + len(self.interest) + len(self.experience) + len(self.skills)


class UserProfileDataDevInfo:
    def __init__(self, device_id: str, manufacturer: str, os_ver: str, app_ver: str):
        self.device_id = device_id
        self.manufacturer = manufacturer
        self.os_ver = os_ver
        self.app_ver = app_ver

    def __str__(self):
        strs = f'Device ID: {self.device_id} Manufacturer: {self.manufacturer} OS Version: {self.os_ver}' \
               f'App Version: {self.app_ver}\n'
        return strs

    def __len__(self):
        return 1


class UserProfileData:
    """
    Class to implement UserProfileData.
    Corresponding to Schema UserProfileDataSchema
    """

    def __init__(self, user_id: int, profile_data: UserProfileDataInfo, device_data: list[UserProfileDataDevInfo]):
        self.user_id = user_id
        self.profile_data = profile_data
        self.device_data = device_data

    def __str__(self):
        strs = f'UserId: {self.user_id}\n'
        strs += f'\tProfile Data {self.profile_data.__str__()}'
        for a in self.device_data:
            strs += f'\t{a.__str__()}'
        return strs

    def __len__(self):
        return 2 + len(self.device_data)


class UserProfileDataInfoExperienceSchema(Schema):
    company_name = fields.String()
    role_desc = fields.String()
    start_date = fields.String()
    end_date = fields.String()

    @post_load
    def create_user_profile_data_info_experience(self, data, **kwargs):
        return UserProfileDataInfoExperience(**data)


class UserProfileDataInfoSchema(Schema):
    name = fields.String()
    email = fields.String()
    phone = fields.String()
    about = fields.String()
    linkedin_profile = fields.String()
    sign_in_method = fields.String()
    total_exp = fields.Integer()
    interest = fields.List(fields.String())
    experience = fields.List(fields.Nested(UserProfileDataInfoExperienceSchema))
    skills = fields.List(fields.String())
    saved_items = fields.List(fields.Integer())

    @post_load
    def create_user_profile_data_info(self, data, **kwargs):
        return UserProfileDataInfo(**data)


class UserProfileDataDevInfoSchema(Schema):
    device_id = fields.String()
    manufacturer = fields.String()
    os_ver = fields.String()
    app_ver = fields.String()

    @post_load
    def create_user_profile_dev_info(self, data, **kwargs):
        return UserProfileDataDevInfo(**data)


class UserProfileDataSchema(Schema):
    user_id = fields.Integer()
    profile_data = fields.Nested(UserProfileDataInfoSchema)
    device_data = fields.List(fields.Nested(UserProfileDataDevInfoSchema))

    @post_load
    def create_user_profile_data(self, data, **kwargs):
        return UserProfileData(**data)
