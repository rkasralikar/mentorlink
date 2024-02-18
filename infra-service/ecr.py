"""ecr.py

Author: Sudipto Nandi

Copyrights: MentorLink 2021-2022

Description: docker deploy script.
"""
import os
import sys
import logging

AWS_ID="205263170971"
REGION="us-west-2"

internal_services=[
            {'name':'analytic', 'tag':'latest', 'use_dev':True, 'active':False},
            {'name': 'apacheservice', 'tag':'latest', 'use_dev':False, 'active':False},
            {'name': 'bigdatakafka', 'tag':'latest', 'use_dev':True, 'active':False},
            {'name': 'bigdatameetup', 'tag':'latest', 'use_dev':True, 'active':True},
            {'name': 'bigdatastackoverflow', 'tag':'latest', 'use_dev':True, 'active':True},
            {'name': 'bigdatarest', 'tag':'latest', 'use_dev':True, 'active':True},
            {'name': 'bigdatarss', 'tag':'latest', 'use_dev':True, 'active':True},
            {'name': 'bigdatauser', 'tag':'latest', 'use_dev':True, 'active':True},
            {'name': 'bigdatayoutube', 'tag':'latest', 'use_dev':True, 'active':True},
            {'name': 'chatservice', 'tag':'latest', 'use_dev':False, 'active':False},
            {'name': 'contentmeetup', 'tag':'latest', 'use_dev':True, 'active':True},
            {'name': 'contentrss', 'tag':'latest', 'use_dev':True, 'active':True},
            {'name': 'contentstackoverflow', 'tag':'latest', 'use_dev':True, 'active':True},
            {'name': 'contentyoutube', 'tag':'latest', 'use_dev':True, 'active':True},
            {'name': 'feedservice', 'tag':'latest', 'use_dev':False, 'active':False},
            {'name': 'insights', 'tag':'latest', 'use_dev':False, 'active':False},
            {'name': 'reco', 'tag':'latest', 'use_dev':True, 'active':True},
            {'name': 'userservice', 'tag':'latest', 'use_dev':False, 'active':False}
        ]
external_service=[
    {'name':'kafka', 'pull_command':'docker pull wurstmeister/kafka:latest', 'active':True},
    {'name':'zookeeper', 'pull_command':'docker pull wurstmeister/zookeeper:latest', 'active':True}
]

def login_to_aws_cli():
    cmd = f"aws ecr get-login-password --region {REGION} |  docker login --username AWS --password-stdin {AWS_ID}.dkr.ecr.{REGION}.amazonaws.com"
    try:
        os.system(cmd)
        return True
    except Exception as  awserr:
        logging.error(f"AWS authentication failed {str(awserr)}")
    return False

def docker_pull():
    for service in internal_services:
        if service['active'] is True:
            if service['use_dev'] is True:
                cmd = f"docker pull {AWS_ID}.dkr.ecr.{REGION}.amazonaws.com/devimages:{service['name']}_{service['tag']}"
            else:
                cmd = f"docker pull {AWS_ID}.dkr.ecr.{REGION}.amazonaws.com/{service['name']}:{service['tag']}"
            logging.info(f"Docker pull Command is {cmd}")
            os.system(cmd)
    for service in external_service:
        if service['active'] is True:
            cmd = service['pull_command']
        logging.info(f"Docker pull Command is {cmd}")
        os.system(cmd)

def docker_start():
    log_dir = "/tmp/mentorlink"
    for service in internal_services:
        serv_log_dir = log_dir+"/"+service['name']
        if service['active'] is True:
            if service['use_dev'] is True:
                cmd = f'docker run --init --rm -d --network="host" --name {service["name"]} -v {serv_log_dir}:/tmp {AWS_ID}.dkr.ecr.{REGION}.amazonaws.com/devimages:{service["name"]}_{service["tag"]}'
            else:
                cmd = f'docker run --init --rm -d --network="host" --name {service["name"]} -v {serv_log_dir}:/tmp {AWS_ID}.dkr.ecr.{REGION}.amazonaws.com/{service["name"]}:{service["tag"]}'
            logging.info(f"Docker run Command is {cmd}")
            os.system(cmd)

def docker_stop():
    for service in internal_services:
        if service['active'] is True:
            cmd = f'docker stop {service["name"]}'
            logging.info(f"Docker stop Command is {cmd}")
            os.system(cmd)

def main():
    logging.basicConfig(level=logging.DEBUG, format='%(filename)s:%(lineno)s - %(levelname)s - %(message)s')
    command = sys.argv[1]
    logging.info(f"Command is {command}")
    if (command == "restart"):
        docker_stop()
    if(command == "start" or command == "restart"):
        if login_to_aws_cli() is False:
            exit()
        docker_pull()
        docker_start()
    else:
        docker_stop()

if __name__ == "__main__":
    main()
