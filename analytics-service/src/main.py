"""main.py

Description: main for the analytics service.
"""

from business_logic.analytics import Analytics
import argparse
import json
from time import sleep


def parse_config(file_name=None, add_path=True):
    if file_name is None:
        return None
    try:
        if add_path:
            f = open('config/' + file_name)
        else:
            f = open(file_name)
        return json.load(f)
    except:
        return None


if __name__ == "__main__":
    default_config_file = "analytics_config.json"

    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--conf', help="Configuration file")
    args = parser.parse_args()

    config_data = parse_config(args.conf)
    if config_data is None:
        print(f"Invalid or no config file has been provided, using default {default_config_file}")
        config_data = parse_config(default_config_file)
        if config_data is None:
            print(f"No Config file exist terminating")
            exit(0)

    # default is 1 day
    pause_sleep = 86400
    if "sleep" in config_data:
        pause_sleep = config_data['sleep']

    config_data['sleep'] = pause_sleep

    print(f"Frequency of etl will be {pause_sleep} secs")

    analytics = Analytics(config_data)
    while True:
        analytics.start()
        sleep(pause_sleep)
