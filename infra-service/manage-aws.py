#!/usr/bin/python3
#aws ecs list-services --cluster staging
#aws ecs update-service --cluster staging --service 'dev-test-bigdatameetup --desired-count <>

import subprocess
import sys
import json

def set_service_desired_count(service, desired_count) -> int:
    c1 = 'aws ecs update-service --cluster staging --service '
    c2 = service 
    c3 = ' --desired-count '
    c4 = desired_count
    print(c1+c2+c3+c4)
    try:
        subprocess.getoutput(c1+c2+c3+c4)
        ret = 1
    except subprocess.getoutput(c1+c2+c3+c4):
        ret = 0
    return ret


def set_msk_state(desired_count) -> int:
    c1 = "aws kafka "
    if (int(desired_count) > 0):
        c2 = "create-cluster "
        c3 = "--cluster-name \"mentorlink-msk\" --kafka-version \"2.6.2\" --number-of-broker-nodes 2 --broker-node-group-info file://brokernodegroupinfo.json"
        print(c1+c2+c3) 
        try:
            result = subprocess.getoutput(c1+c2+c3)
            f = open("cluster-info.json", "w")
            f.write(result)
            ret = 1
        except subprocess.getoutput(c1+c2+c3):
            ret = 0
    else:
        c2 = "delete-cluster "
        c3 = "--cluster-arn "
        f = open('cluster-info.json')
        resp = json.load(f)
        c4 = resp['ClusterArn']
        print(c1+c2+c3+c4) 
        try:
            result = subprocess.getoutput(c1+c2+c3+c4)
            ret = 1
        except subprocess.getoutput(c1+c2+c3+c4):
            ret = 0
    #print("result is ", result, "ret is ", ret)
    return ret

def main(list, desired_count) -> int:
    for service in list:
        ret = set_service_desired_count(service, desired_count)
        ret = 1
    if (ret > 0):
        set_msk_state(desired_count)
    return 1

if __name__ == "__main__":
    #print(sys.argv)
    desired_count = sys.argv[1]
    services = ['dev-test-bigdatastackoverflow', 'dev-test-contentstackoverflow',
            'dev-test-insightsservice', 'dev-test-bigdatameetup',
            'dev-test-contentrss', 'dev-test-chatservice1',
            'dev-test-bigdatayoutube', 'dev-test-bigdatakafka',
            'dev-test-userservice', 'dev-test-contentmeetup',
            'dev-test-analytics', 'dev-test-bigdatarest', 'dev-test-feedservice',
            'dev-test-appservice', 'dev-test-bigdatauser',
            'dev-test-bigdatarss', 'dev-test-contentyoutube',
            'dev-test-recoservice']
    ret = main(services, desired_count)
    if (ret > 0):
        print("success")
    else:
        print("failure")
