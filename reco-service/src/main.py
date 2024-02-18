"""main.py

Author: Sudipto Nandi

Copyrights: MentorLink 2021-2022

Description: main for the recommendation service.
"""
import argparse
from common_modules.storage.storage_elastic import StorageElastic
from src.server.server import start_rest_server
from src.recomgr.reco_mgr import start_recommendation_generation
from common_modules.logger.mnt_logging import MntLogging as MyLog
from common_modules.storage.resource_mgr import ResourceMgr
import json


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
    parser.add_argument('-c', '--config', help="Config file")
    parser.add_argument('-l', '--loglevel', help="Specify log level. debug, error, info, critical")
    args = parser.parse_args()

    log_level = "error"
    if args.loglevel is not None:
        log_level = args.loglevel
    MyLog().setloglevel(log_level)

    file = args.config
    config_data = parse_config(file)
    if config_data is None:
        MyLog().getlogger().error(f"Config file is not provided, terminating")
        return
    MyLog().getlogger().debug(f"Config Data {config_data}")

    start_recommendation_generation(user_profile_table_name=config_data['user_profile_table'],
                                    resmgr=ResourceMgr(StorageElastic(cleanup=False), cleanup=False))
    start_rest_server(port=config_data['rest_server_port'], host=config_data['rest_server_host'])
    return


if __name__ == "__main__":
    main()
