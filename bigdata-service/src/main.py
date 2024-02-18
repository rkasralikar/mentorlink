"""main.py

Author: Sudipto Nandi

Copyrights: MentorLink 2021-2022

Description: main for the micro service.
"""
import argparse
from src.businesslogic.item_rss_feed import ItemsRssFeed
from src.server.server import start_rest_server
from common_modules.logger.mnt_logging import MntLogging as MyLog
from common_modules.storage.resource_mgr import ResourceMgr
from common_modules.storage.storage_elastic import StorageElastic
from src.businesslogic.etl_manager import EtlManager
from src.businesslogic.user_profile_etl import EtlJObUserProfile
from src.businesslogic.user_activity_etl import EtlJObUserActivity
from src.businesslogic.user_profile_anlytics_etl import EtlJObUserProfileAnalytics
from src.businesslogic.user_chat_analytics_etl import EtlJObUserChatAnalytics
from src.businesslogic.item_normalization_etl import EtlJObItemNormalization
from src.businesslogic.items_udemy import ItemsUdemy
from src.businesslogic.item_youtube import ItemsYoutube
from src.businesslogic.item_stackoverflow import ItemsStackOverflow
from src.businesslogic.item_meetup import ItemsMeetup

import json
import os
from src.businesslogic.kafka_service import start_kafka_service


def parse_config(file_name=None):
    if file_name is None:
        return None
    try:
        f = open('config/' + file_name)
        return json.load(f)
    except:
        return None


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-k', '--kafka',  help="Kafka Config file")
    parser.add_argument('-e', '--etllist', nargs="+", help="List of etls you want to run")
    parser.add_argument('-r', '--restserverconffile', help="Start rest server")
    parser.add_argument('-f', '--freq', type=int, help="Frequency of the Etl in seconds")
    parser.add_argument('-l', '--loglevel', help="Specify log level. debug, error, info, critical")
    args = parser.parse_args()

    log_level = "error"
    if args.loglevel is not None:
        log_level = args.loglevel
    MyLog().setloglevel(log_level)
    resmgr = ResourceMgr(StorageElastic(cleanup=False), cleanup=False)
    if args.kafka is not None:
        start_kafka_service(args.kafka, resmgr)
        return
    elif args.restserverconffile is not None:
        start_rest_server(args.restserverconffile, resmgr)
        return
    else:
        freq = args.freq
        MyLog().getlogger().debug(f"Frequency of etl will be {freq}secs")
        for file in args.etllist:
            etl_objs = []
            config_data = parse_config(file)
            if config_data is None:
                return
            MyLog().getlogger().debug(f"Config Data {config_data}")
            if config_data['name'] == 'user-profile':
                etl_objs.append(EtlJObUserProfile(
                    end_point=config_data['end_point'],
                    login_url=config_data['login_url'],
                    user_name=config_data['user_name'],
                    password=config_data['password'],
                    resource_mgr=resmgr,
                    table_name=config_data['profile_table_name'],
                    mapping_name=None,
                    interest_list_sink='interest_list_sink'))
            elif config_data['name'] == 'user-activity':
                etl_objs.append(EtlJObUserActivity(
                    end_point=config_data['end_point'],
                    login_url=config_data['login_url'],
                    user_name=config_data['user_name'],
                    password=config_data['password'],
                    resource_mgr=resmgr))
            elif config_data['name'] == 'user-profile-analytics':
                etl_objs.append(EtlJObUserProfileAnalytics(
                    end_point=config_data['end_point'],
                    login_url=config_data['login_url'],
                    user_name=config_data['user_name'],
                    password=config_data['password'],
                    resource_mgr=resmgr))
            elif config_data['name'] == 'user-chat-analytics':
                etl_objs.append(EtlJObUserChatAnalytics(
                    end_point=config_data['end_point'],
                    login_url=config_data['login_url'],
                    user_name=config_data['user_name'],
                    password=config_data['password'],
                    resource_mgr=resmgr))
            elif config_data['name'] == 'youtube':
                etl_objs.append(EtlJObItemNormalization(
                    end_point="",
                    login_url="",
                    user_name="",
                    password="",
                    item_src=[ItemsYoutube(table_name=config_data['sink_name'])],
                    resource_mgr=resmgr))
            elif config_data['name'] == 'rss':
                etl_objs.append(EtlJObItemNormalization(
                    end_point="",
                    login_url="",
                    user_name="",
                    password="",
                    item_src=[ItemsRssFeed(table_name=config_data['sink_name'])],
                    resource_mgr=resmgr))
            elif config_data['name'] == 'udemy':
                etl_objs.append(EtlJObItemNormalization(
                    end_point="",
                    login_url="",
                    user_name="",
                    password="",
                    item_src=[ItemsUdemy(table_name=config_data['sink_name'])],
                    resource_mgr=resmgr))
            elif config_data['name'] == 'stackoverflow':
                etl_objs.append(EtlJObItemNormalization(
                    end_point="",
                    login_url="",
                    user_name="",
                    password="",
                    item_src=[ItemsStackOverflow(table_name=config_data['sink_name'])],
                    resource_mgr=resmgr))
            elif config_data['name'] == 'meetup':
                etl_objs.append(EtlJObItemNormalization(
                    end_point="",
                    login_url="",
                    user_name="",
                    password="",
                    item_src=[ItemsMeetup(table_name=config_data['sink_name'])],
                    resource_mgr=resmgr))
            else:
                MyLog().getlogger().error(f"Unknown etl type {config_data['name']}")


        EtlManager(etl_objs=etl_objs, exp_time=freq).start()


if __name__ == "__main__":
    main()
