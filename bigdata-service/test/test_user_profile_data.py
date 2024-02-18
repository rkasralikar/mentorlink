import pytest
from common_modules.logger.mnt_logging import MntLogging as MyLog
import src.datamodel.user_profile as user_profile
import json
from common_modules.storage.resource_mgr import ResourceMgr
from common_modules.storage.storage_elastic import StorageElastic


class TestClass:
    def setup_method(self, method):
        MyLog().setloglevel('debug')
        MyLog().getlogger().info("===== Setup Test Case %s ====" %
                                 method.__name__)

    def teardown_method(self, method):
        MyLog().getlogger().info("===== Teardown Test Case %s ====" %
                                 method.__name__)

    def test_user_profile_data_serialization(self):
        uaobj = user_profile.UserProfileData(user_id=10000,
                                             profile_data=
                                             user_profile.UserProfileDataInfo(name="Sudipto",
                                                                              phone="12345",
                                                                              email="snandi@yomail.com",
                                                                              about="This is test",
                                                                              sign_in_method='phone',
                                                                              total_exp=10,
                                                                              linkedin_profile="snandi@linked.com",
                                                                              interest=['machine-learning', 'python',
                                                                                        'c++'],
                                                                              experience=[
                                                                                  user_profile.UserProfileDataInfoExperience(
                                                                                      company_name="Roku",
                                                                                      role_desc="Sr. Software Eng",
                                                                                      start_date="1/1/1",
                                                                                      end_date="1/1/2"),
                                                                                  user_profile.UserProfileDataInfoExperience(
                                                                                      company_name="Juniper",
                                                                                      role_desc="Sr. Staff Software Eng",
                                                                                      start_date="1/1/1",
                                                                                      end_date="2/2/2"
                                                                                  )
                                                                              ],
                                                                              skills=["machine-learning", "python"],
                                                                              saved_items=[1, 2, 3]
                                                                              ),
                                             device_data=[
                                                 user_profile.UserProfileDataDevInfo(device_id="1",
                                                                                     manufacturer='apple',
                                                                                     os_ver='1.0',
                                                                                     app_ver='1.0'),
                                                 user_profile.UserProfileDataDevInfo(device_id="2",
                                                                                     manufacturer='apple',
                                                                                     os_ver='1.0',
                                                                                     app_ver='1.1'),
                                             ]
                                             )
        user_profile_data_json_ser = user_profile.UserProfileDataSchema().dump(uaobj)
        assert len(user_profile_data_json_ser) != 0
        assert user_profile_data_json_ser['user_id'] == 10000
        assert user_profile_data_json_ser['profile_data']['name'] == "Sudipto"

    def test_user_profile_data_deserialization(self):
        jos = json.dumps(
            {'device_data': [{'app_ver': '1.0', 'os_ver': '1.0', 'manufacturer': 'apple', 'device_id': '1'},
                             {'app_ver': '1.1', 'os_ver': '1.0', 'manufacturer': 'apple', 'device_id': '2'}],
             'user_id': 10000,
             'profile_data': {'name': 'Sudipto', 'email': 'snandi@yomail.com', 'linkedin_profile': 'snandi@linked.in',
                              'sign_in_method': 'phone',
                              'interest': ['machine-learning', 'python', 'c++'], 'phone': '12345',
                              'about': 'This is test', 'skills': ['machine-learning', 'python'], 'experience': [
                     {'start_date': '1/1/1', 'company_name': 'Roku', 'end_date': '1/1/2',
                      'role_desc': 'Sr. Software Eng'},
                     {'start_date': '1/1/1', 'company_name': 'Juniper', 'end_date': '2/2/2',
                      'role_desc': 'Sr. Staff Software Eng'}], 'total_exp': 10, 'saved_items': [1, 2, 3]}}

        )
        uobj = user_profile.UserProfileDataSchema().loads(jos)
        assert len(uobj) != 0
        assert uobj.user_id == 10000

        jos = json.dumps({'user_id': '18446744073709551615',
                          'profile_data': {'name': 'vishal', 'email': 'vishal@yopmail.com', 'phone': '9762109172',
                                           'linkedin_profile': 'https://in.linkedin.com/profile/url12',
                                           'sign_in_method': 'phone',
                                           'about': 'demo about', 'total_exp': '3',
                                           'interest': ['604c8a0f42b538590c462bd2'], 'experience': [
                                  {'company_name': 'demo company name', 'role_desc': 'demo role description',
                                   'start_date': '29/09/21', 'end_date': '23/09/22'}],
                                           'skills': ['604c8118a08ede61145ea762'], 'saved_items': [1, 2, 3]},
                          'device_data': [{'device_id': '1234', 'manufacturer': 'apple', 'os_ver': 'apple1',
                                           'app_ver': 'er3432'}]})
        uobj = user_profile.UserProfileDataSchema().loads(jos)

        jos = json.dumps({'profile_data': {'name': 'vishal', 'email': 'vishal@yopmail.com', 'phone': '9762109172',
                                           'linkedin_profile': 'https://in.linkedin.com/profile/url12',
                                           'sign_in_method': 'email', 'about': 'demo about', 'total_exp': '3',
                                           'interest': ['604c8a0f42b538590c462bd2'], 'experience': [
                {'company_name': 'demo company name', 'role_desc': 'demo role description', 'start_date': '29/09/21',
                 'end_date': '23/09/22'}], 'skills': ['604c8118a08ede61145ea762'], 'saved_items': [1, 2, 3]}, 'user_id': 1, 'device_data': [
            {'device_id': '1234', 'manufacturer': 'apple', 'os_ver': 'apple1', 'app_ver': 'er3432'}]})
        uobj = user_profile.UserProfileDataSchema().loads(jos)
        print(uobj)
